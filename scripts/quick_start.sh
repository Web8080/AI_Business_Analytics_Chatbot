#!/bin/bash

# Quick Start Script for AI Analytics Intelligence System

echo "======================================================================"
echo "🤖 AI Analytics Intelligence System - Quick Start"
echo "======================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it and add your OpenAI API key."
    echo ""
    read -p "Press Enter to continue after adding your API key..."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
python3 -c "from config import setup_directories; setup_directories()"

echo ""
echo "======================================================================"
echo "✅ Setup complete!"
echo "======================================================================"
echo ""
echo "To start the system, run:"
echo "  python main.py"
echo ""
echo "API Documentation will be available at:"
echo "  http://localhost:8000/docs"
echo ""
echo "======================================================================"

