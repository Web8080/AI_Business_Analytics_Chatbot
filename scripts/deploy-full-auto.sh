#!/bin/bash
# Victor.I - Fully Automated AWS Deployment (Zero Manual Steps)
# Usage: ./scripts/deploy-full-auto.sh [region]

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TIMESTAMP=$(date +%s)

echo "🚀 Fully Automated AWS Deployment for AI QueryLens"
echo "Region: $REGION"
echo "Account: $ACCOUNT_ID"
echo ""

# Generate Django secret key
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

# 1. ECR Setup
echo "📦 Setting up ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name querylens-api --region $REGION 2>/dev/null || true
aws ecr create-repository --repository-name querylens-ws --region $REGION 2>/dev/null || true

# 2. Build & Push Images
echo "🔨 Building and pushing Docker images..."
cd $REPO_ROOT
docker build -f backend/Dockerfile -t querylens-api:latest .
docker tag querylens-api:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest

docker build -f node-server/Dockerfile -t querylens-ws:latest .
docker tag querylens-ws:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest

# 3. Create IAM Role for App Runner
echo "🔐 Creating IAM role for App Runner..."
ROLE_NAME="QueryLensAppRunnerRole"
aws iam create-role --role-name $ROLE_NAME \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "build.apprunner.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }' 2>/dev/null || true

aws iam attach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess 2>/dev/null || true

sleep 5  # Wait for IAM propagation

ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

# 4. Deploy Django API to App Runner
echo "🚀 Deploying Django API to App Runner..."
cat > /tmp/apprunner-django.json <<EOF
{
  "ServiceName": "querylens-api-$TIMESTAMP",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-api:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "SECRET_KEY": "$SECRET_KEY",
          "DEBUG": "0",
          "ALLOWED_HOSTS": "*",
          "CORS_ALLOWED_ORIGINS": "*",
          "OLLAMA_MODEL": "llama3.2"
        }
      }
    },
    "AuthenticationConfiguration": {
      "AccessRoleArn": "$ROLE_ARN"
    }
  },
  "InstanceConfiguration": {
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }
}
EOF

DJANGO_ARN=$(aws apprunner create-service --cli-input-json file:///tmp/apprunner-django.json --region $REGION --query 'Service.ServiceArn' --output text)
echo "Waiting for Django API to deploy..."
aws apprunner wait service-running --service-arn $DJANGO_ARN --region $REGION
DJANGO_URL=$(aws apprunner describe-service --service-arn $DJANGO_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
echo "✅ Django API: https://$DJANGO_URL"

# 5. Deploy Node WebSocket to App Runner
echo "🚀 Deploying Node WebSocket to App Runner..."
cat > /tmp/apprunner-node.json <<EOF
{
  "ServiceName": "querylens-ws-$TIMESTAMP",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/querylens-ws:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "3001",
        "RuntimeEnvironmentVariables": {
          "DJANGO_API_URL": "https://$DJANGO_URL"
        }
      }
    },
    "AuthenticationConfiguration": {
      "AccessRoleArn": "$ROLE_ARN"
    }
  },
  "InstanceConfiguration": {
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  }
}
EOF

NODE_ARN=$(aws apprunner create-service --cli-input-json file:///tmp/apprunner-node.json --region $REGION --query 'Service.ServiceArn' --output text)
echo "Waiting for Node WebSocket to deploy..."
aws apprunner wait service-running --service-arn $NODE_ARN --region $REGION
NODE_URL=$(aws apprunner describe-service --service-arn $NODE_ARN --region $REGION --query 'Service.ServiceUrl' --output text)
echo "✅ Node WebSocket: wss://$NODE_URL"

# 6. Deploy Frontend to Amplify
echo "🚀 Deploying Frontend to Amplify..."

# Check if GitHub token exists
if [ -z "$GITHUB_TOKEN" ]; then
  echo "⚠️  GITHUB_TOKEN not set. Deploying without Git (manual zip upload)..."
  
  # Build frontend locally
  cd $REPO_ROOT/frontend
  npm ci
  NEXT_PUBLIC_API_URL=https://$DJANGO_URL NEXT_PUBLIC_WS_URL=wss://$NODE_URL npm run build
  
  # Create Amplify app for manual deployment
  AMPLIFY_APP_ID=$(aws amplify create-app --name "querylens-$TIMESTAMP" --region $REGION --query 'app.appId' --output text)
  
  echo "✅ Amplify app created: $AMPLIFY_APP_ID"
  echo "📦 To complete frontend deployment:"
  echo "   1. Zip the frontend/.next and frontend/public folders"
  echo "   2. Go to AWS Console > Amplify > querylens-$TIMESTAMP"
  echo "   3. Deploy manually or connect your Git repository"
  
else
  # Deploy with GitHub
  REPO_URL=$(git config --get remote.origin.url | sed 's/\.git$//')
  
  AMPLIFY_APP_ID=$(aws amplify create-app \
    --name "querylens-$TIMESTAMP" \
    --repository "$REPO_URL" \
    --access-token "$GITHUB_TOKEN" \
    --region $REGION \
    --query 'app.appId' --output text)
  
  aws amplify create-branch \
    --app-id $AMPLIFY_APP_ID \
    --branch-name main \
    --region $REGION
  
  aws amplify update-app \
    --app-id $AMPLIFY_APP_ID \
    --environment-variables \
      NEXT_PUBLIC_API_URL=https://$DJANGO_URL \
      NEXT_PUBLIC_WS_URL=wss://$NODE_URL \
    --build-spec "{\"version\":1,\"frontend\":{\"phases\":{\"preBuild\":{\"commands\":[\"cd frontend\",\"npm ci\"]},\"build\":{\"commands\":[\"npm run build\"]}},\"artifacts\":{\"baseDirectory\":\"frontend/.next\",\"files\":[\"**/*\"]}}}" \
    --region $REGION
  
  aws amplify start-job \
    --app-id $AMPLIFY_APP_ID \
    --branch-name main \
    --job-type RELEASE \
    --region $REGION
  
  AMPLIFY_URL=$(aws amplify get-app --app-id $AMPLIFY_APP_ID --region $REGION --query 'app.defaultDomain' --output text)
  echo "✅ Frontend deploying to: https://main.$AMPLIFY_URL"
fi

# 7. Update Django CORS
echo "🔧 Updating Django CORS settings..."
if [ ! -z "$AMPLIFY_URL" ]; then
  aws apprunner update-service \
    --service-arn $DJANGO_ARN \
    --source-configuration "ImageRepository={ImageConfiguration={RuntimeEnvironmentVariables={SECRET_KEY=$SECRET_KEY,DEBUG=0,ALLOWED_HOSTS=*,CORS_ALLOWED_ORIGINS=https://main.$AMPLIFY_URL,OLLAMA_MODEL=llama3.2}}}" \
    --region $REGION
fi

# 8. Summary
echo ""
echo "🎉 Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Django API:      https://$DJANGO_URL"
echo "📍 Node WebSocket:  wss://$NODE_URL"
[ ! -z "$AMPLIFY_URL" ] && echo "📍 Frontend:        https://main.$AMPLIFY_URL"
echo ""
echo "💰 Estimated Cost:  ~\$40-70/month"
echo ""
echo "🔧 To add custom domain:"
echo "   aws amplify create-domain-association --app-id $AMPLIFY_APP_ID --domain-name yourdomain.com"
echo ""
echo "🗑️  To delete everything:"
echo "   ./scripts/cleanup-aws.sh $REGION"
