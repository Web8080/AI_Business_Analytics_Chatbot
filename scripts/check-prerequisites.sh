#!/bin/bash
# Victor.I - Pre-flight Check for AWS Deployment

echo "🔍 Checking deployment prerequisites..."
echo ""

READY=true

# Check AWS CLI
if command -v aws &> /dev/null; then
  echo "✅ AWS CLI installed ($(aws --version | cut -d' ' -f1))"
else
  echo "❌ AWS CLI not installed"
  echo "   Install: brew install awscli (macOS) or https://aws.amazon.com/cli/"
  READY=false
fi

# Check AWS credentials
if aws sts get-caller-identity &> /dev/null; then
  ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
  REGION=$(aws configure get region)
  echo "✅ AWS credentials configured"
  echo "   Account: $ACCOUNT"
  echo "   Region: ${REGION:-us-east-1 (default)}"
else
  echo "❌ AWS credentials not configured"
  echo "   Run: aws configure"
  READY=false
fi

# Check Docker
if command -v docker &> /dev/null; then
  if docker ps &> /dev/null; then
    echo "✅ Docker installed and running"
  else
    echo "⚠️  Docker installed but not running"
    echo "   Start Docker Desktop"
    READY=false
  fi
else
  echo "❌ Docker not installed"
  echo "   Install: https://www.docker.com/products/docker-desktop"
  READY=false
fi

# Check Python
if command -v python3 &> /dev/null; then
  echo "✅ Python 3 installed ($(python3 --version))"
else
  echo "❌ Python 3 not installed"
  READY=false
fi

# Check Git
if command -v git &> /dev/null; then
  if git rev-parse --git-dir &> /dev/null 2>&1; then
    echo "✅ Git repository initialized"
  else
    echo "⚠️  Not in a Git repository (optional for deployment)"
  fi
else
  echo "⚠️  Git not installed (optional)"
fi

echo ""
if [ "$READY" = true ]; then
  echo "🎉 All prerequisites met! Ready to deploy."
  echo ""
  echo "Run: ./scripts/deploy-full-auto.sh"
else
  echo "❌ Please install missing prerequisites first."
  exit 1
fi
