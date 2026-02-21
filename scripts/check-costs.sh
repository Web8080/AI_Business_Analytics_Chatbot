#!/bin/bash
# Check current AWS costs

REGION=${1:-us-east-1}

echo "💰 Checking AWS Costs..."
echo ""

# Get current month costs
START_DATE=$(date -u -d "$(date +%Y-%m-01)" +%Y-%m-%d 2>/dev/null || date -u -v1d +%Y-%m-%d)
END_DATE=$(date -u +%Y-%m-%d)

echo "📅 Period: $START_DATE to $END_DATE"
echo ""

# Get cost breakdown
aws ce get-cost-and-usage \
  --time-period Start=$START_DATE,End=$END_DATE \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE \
  --query 'ResultsByTime[0].Groups[?Metrics.BlendedCost.Amount > `0.01`].[Keys[0], Metrics.BlendedCost.Amount]' \
  --output table

echo ""
echo "🔍 Active Resources:"
echo ""

# Check App Runner
APPRUNNER_COUNT=$(aws apprunner list-services --region $REGION --query 'ServiceSummaryList | length(@)' --output text 2>/dev/null || echo "0")
echo "  App Runner services: $APPRUNNER_COUNT"

# Check Amplify
AMPLIFY_COUNT=$(aws amplify list-apps --region $REGION --query 'apps | length(@)' --output text 2>/dev/null || echo "0")
echo "  Amplify apps: $AMPLIFY_COUNT"

# Check ECR
ECR_COUNT=$(aws ecr describe-repositories --region $REGION --query 'repositories | length(@)' --output text 2>/dev/null || echo "0")
echo "  ECR repositories: $ECR_COUNT"

echo ""
echo "💡 To stop all charges: ./scripts/cleanup-aws.sh"
