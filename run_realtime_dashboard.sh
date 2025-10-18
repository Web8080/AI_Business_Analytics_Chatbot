#!/bin/bash

# Real-time Dashboard Launch Script

echo "=========================================================================="
echo "🔄 AI ANALYTICS DASHBOARD - REAL-TIME EDITION"
echo "=========================================================================="
echo ""
echo "✨ ADVANCED FEATURE #1:"
echo "   🔄 Real-time Data Refresh (every 30 seconds)"
echo "   📊 Live Data Version Tracking"
echo "   ⏰ Data Freshness Indicators"
echo "   🎛️  Configurable Refresh Intervals"
echo "   🔄 Manual & Auto Refresh Controls"
echo "   📈 Real-time Metrics Dashboard"
echo ""
echo "Starting Real-time Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8502"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch real-time dashboard on different port
streamlit run dashboard_advanced_1.py --server.port 8502 --server.headless true
