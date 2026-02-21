#!/bin/bash
# Victor.I - Quick Frontend-Only Deployment (No Docker, No Backend)
# This is FREE on AWS free tier!

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TIMESTAMP=$(date +%s)

echo "🚀 Quick Frontend Deployment (FREE TIER)"
echo "Region: $REGION"
echo ""

# Check if we have a Git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "❌ Not a Git repository. Initializing..."
  git init
  git add .
  git commit -m "Initial commit for deployment"
fi

# Get GitHub token if available
if [ -z "$GITHUB_TOKEN" ]; then
  echo "⚠️  No GITHUB_TOKEN set. Using manual deployment..."
  echo ""
  echo "📦 Building frontend locally..."
  cd $REPO_ROOT/frontend
  
  # Install dependencies
  npm ci || npm install
  
  # Build
  npm run build
  
  echo ""
  echo "✅ Frontend built successfully!"
  echo ""
  echo "📋 Next steps:"
  echo "1. Go to: https://console.aws.amazon.com/amplify/home?region=$REGION"
  echo "2. Click 'New app' > 'Deploy without Git'"
  echo "3. Drag and drop the 'frontend/.next' folder"
  echo ""
  echo "💰 Cost: FREE (covered by AWS free tier)"
  
else
  # Deploy with GitHub
  echo "🔗 Deploying from GitHub..."
  
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
  
  # Set build spec for monorepo
  aws amplify update-app \
    --app-id $AMPLIFY_APP_ID \
    --build-spec '{
      "version": 1,
      "frontend": {
        "phases": {
          "preBuild": {
            "commands": ["cd frontend", "npm ci"]
          },
          "build": {
            "commands": ["npm run build"]
          }
        },
        "artifacts": {
          "baseDirectory": "frontend/.next",
          "files": ["**/*"]
        }
      }
    }' \
    --region $REGION
  
  aws amplify start-job \
    --app-id $AMPLIFY_APP_ID \
    --branch-name main \
    --job-type RELEASE \
    --region $REGION
  
  AMPLIFY_URL=$(aws amplify get-app --app-id $AMPLIFY_APP_ID --region $REGION --query 'app.defaultDomain' --output text)
  
  echo ""
  echo "🎉 Deployment Started!"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📍 Frontend URL: https://main.$AMPLIFY_URL"
  echo "💰 Cost: FREE (AWS free tier)"
  echo ""
  echo "⏱️  Build will take ~5 minutes"
  echo "🔍 Check status: https://console.aws.amazon.com/amplify/home?region=$REGION#/$AMPLIFY_APP_ID"
fi
