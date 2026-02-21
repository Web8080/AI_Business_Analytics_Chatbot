#!/bin/bash
# Victor.I - Cleanup AWS Resources
# Usage: ./scripts/cleanup-aws.sh [region]

set -e

REGION=${1:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "🗑️  Cleaning up AWS resources..."

# Delete App Runner services
echo "Deleting App Runner services..."
for service in $(aws apprunner list-services --region $REGION --query 'ServiceSummaryList[?starts_with(ServiceName, `querylens`)].ServiceArn' --output text); do
  echo "  Deleting $service"
  aws apprunner delete-service --service-arn $service --region $REGION
done

# Delete Amplify apps
echo "Deleting Amplify apps..."
for app in $(aws amplify list-apps --region $REGION --query 'apps[?starts_with(name, `querylens`)].appId' --output text); do
  echo "  Deleting $app"
  aws amplify delete-app --app-id $app --region $REGION
done

# Delete ECR images
echo "Deleting ECR images..."
aws ecr batch-delete-image --repository-name querylens-api --region $REGION \
  --image-ids "$(aws ecr list-images --repository-name querylens-api --region $REGION --query 'imageIds[*]' --output json)" 2>/dev/null || true
aws ecr batch-delete-image --repository-name querylens-ws --region $REGION \
  --image-ids "$(aws ecr list-images --repository-name querylens-ws --region $REGION --query 'imageIds[*]' --output json)" 2>/dev/null || true

# Delete ECR repositories
echo "Deleting ECR repositories..."
aws ecr delete-repository --repository-name querylens-api --region $REGION --force 2>/dev/null || true
aws ecr delete-repository --repository-name querylens-ws --region $REGION --force 2>/dev/null || true

echo "✅ Cleanup complete!"
