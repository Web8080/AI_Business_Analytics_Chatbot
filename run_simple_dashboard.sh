#!/bin/bash

# Simple Dashboard Launch Script

echo "=========================================================================="
echo "🤖 AI ANALYTICS DASHBOARD - SIMPLE & RELIABLE"
echo "=========================================================================="
echo ""
echo "✨ CORE FEATURES:"
echo "   🤖 Chatbot - Main AI assistant (NO INFINITE LOOPS)"
echo "   📊 Data Overview - Basic data analysis"
echo "   ⚡ Quick Actions - Pre-built questions"
echo "   🎨 Theme Toggle - Light/Dark mode"
echo "   📤 Export Options - Download data and chat"
echo "   🗑️ Clear Chat - Reset conversation"
echo ""
echo "🎯 KEY BENEFITS:"
echo "   ✅ NO infinite loops or errors"
echo "   ✅ Chatbot works immediately after upload"
echo "   ✅ Clean, simple interface"
echo "   ✅ Reliable and stable"
echo "   ✅ Easy to use"
echo ""
echo "Starting Simple Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch simple dashboard
streamlit run dashboard_simple.py --server.port 8501 --server.headless true
