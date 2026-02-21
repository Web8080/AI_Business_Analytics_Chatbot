#!/bin/bash
# Victor.I - AWS Deployment Script for AI QueryLens
# Usage: ./scripts/deploy-aws.sh [region] [account-id]

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=${2:-$(aws sts get-caller-identity --query Account --output text)}
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)

echo "Deploying AI QueryLens to AWS"
echo "Region: $REGION"
echo "Account: $ACCOUNT_ID"
echo "Root: $REPO_ROOT"

# ECR Login
echo "Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Create ECR repositories
echo "Creating ECR repositories..."
aws ecr create-repository --repository-name querylens-api --region $REGION 2>/dev/null || echo "querylens-api repo exists"
aws ecr create-repository --repository-name querylens-ws --region $REGION 2>/dev/null || echo "querylens-ws repo exists"

# Build and push Django API
echo "Building Django API..."
cd $REPO_ROOT
docker build -f backend/Dockerfile -t querylens-api:latest .
docker tag querylens-api:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest
echo "Pushing Django API to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest

# Build and push Node WebSocket
echo "Building Node WebSocket server..."
docker build -f node-server/Dockerfile -t querylens-ws:latest .
docker tag querylens-ws:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest
echo "Pushing Node WS to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest

echo "Images pushed to ECR."
echo ""
echo "Next steps:"
echo "1. Deploy Django API to App Runner:"
echo "   - Go to AWS Console > App Runner > Create service"
echo "   - Source: ECR > $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest"
echo "   - Port: 8000"
echo "   - Add env vars: SECRET_KEY, DEBUG=0, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, OLLAMA_BASE_URL"
echo ""
echo "2. Deploy Node WS to App Runner:"
echo "   - Source: ECR > $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest"
echo "   - Port: 3001"
echo "   - Add env var: DJANGO_API_URL=<your-django-url>"
echo ""
echo "3. Deploy Frontend to Amplify:"
echo "   - Connect repo, set root to 'frontend'"
echo "   - Add env vars: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_WS_URL"
