#!/bin/bash

echo "🚀 Starting OpenAI-Powered Analytics Dashboard..."
echo "=================================================="

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   The system will use fallback mode without OpenAI GPT-4"
    echo "   To enable OpenAI features:"
    echo "   1. Get API key from: https://platform.openai.com/api-keys"
    echo "   2. Set environment variable: export OPENAI_API_KEY='your-key-here'"
    echo "   3. Or add to .env file: OPENAI_API_KEY=your-key-here"
    echo ""
fi

# Install required packages if not already installed
echo "📦 Checking dependencies..."
pip install -q openai

# Start the dashboard
echo "🌐 Starting dashboard at http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

streamlit run dashboard_openai.py --server.port 8501 --server.address localhost
