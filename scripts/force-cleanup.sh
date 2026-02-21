#!/bin/bash
# Force cleanup - waits for services to be deletable

REGION=us-east-1

echo "🗑️  Force cleanup - waiting for services..."

# Get all services
SERVICES=$(aws apprunner list-services --region $REGION --query 'ServiceSummaryList[?starts_with(ServiceName, `querylens`)].ServiceArn' --output text)

for SERVICE_ARN in $SERVICES; do
  echo "Waiting for $SERVICE_ARN to be deletable..."
  
  for i in {1..30}; do
    STATUS=$(aws apprunner describe-service --service-arn $SERVICE_ARN --region $REGION --query 'Service.Status' --output text 2>/dev/null || echo "DELETED")
    
    if [ "$STATUS" == "DELETED" ] || [ "$STATUS" == "DELETE_FAILED" ]; then
      echo "Already deleted"
      break
    fi
    
    if [ "$STATUS" != "OPERATION_IN_PROGRESS" ]; then
      echo "Deleting..."
      aws apprunner delete-service --service-arn $SERVICE_ARN --region $REGION 2>/dev/null || true
      break
    fi
    
    echo "  [$i/30] Status: $STATUS"
    sleep 10
  done
done

# Delete ECR
echo "Deleting ECR..."
aws ecr delete-repository --repository-name querylens-api --region $REGION --force 2>/dev/null || true
aws ecr delete-repository --repository-name querylens-ws --region $REGION --force 2>/dev/null || true

echo "✅ Cleanup complete!"
