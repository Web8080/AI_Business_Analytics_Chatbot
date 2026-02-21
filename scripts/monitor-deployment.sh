#!/bin/bash
# Monitor App Runner deployment

SERVICE_ARN="arn:aws:apprunner:us-east-1:920373025107:service/querylens-api-1771687798"

echo "🔍 Monitoring deployment..."
echo ""

for i in {1..30}; do
  STATUS=$(aws apprunner describe-service --service-arn $SERVICE_ARN --region us-east-1 --query 'Service.Status' --output text 2>/dev/null)
  
  if [ "$STATUS" == "RUNNING" ]; then
    URL=$(aws apprunner describe-service --service-arn $SERVICE_ARN --region us-east-1 --query 'Service.ServiceUrl' --output text)
    echo ""
    echo "🎉 Deployment Complete!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 Django API: https://$URL"
    echo ""
    echo "💰 Cost: ~\$25-50/month"
    echo "💳 Budget: \$50/month (updated)"
    echo "🗑️  Delete: ./scripts/cleanup-aws.sh"
    exit 0
  elif [ "$STATUS" == "CREATE_FAILED" ]; then
    echo "❌ Deployment failed"
    exit 1
  fi
  
  echo "[$i/30] Status: $STATUS"
  sleep 20
done

echo "⏰ Still deploying. Check: https://console.aws.amazon.com/apprunner/home?region=us-east-1#/services"
