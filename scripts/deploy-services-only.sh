#!/bin/bash
# Victor.I - Resume Deployment (Skip Docker builds)
# Use this if deployment was interrupted

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TIMESTAMP=$(date +%s)

echo "🔄 Resuming AWS Deployment"
echo "Region: $REGION"
echo "Account: $ACCOUNT_ID"
echo ""

# Check if images exist in ECR
echo "📦 Checking ECR images..."
DJANGO_IMAGE="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest"
NODE_IMAGE="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest"

if ! aws ecr describe-images --repository-name querylens-api --image-ids imageTag=latest --region $REGION &>/dev/null; then
  echo "❌ Django image not found. Run ./scripts/deploy-full-auto.sh first"
  exit 1
fi

if ! aws ecr describe-images --repository-name querylens-ws --image-ids imageTag=latest --region $REGION &>/dev/null; then
  echo "❌ Node image not found. Run ./scripts/deploy-full-auto.sh first"
  exit 1
fi

echo "✅ Images found in ECR"
echo ""

# Get or create IAM role
ROLE_NAME="QueryLensAppRunnerRole"
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>/dev/null || echo "")

if [ -z "$ROLE_ARN" ]; then
  echo "🔐 Creating IAM role..."
  aws iam create-role --role-name $ROLE_NAME \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "build.apprunner.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }'
  
  aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
  
  sleep 5
  ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)
fi

echo "✅ IAM role ready: $ROLE_ARN"
echo ""

# Generate Django secret
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

# Deploy Django API
echo "🚀 Deploying Django API..."
DJANGO_ARN=$(aws apprunner create-service \
  --service-name "querylens-api-$TIMESTAMP" \
  --source-configuration "{
    \"ImageRepository\": {
      \"ImageIdentifier\": \"$DJANGO_IMAGE\",
      \"ImageRepositoryType\": \"ECR\",
      \"ImageConfiguration\": {
        \"Port\": \"8000\",
        \"RuntimeEnvironmentVariables\": {
          \"SECRET_KEY\": \"$SECRET_KEY\",
          \"DEBUG\": \"0\",
          \"ALLOWED_HOSTS\": \"*\",
          \"CORS_ALLOWED_ORIGINS\": \"*\",
          \"OLLAMA_MODEL\": \"llama3.2\"
        }
      }
    },
    \"AuthenticationConfiguration\": {
      \"AccessRoleArn\": \"$ROLE_ARN\"
    }
  }" \
  --instance-configuration "Cpu=1 vCPU,Memory=2 GB" \
  --region $REGION \
  --query 'Service.ServiceArn' --output text)

echo "⏳ Waiting for Django API..."
aws apprunner wait service-running --service-arn $DJANGO_ARN --region $REGION
DJANGO_URL=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
echo "✅ Django API: https://$DJANGO_URL"
echo ""

# Deploy Node WebSocket
echo "🚀 Deploying Node WebSocket..."
NODE_ARN=$(aws apprunner create-service \
  --service-name "querylens-ws-$TIMESTAMP" \
  --source-configuration "{
    \"ImageRepository\": {
      \"ImageIdentifier\": \"$NODE_IMAGE\",
      \"ImageRepositoryType\": \"ECR\",
      \"ImageConfiguration\": {
        \"Port\": \"3001\",
        \"RuntimeEnvironmentVariables\": {
          \"DJANGO_API_URL\": \"https://$DJANGO_URL\"
        }
      }
    },
    \"AuthenticationConfiguration\": {
      \"AccessRoleArn\": \"$ROLE_ARN\"
    }
  }" \
  --instance-configuration "Cpu=0.25 vCPU,Memory=0.5 GB" \
  --region $REGION \
  --query 'Service.ServiceArn' --output text)

echo "⏳ Waiting for Node WebSocket..."
aws apprunner wait service-running --service-arn $NODE_ARN --region $REGION
NODE_URL=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
echo "✅ Node WebSocket: wss://$NODE_URL"
echo ""

# Summary
echo "🎉 Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Django API:      https://$DJANGO_URL"
echo "📍 Node WebSocket:  wss://$NODE_URL"
echo ""
echo "💰 Estimated Cost:  ~\$10-15/month"
echo ""
echo "🗑️  To delete: ./scripts/cleanup-aws.sh"
