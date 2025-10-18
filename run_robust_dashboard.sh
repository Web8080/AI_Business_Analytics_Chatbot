#!/bin/bash

# Robust Dashboard Launch Script

echo "=========================================================================="
echo "🚀 AI ANALYTICS DASHBOARD - PROFESSIONAL EDITION"
echo "=========================================================================="
echo ""
echo "✨ PROFESSIONAL FEATURES:"
echo "   🤖 AI Chatbot - Main assistant with proper input clearing"
echo "   📊 Data Overview - Comprehensive data analysis"
echo "   🔧 Advanced Features - Cohort, A/B Testing (in submenu)"
echo "   ⚙️ Settings - Theme, export, system management"
echo "   🎨 Professional UI - Modern, responsive design"
echo "   📱 Responsive Layout - Works on all screen sizes"
echo ""
echo "🎯 KEY IMPROVEMENTS:"
echo "   ✅ Chat input clears after sending"
echo "   ✅ Responsive and professional UI"
echo "   ✅ Advanced features in separate tab"
echo "   ✅ No infinite loops or errors"
echo "   ✅ Proper form handling"
echo "   ✅ Modern gradient design"
echo ""
echo "Starting Professional Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch robust dashboard
streamlit run dashboard_robust.py --server.port 8501 --server.headless true
