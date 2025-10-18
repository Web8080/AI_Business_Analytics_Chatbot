#!/bin/bash

# Advanced Analytics Dashboard Launch Script

echo "=========================================================================="
echo "📊 AI ANALYTICS DASHBOARD - ADVANCED ANALYTICS EDITION"
echo "=========================================================================="
echo ""
echo "✨ ADVANCED FEATURE #3:"
echo "   📈 Cohort Analysis - Customer retention & behavior tracking"
echo "   🧪 A/B Testing - Statistical significance testing"
echo "   📊 Comparative Analysis - Period-over-period comparisons"
echo "   🎯 Scenario Planning - What-if analysis (coming soon)"
echo "   📊 Statistical Rigor - P-values, effect sizes, confidence intervals"
echo "   📈 Interactive Visualizations - Heatmaps, bar charts, comparisons"
echo "   🎛️  Configurable Parameters - Customizable analysis settings"
echo ""
echo "📦 Installing advanced analytics dependencies..."
pip install -q scipy scikit-learn
echo ""
echo "Starting Advanced Analytics Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8504"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch advanced analytics dashboard on different port
streamlit run dashboard_advanced_3.py --server.port 8504 --server.headless true
