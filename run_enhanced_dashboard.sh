#!/bin/bash

# Enhanced Dashboard Launch Script with Quick Wins

echo "=========================================================================="
echo "🚀 AI ANALYTICS DASHBOARD - ENHANCED UI"
echo "=========================================================================="
echo ""
echo "✨ NEW FEATURES:"
echo "   🎨 Dark/Light Theme Toggle"
echo "   ⚡ Quick Action Buttons"
echo "   📚 Chat History Saving"
echo "   📤 Export Data & Chat"
echo "   🔍 Data Quality Indicators"
echo "   ❓ Help & Tips"
echo "   ⌨️  Keyboard Shortcuts"
echo ""
echo "Starting Enhanced Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch enhanced dashboard
streamlit run dashboard_enhanced_ui.py --server.port 8501 --server.headless true
