#!/bin/bash

# Quick Launch Script for Dashboard and Visualizations

echo "=========================================================================="
echo "AI ANALYTICS DASHBOARD - QUICK LAUNCH"
echo "=========================================================================="
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Installing Streamlit..."
    pip install streamlit -q
fi

echo "Starting Streamlit Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo ""
echo "Available Pages:"
echo "  1. Overview - KPIs and Performance Summary"
echo "  2. Descriptive Analytics - Trends and Statistics"
echo "  3. Predictive Models - Forecasts and Churn Prediction"
echo "  4. Recommendations - Actionable Insights"
echo "  5. Visualizations - Interactive Charts"
echo "  6. Raw Data - Data Explorer"
echo ""
echo "HTML Visualizations:"
echo "  - results/images/revenue_trend.html"
echo "  - results/images/product_performance.html"
echo "  - results/images/correlation_matrix.html"
echo "  - results/images/forecast_30days.html"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch dashboard
streamlit run dashboard.py --server.port 8501 --server.headless true

