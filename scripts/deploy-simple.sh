#!/bin/bash
# Simple App Runner deployment with TCP health check

REGION=us-east-1
ACCOUNT_ID=920373025107
TIMESTAMP=$(date +%s)

echo "🚀 Deploying to App Runner..."

# Get IAM role
ROLE_ARN=$(aws iam get-role --role-name QueryLensAppRunnerRole --query 'Role.Arn' --output text 2>/dev/null)

if [ -z "$ROLE_ARN" ]; then
  echo "Creating IAM role..."
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

# Deploy Django with TCP health check
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

echo "Creating App Runner service..."
DJANGO_ARN=$(aws apprunner create-service \
  --service-name "querylens-$TIMESTAMP" \
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
  --health-check-configuration "Protocol=TCP,Interval=10,Timeout=5,HealthyThreshold=1,UnhealthyThreshold=3" \
  --region $REGION \
  --query 'Service.ServiceArn' --output text)

echo "Service ARN: $DJANGO_ARN"
echo ""
echo "⏳ Deployment started. Check status:"
echo "https://console.aws.amazon.com/apprunner/home?region=$REGION#/services"
echo ""
echo "Or run: aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.[Status,ServiceUrl]'"
