#!/bin/bash

# Unified Dashboard Launch Script

echo "=========================================================================="
echo "🚀 AI ANALYTICS DASHBOARD - UNIFIED EDITION"
echo "=========================================================================="
echo ""
echo "✨ ALL FEATURES COMBINED:"
echo "   🤖 Chatbot - Main AI assistant (works immediately after upload)"
echo "   📊 Data Overview - Comprehensive data analysis"
echo "   📈 Advanced Analytics - Cohort, A/B Testing, Comparative (optional)"
echo "   🔄 Real-time - Auto-refresh capabilities (optional)"
echo "   🎤 Voice - Speech features (optional)"
echo "   ⚙️ Settings - Theme, export, configuration"
echo ""
echo "🎯 KEY BENEFITS:"
echo "   ✅ Chatbot works immediately after data upload"
echo "   ✅ Advanced features are optional menu items"
echo "   ✅ No errors - all features properly integrated"
echo "   ✅ Clean, professional interface"
echo "   ✅ Easy navigation between features"
echo ""
echo "Starting Unified Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch unified dashboard
streamlit run dashboard_unified.py --server.port 8501 --server.headless true
