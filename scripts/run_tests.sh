#!/bin/bash

# Run Tests Script

echo "🧪 Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing

echo ""
echo "✅ Tests complete!"

