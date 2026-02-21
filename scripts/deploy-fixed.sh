#!/bin/bash
# Victor.I - Fixed AWS Deployment with Production Server

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TIMESTAMP=$(date +%s)

echo "🚀 AWS Deployment (Fixed)"
echo ""

# 1. ECR Setup
echo "📦 ECR Login..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

echo "📦 Creating repositories..."
aws ecr create-repository --repository-name querylens-api --region $REGION 2>/dev/null || true

# 2. Build & Push Django only
echo "🔨 Building Django with Gunicorn..."
cd $REPO_ROOT
docker build -f backend/Dockerfile -t querylens-api:latest .
docker tag querylens-api:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest

echo "⬆️  Pushing to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest

# 3. Get IAM Role
echo "🔐 Getting IAM role..."
ROLE_ARN=$(aws iam get-role --role-name QueryLensAppRunnerRole --query 'Role.Arn' --output text 2>/dev/null || echo "")

if [ -z "$ROLE_ARN" ]; then
  aws iam create-role --role-name QueryLensAppRunnerRole \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "build.apprunner.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }'
  
  aws iam attach-role-policy --role-name QueryLensAppRunnerRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
  
  sleep 5
  ROLE_ARN=$(aws iam get-role --role-name QueryLensAppRunnerRole --query 'Role.Arn' --output text)
fi

# 4. Deploy Django
echo "🚀 Deploying Django API..."
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

DJANGO_ARN=$(aws apprunner create-service \
  --service-name "querylens-api-$TIMESTAMP" \
  --source-configuration "{
    \"ImageRepository\": {
      \"ImageIdentifier\": \"$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest\",
      \"ImageRepositoryType\": \"ECR\",
      \"ImageConfiguration\": {
        \"Port\": \"8000\",
        \"RuntimeEnvironmentVariables\": {
          \"SECRET_KEY\": \"$SECRET_KEY\",
          \"DEBUG\": \"0\",
          \"ALLOWED_HOSTS\": \"*\",
          \"CORS_ALLOWED_ORIGINS\": \"*\"
        }
      }
    },
    \"AuthenticationConfiguration\": {
      \"AccessRoleArn\": \"$ROLE_ARN\"
    }
  }" \
  --instance-configuration "Cpu=1 vCPU,Memory=2 GB" \
  --health-check-configuration "Protocol=HTTP,Path=/admin,Interval=10,Timeout=5,HealthyThreshold=1,UnhealthyThreshold=3" \
  --region $REGION \
  --query 'Service.ServiceArn' --output text)

echo "⏳ Waiting for deployment (5-10 min)..."
echo "   Service ARN: $DJANGO_ARN"

# Poll status
for i in {1..60}; do
  STATUS=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.Status' --output text 2>/dev/null || echo "ERROR")
  
  if [ "$STATUS" == "RUNNING" ]; then
    DJANGO_URL=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
    echo ""
    echo "🎉 Deployment Complete!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 Django API: https://$DJANGO_URL"
    echo ""
    echo "💰 Cost: ~\$25-50/month"
    echo "🗑️  Delete: ./scripts/cleanup-aws.sh"
    exit 0
  elif [ "$STATUS" == "CREATE_FAILED" ]; then
    echo ""
    echo "❌ Deployment failed!"
    echo "Check logs: https://console.aws.amazon.com/apprunner/home?region=$REGION#/services"
    exit 1
  fi
  
  echo "   Status: $STATUS (attempt $i/60)"
  sleep 10
done

echo "⏰ Timeout waiting for deployment"
echo "Check status: https://console.aws.amazon.com/apprunner/home?region=$REGION#/services"
