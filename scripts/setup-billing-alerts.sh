#!/bin/bash
# Set up AWS billing alerts

set -e

echo "🔔 Setting up AWS Billing Alerts"
echo ""

# Get email
read -p "Enter your email for billing alerts: " EMAIL

if [ -z "$EMAIL" ]; then
  echo "❌ Email required"
  exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Update notification config with email
cat > /tmp/budget-notifications.json <<EOF
[
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 50,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
      {
        "SubscriptionType": "EMAIL",
        "Address": "$EMAIL"
      }
    ]
  },
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
      {
        "SubscriptionType": "EMAIL",
        "Address": "$EMAIL"
      }
    ]
  },
  {
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 100,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [
      {
        "SubscriptionType": "EMAIL",
        "Address": "$EMAIL"
      }
    ]
  }
]
EOF

# Get budget amount
read -p "Enter monthly budget limit in USD (default: 50): " BUDGET
BUDGET=${BUDGET:-50}

# Create budget config
cat > /tmp/budget-config.json <<EOF
{
  "BudgetName": "QueryLens-Monthly-Budget",
  "BudgetLimit": {
    "Amount": "$BUDGET",
    "Unit": "USD"
  },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST",
  "CostFilters": {},
  "CostTypes": {
    "IncludeTax": true,
    "IncludeSubscription": true,
    "UseBlended": false,
    "IncludeRefund": false,
    "IncludeCredit": false,
    "IncludeUpfront": true,
    "IncludeRecurring": true,
    "IncludeOtherSubscription": true,
    "IncludeSupport": true,
    "IncludeDiscount": true,
    "UseAmortized": false
  }
}
EOF

echo ""
echo "Creating budget: \$$BUDGET/month"
echo "Email alerts to: $EMAIL"
echo ""

# Create budget
aws budgets create-budget \
  --account-id $ACCOUNT_ID \
  --budget file:///tmp/budget-config.json \
  --notifications-with-subscribers file:///tmp/budget-notifications.json

echo ""
echo "✅ Billing alerts configured!"
echo ""
echo "You'll receive emails when you reach:"
echo "  • 50% of budget (\$$(echo "$BUDGET * 0.5" | bc))"
echo "  • 80% of budget (\$$(echo "$BUDGET * 0.8" | bc))"
echo "  • 100% of budget (\$$BUDGET)"
echo ""
echo "⚠️  Check your email and confirm the subscription!"
