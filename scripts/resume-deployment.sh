#!/bin/bash
# Victor.I - Resume from where deployment stopped
# Skips Docker builds, only deploys services

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
TIMESTAMP=$(date +%s)

echo "🔄 Resuming Deployment"
echo ""

# Check if images exist
if ! aws ecr describe-images --repository-name querylens-api --image-ids imageTag=latest --region $REGION &>/dev/null; then
  echo "❌ Images not found. Run ./scripts/deploy-full-auto.sh first"
  exit 1
fi

echo "✅ Docker images found in ECR"

# Get IAM role
ROLE_ARN=$(aws iam get-role --role-name QueryLensAppRunnerRole --query 'Role.Arn' --output text 2>/dev/null)
if [ -z "$ROLE_ARN" ]; then
  echo "❌ IAM role not found. Run ./scripts/deploy-full-auto.sh first"
  exit 1
fi

echo "✅ IAM role found"
echo ""

# Check if Django service already exists
EXISTING_DJANGO=$(aws apprunner list-services --region $REGION --query "ServiceSummaryList[?starts_with(ServiceName, 'querylens-api')].ServiceArn" --output text | head -1)

if [ ! -z "$EXISTING_DJANGO" ]; then
  echo "📍 Django service already exists"
  DJANGO_ARN=$EXISTING_DJANGO
  
  # Wait for it to be running
  echo "⏳ Checking Django status..."
  while true; do
    STATUS=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.Status' --output text)
    if [ "$STATUS" == "RUNNING" ]; then
      break
    fi
    echo "   Status: $STATUS (waiting...)"
    sleep 10
  done
  
  DJANGO_URL=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
  echo "✅ Django API: https://$DJANGO_URL"
else
  # Create Django service
  echo "🚀 Creating Django service..."
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
    --region $REGION \
    --query 'Service.ServiceArn' --output text)
  
  echo "⏳ Waiting for Django (this takes ~3 minutes)..."
  while true; do
    STATUS=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.Status' --output text)
    if [ "$STATUS" == "RUNNING" ]; then
      break
    fi
    echo "   Status: $STATUS"
    sleep 15
  done
  
  DJANGO_URL=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
  echo "✅ Django API: https://$DJANGO_URL"
fi

echo ""

# Check if Node service exists
EXISTING_NODE=$(aws apprunner list-services --region $REGION --query "ServiceSummaryList[?starts_with(ServiceName, 'querylens-ws')].ServiceArn" --output text | head -1)

if [ ! -z "$EXISTING_NODE" ]; then
  echo "📍 Node service already exists"
  NODE_ARN=$EXISTING_NODE
  
  echo "⏳ Checking Node status..."
  while true; do
    STATUS=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.Status' --output text)
    if [ "$STATUS" == "RUNNING" ]; then
      break
    fi
    echo "   Status: $STATUS (waiting...)"
    sleep 10
  done
  
  NODE_URL=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
  echo "✅ Node WebSocket: wss://$NODE_URL"
else
  # Create Node service
  echo "🚀 Creating Node service..."
  
  NODE_ARN=$(aws apprunner create-service \
    --service-name "querylens-ws-$TIMESTAMP" \
    --source-configuration "{
      \"ImageRepository\": {
        \"ImageIdentifier\": \"$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest\",
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
  
  echo "⏳ Waiting for Node (this takes ~2 minutes)..."
  while true; do
    STATUS=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.Status' --output text)
    if [ "$STATUS" == "RUNNING" ]; then
      break
    fi
    echo "   Status: $STATUS"
    sleep 15
  done
  
  NODE_URL=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
  echo "✅ Node WebSocket: wss://$NODE_URL"
fi

echo ""
echo "🎉 Backend Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Django API:      https://$DJANGO_URL"
echo "📍 Node WebSocket:  wss://$NODE_URL"
echo ""
echo "💰 Cost: ~\$10-15/month"
echo "🗑️  Delete: ./scripts/cleanup-aws.sh"
