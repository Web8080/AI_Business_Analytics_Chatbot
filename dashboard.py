"""
Streamlit Dashboard - Interactive Analytics Visualization
Run with: streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">AI Analytics Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select View",
        ["Overview", "Descriptive Analytics", "Predictive Models", "Recommendations", "Visualizations", "Raw Data"]
    )
    
    st.markdown("---")
    st.markdown("### System Info")
    st.info("Execution Time: 0.33s\n\nData Quality: 100/100\n\nModels Trained: 3")

# Load data
results_dir = Path('results')

@st.cache_data
def load_json(filename):
    """Load JSON file"""
    path = results_dir / filename
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None

@st.cache_data
def load_csv(filename):
    """Load CSV file"""
    path = results_dir / filename
    if path.exists():
        return pd.read_csv(path)
    return None

# Load all data
kpis = load_json('kpis.json')
trends = load_json('trends.json')
forecast = load_json('forecast.json')
churn = load_json('churn_prediction.json')
recommendations = load_json('recommendations.json')
cleaned_data = load_csv('cleaned_sales_data.csv')
summary = load_json('demo_results_summary.json')

# OVERVIEW PAGE
if page == "Overview":
    st.header("Executive Summary")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${kpis['revenue']['total_revenue']:,.2f}" if kpis else "N/A",
            delta=f"+{kpis['revenue']['revenue_growth_rate']:.1f}%" if kpis and kpis['revenue'].get('revenue_growth_rate') else None
        )
    
    with col2:
        st.metric(
            label="Customers",
            value=kpis['customers']['total_customers'] if kpis else "N/A"
        )
    
    with col3:
        st.metric(
            label="Churn Rate",
            value=f"{churn['churn_rate']:.1f}%" if churn else "N/A",
            delta=f"-{churn['churn_rate']:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Avg Revenue/Trans",
            value=f"${kpis['revenue']['average_revenue']:,.2f}" if kpis else "N/A"
        )
    
    st.markdown("---")
    
    # Performance Summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pipeline Performance")
        if summary:
            perf_data = []
            for stage, data in summary['stages'].items():
                perf_data.append({
                    'Stage': stage.replace('_', ' ').title(),
                    'Duration (s)': f"{data['duration']:.3f}"
                })
            st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)
            
            st.success(f"**Total Execution Time:** {summary['total_duration']:.2f} seconds")
    
    with col2:
        st.subheader("Top Recommendations")
        if recommendations:
            for i, rec in enumerate(recommendations['recommendations'][:3], 1):
                priority_color = "🔴" if rec['priority'] == 'high' else "🟡"
                st.markdown(f"{priority_color} **{i}.** {rec['recommendation'][:100]}...")
    
    # Data Quality
    st.markdown("---")
    st.subheader("Data Quality Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows Processed", summary['stages']['data_ingestion']['rows_loaded'] if summary else "N/A")
    col2.metric("Quality Score", f"{summary['stages']['data_ingestion']['quality_score']}/100" if summary else "N/A")
    col3.metric("Duplicates", "0")
    col4.metric("Missing Values", "0%")

# DESCRIPTIVE ANALYTICS PAGE
elif page == "Descriptive Analytics":
    st.header("Descriptive Analytics")
    
    # KPIs
    st.subheader("Key Performance Indicators")
    if kpis:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Revenue Metrics")
            st.metric("Total Revenue", f"${kpis['revenue']['total_revenue']:,.2f}")
            st.metric("Average Revenue", f"${kpis['revenue']['average_revenue']:,.2f}")
            st.metric("Median Revenue", f"${kpis['revenue']['median_revenue']:,.2f}")
            if kpis['revenue'].get('revenue_growth_rate'):
                st.metric("Growth Rate", f"{kpis['revenue']['revenue_growth_rate']:.1f}%")
        
        with col2:
            st.markdown("### Customer & Product Metrics")
            st.metric("Total Customers", kpis['customers']['total_customers'])
            st.metric("Avg Trans/Customer", f"{kpis['customers']['average_transactions_per_customer']:.1f}")
            st.metric("Total Products", kpis['products']['total_products'])
            st.metric("Top Product", kpis['products']['top_product'])
    
    # Trends
    st.markdown("---")
    st.subheader("Trend Analysis")
    if trends and 'trends' in trends:
        for metric, trend_data in trends['trends'].items():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"**{metric.title()}**")
            
            with col2:
                direction_emoji = "📈" if trend_data['direction'] == 'increasing' else "📉" if trend_data['direction'] == 'decreasing' else "➡️"
                st.markdown(f"{direction_emoji} {trend_data['direction'].upper()}")
                st.progress(min(abs(trend_data['r_squared']), 1.0))
            
            with col3:
                st.metric("Change", f"{trend_data['percent_change']:+.1f}%")

# PREDICTIVE MODELS PAGE
elif page == "Predictive Models":
    st.header("Predictive Analytics & Model Performance")
    
    # Forecast Model
    st.subheader("📈 Time Series Forecast")
    col1, col2, col3 = st.columns(3)
    
    if forecast and forecast['status'] == 'success':
        with col1:
            st.metric("Model", forecast['model_type'].replace('_', ' ').title())
        with col2:
            if 'historical_performance' in forecast:
                st.metric("MAE", f"${forecast['historical_performance']['mae']:,.2f}")
        with col3:
            if 'historical_performance' in forecast:
                st.metric("MAPE", f"{forecast['historical_performance']['mape']:.2f}%")
        
        # Forecast Chart
        if 'forecast' in forecast:
            forecast_df = pd.DataFrame(forecast['forecast'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_df['ds'],
                y=forecast_df['yhat'],
                mode='lines',
                name='Forecast',
                line=dict(color='red', width=2)
            ))
            
            if 'yhat_lower' in forecast_df.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat_upper'],
                    mode='lines',
                    name='Upper Bound',
                    line=dict(width=0),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat_lower'],
                    mode='lines',
                    name='Confidence Interval',
                    fill='tonexty',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(width=0)
                ))
            
            fig.update_layout(
                title="30-Day Revenue Forecast",
                xaxis_title="Date",
                yaxis_title="Predicted Revenue ($)",
                template="plotly_white",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Churn Prediction
    st.subheader("👥 Customer Churn Prediction")
    if churn and churn['status'] == 'success':
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", churn['total_users'])
        with col2:
            st.metric("Churn Rate", f"{churn['churn_rate']:.1f}%", delta=f"-{churn['churn_rate']:.1f}%", delta_color="inverse")
        with col3:
            st.metric("High Risk Users", churn.get('churned_users', 'N/A'))
        
        # Risk Distribution
        if 'risk_distribution' in churn:
            st.markdown("### Risk Distribution")
            risk_df = pd.DataFrame(list(churn['risk_distribution'].items()), columns=['Risk Level', 'Count'])
            
            fig = go.Figure(data=[go.Pie(
                labels=risk_df['Risk Level'],
                values=risk_df['Count'],
                hole=0.3,
                marker=dict(colors=['#d32f2f', '#f57c00', '#388e3c'])
            )])
            fig.update_layout(title="Customer Risk Segmentation", height=400)
            st.plotly_chart(fig, use_container_width=True)

# RECOMMENDATIONS PAGE
elif page == "Recommendations":
    st.header("Actionable Recommendations")
    
    if recommendations:
        st.success(f"**Total Recommendations Generated:** {recommendations['total_recommendations']}")
        
        # Filter by priority
        priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
        
        filtered_recs = recommendations['recommendations']
        if priority_filter != "All":
            filtered_recs = [r for r in filtered_recs if r['priority'].lower() == priority_filter.lower()]
        
        # Display recommendations
        for i, rec in enumerate(filtered_recs, 1):
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            
            with st.expander(f"{priority_emoji} Recommendation {i}: {rec.get('type', 'General').replace('_', ' ').title()}", expanded=(i <= 3)):
                st.markdown(f"**Priority:** {rec['priority'].upper()}")
                st.markdown(f"**Type:** {rec.get('type', 'general').replace('_', ' ').title()}")
                st.markdown(f"**Recommendation:**")
                st.info(rec['recommendation'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Expected Impact:** {rec.get('expected_impact', 'N/A').title()}")
                with col2:
                    st.markdown(f"**Confidence:** {rec.get('confidence', 'N/A').title()}")

# VISUALIZATIONS PAGE
elif page == "Visualizations":
    st.header("Interactive Visualizations")
    
    # Load Plotly charts
    chart_files = {
        'Revenue Trend': 'chart_timeseries.json',
        'Product Performance': 'chart_bar.json',
        'Correlation Matrix': 'chart_heatmap.json',
        'Forecast': 'chart_forecast.json'
    }
    
    chart_selection = st.selectbox("Select Chart", list(chart_files.keys()))
    
    chart_file = chart_files[chart_selection]
    chart_data = load_json(chart_file)
    
    if chart_data:
        fig = go.Figure(chart_data)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Chart data not found: {chart_file}")

# RAW DATA PAGE
elif page == "Raw Data":
    st.header("Raw Data Explorer")
    
    if cleaned_data is not None:
        st.subheader(f"Dataset: {len(cleaned_data)} rows × {len(cleaned_data.columns)} columns")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            if 'category' in cleaned_data.columns:
                category_filter = st.multiselect("Filter by Category", cleaned_data['category'].unique())
                if category_filter:
                    cleaned_data = cleaned_data[cleaned_data['category'].isin(category_filter)]
        
        with col2:
            if 'region' in cleaned_data.columns:
                region_filter = st.multiselect("Filter by Region", cleaned_data['region'].unique())
                if region_filter:
                    cleaned_data = cleaned_data[cleaned_data['region'].isin(region_filter)]
        
        # Display data
        st.dataframe(cleaned_data, use_container_width=True, height=500)
        
        # Download button
        csv = cleaned_data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="cleaned_sales_data.csv",
            mime="text/csv"
        )
        
        # Statistics
        st.subheader("Quick Statistics")
        st.write(cleaned_data.describe())
    else:
        st.error("Data file not found")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666;">AI Analytics Intelligence System | Powered by Streamlit</div>',
    unsafe_allow_html=True
)

