"""
ADVANCED AI-POWERED Analytics Dashboard - Feature #3
Advanced Analytics: Cohort Analysis, A/B Testing, Comparative Analysis
Run: streamlit run dashboard_advanced_3.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from datetime import datetime, timedelta
import scipy.stats as stats
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard - Advanced Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'cohort_data' not in st.session_state:
    st.session_state.cohort_data = None
if 'ab_test_data' not in st.session_state:
    st.session_state.ab_test_data = None

# Advanced Analytics Functions
class AdvancedAnalytics:
    def __init__(self):
        self.data = None
    
    def load_data(self, df):
        """Load data for analysis"""
        self.data = df
    
    def cohort_analysis(self, user_col, date_col, metric_col):
        """Perform cohort analysis"""
        if self.data is None:
            return None
        
        try:
            # Prepare data
            df = self.data.copy()
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Create cohort groups (monthly cohorts)
            df['cohort_month'] = df[date_col].dt.to_period('M')
            df['order_month'] = df[date_col].dt.to_period('M')
            
            # Create cohort table
            cohort_data = df.groupby([user_col, 'cohort_month'])[metric_col].sum().reset_index()
            cohort_table = cohort_data.groupby('cohort_month')[user_col].nunique()
            
            # Calculate retention
            cohort_sizes = cohort_table.values
            retention_matrix = []
            
            for i, cohort in enumerate(cohort_table.index):
                cohort_users = cohort_data[cohort_data['cohort_month'] == cohort][user_col].unique()
                retention_row = []
                
                for j in range(len(cohort_table)):
                    if j >= i:
                        period_users = cohort_data[cohort_data['order_month'] == cohort_table.index[j]][user_col].unique()
                        retention = len(set(cohort_users) & set(period_users)) / len(cohort_users) * 100
                        retention_row.append(retention)
                    else:
                        retention_row.append(0)
                
                retention_matrix.append(retention_row)
            
            return {
                'cohort_table': cohort_table,
                'retention_matrix': retention_matrix,
                'cohort_sizes': cohort_sizes
            }
        except Exception as e:
            st.error(f"Cohort analysis error: {e}")
            return None
    
    def ab_test_analysis(self, group_col, metric_col, alpha=0.05):
        """Perform A/B test analysis"""
        if self.data is None:
            return None
        
        try:
            df = self.data.copy()
            groups = df[group_col].unique()
            
            if len(groups) != 2:
                st.error("A/B test requires exactly 2 groups")
                return None
            
            group_a = df[df[group_col] == groups[0]][metric_col]
            group_b = df[df[group_col] == groups[1]][metric_col]
            
            # Calculate statistics
            mean_a = group_a.mean()
            mean_b = group_b.mean()
            std_a = group_a.std()
            std_b = group_b.std()
            n_a = len(group_a)
            n_b = len(group_b)
            
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(group_a, group_b)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
            cohens_d = (mean_a - mean_b) / pooled_std
            
            # Determine significance
            is_significant = p_value < alpha
            
            return {
                'group_a': {
                    'name': groups[0],
                    'mean': mean_a,
                    'std': std_a,
                    'n': n_a
                },
                'group_b': {
                    'name': groups[1],
                    'mean': mean_b,
                    'std': std_b,
                    'n': n_b
                },
                't_statistic': t_stat,
                'p_value': p_value,
                'cohens_d': cohens_d,
                'is_significant': is_significant,
                'alpha': alpha
            }
        except Exception as e:
            st.error(f"A/B test error: {e}")
            return None
    
    def comparative_analysis(self, date_col, metric_col, periods=2):
        """Perform period-over-period comparison"""
        if self.data is None:
            return None
        
        try:
            df = self.data.copy()
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Split data into periods
            df['period'] = pd.cut(df[date_col], periods, labels=[f'Period {i+1}' for i in range(periods)])
            
            period_stats = []
            for period in df['period'].unique():
                period_data = df[df['period'] == period][metric_col]
                stats_dict = {
                    'period': period,
                    'mean': period_data.mean(),
                    'median': period_data.median(),
                    'std': period_data.std(),
                    'count': len(period_data),
                    'sum': period_data.sum()
                }
                period_stats.append(stats_dict)
            
            # Calculate growth rates
            if len(period_stats) >= 2:
                growth_rate = ((period_stats[1]['mean'] - period_stats[0]['mean']) / period_stats[0]['mean']) * 100
            else:
                growth_rate = 0
            
            return {
                'period_stats': period_stats,
                'growth_rate': growth_rate
            }
        except Exception as e:
            st.error(f"Comparative analysis error: {e}")
            return None

# Initialize advanced analytics
advanced_analytics = AdvancedAnalytics()

# Theme CSS
def get_theme_css(theme):
    if theme == 'dark':
        return """
        <style>
            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #00d4ff;
                text-align: center;
                padding: 1rem;
                background: linear-gradient(90deg, #00d4ff 0%, #0099cc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .analytics-card {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            .metric-highlight {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
            }
        </style>
        """
    else:  # light theme
        return """
        <style>
            .stApp {
                background-color: #ffffff;
                color: #262730;
            }
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1f4788;
                text-align: center;
                padding: 1rem;
                background: linear-gradient(90deg, #1f4788 0%, #2196F3 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .analytics-card {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #262730;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #dee2e6;
            }
            .metric-highlight {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
            }
        </style>
        """

# Apply theme
st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📊 AI Analytics Dashboard - Advanced Analytics</div>', unsafe_allow_html=True)
st.markdown("**Cohort Analysis • A/B Testing • Comparative Analysis • Scenario Planning**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Advanced Analytics")
    
    # Theme toggle
    st.header("🎨 Settings")
    theme = st.selectbox(
        "Theme",
        ["light", "dark"],
        index=0 if st.session_state.get('theme', 'light') == 'light' else 1,
        help="Choose your preferred theme"
    )
    if theme != st.session_state.get('theme', 'light'):
        st.session_state.theme = theme
        st.rerun()
    
    st.markdown("---")
    
    # File Upload
    st.header("📁 Upload Data")
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload your data file for advanced analytics"
    )
    
    if uploaded_file is not None:
        try:
            # Parse CSV
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.session_state.uploaded_filename = uploaded_file.name
            advanced_analytics.load_data(df)
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.info(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            # Show preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())
            
            # Show columns
            with st.expander("📋 Columns"):
                for col in df.columns:
                    st.write(f"• {col} ({df[col].dtype})")
                    
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")

# Main content
if st.session_state.uploaded_data is not None:
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Cohort Analysis", "🧪 A/B Testing", "📊 Comparative Analysis", "🎯 Scenario Planning"])
    
    with tab1:
        st.header("📈 Cohort Analysis")
        st.markdown("Analyze customer behavior and retention over time")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            user_col = st.selectbox("User ID Column", st.session_state.uploaded_data.columns, key="cohort_user")
        with col2:
            date_col = st.selectbox("Date Column", st.session_state.uploaded_data.columns, key="cohort_date")
        with col3:
            metric_col = st.selectbox("Metric Column", st.session_state.uploaded_data.columns, key="cohort_metric")
        
        if st.button("🔍 Run Cohort Analysis", type="primary"):
            with st.spinner("Analyzing cohorts..."):
                cohort_results = advanced_analytics.cohort_analysis(user_col, date_col, metric_col)
                
                if cohort_results:
                    st.session_state.cohort_data = cohort_results
                    
                    # Display results
                    st.success("✅ Cohort analysis completed!")
                    
                    # Cohort size chart
                    fig_cohort = px.bar(
                        x=cohort_results['cohort_table'].index.astype(str),
                        y=cohort_results['cohort_sizes'],
                        title="Cohort Sizes by Month",
                        labels={'x': 'Cohort Month', 'y': 'Number of Users'}
                    )
                    st.plotly_chart(fig_cohort, use_container_width=True)
                    
                    # Retention heatmap
                    retention_df = pd.DataFrame(
                        cohort_results['retention_matrix'],
                        index=cohort_results['cohort_table'].index.astype(str),
                        columns=[f"Month {i+1}" for i in range(len(cohort_results['retention_matrix'][0]))]
                    )
                    
                    fig_heatmap = px.imshow(
                        retention_df,
                        title="Customer Retention Heatmap (%)",
                        color_continuous_scale="RdYlGn"
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab2:
        st.header("🧪 A/B Testing")
        st.markdown("Compare two groups with statistical significance testing")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            group_col = st.selectbox("Group Column", st.session_state.uploaded_data.columns, key="ab_group")
        with col2:
            metric_col = st.selectbox("Metric Column", st.session_state.uploaded_data.columns, key="ab_metric")
        with col3:
            alpha = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01, key="ab_alpha")
        
        if st.button("🧪 Run A/B Test", type="primary"):
            with st.spinner("Running A/B test..."):
                ab_results = advanced_analytics.ab_test_analysis(group_col, metric_col, alpha)
                
                if ab_results:
                    st.session_state.ab_test_data = ab_results
                    
                    # Display results
                    st.success("✅ A/B test completed!")
                    
                    # Results summary
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f'''
                        <div class="analytics-card">
                            <h3>📊 Group A: {ab_results['group_a']['name']}</h3>
                            <p><strong>Mean:</strong> {ab_results['group_a']['mean']:.2f}</p>
                            <p><strong>Std Dev:</strong> {ab_results['group_a']['std']:.2f}</p>
                            <p><strong>Sample Size:</strong> {ab_results['group_a']['n']:,}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f'''
                        <div class="analytics-card">
                            <h3>📊 Group B: {ab_results['group_b']['name']}</h3>
                            <p><strong>Mean:</strong> {ab_results['group_b']['mean']:.2f}</p>
                            <p><strong>Std Dev:</strong> {ab_results['group_b']['std']:.2f}</p>
                            <p><strong>Sample Size:</strong> {ab_results['group_b']['n']:,}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    # Statistical results
                    st.markdown(f'''
                    <div class="analytics-card">
                        <h3>📈 Statistical Results</h3>
                        <p><strong>P-value:</strong> {ab_results['p_value']:.4f}</p>
                        <p><strong>Effect Size (Cohen's d):</strong> {ab_results['cohens_d']:.3f}</p>
                        <p><strong>Significant:</strong> {"✅ Yes" if ab_results['is_significant'] else "❌ No"}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Visualization
                    groups_data = [ab_results['group_a']['mean'], ab_results['group_b']['mean']]
                    groups_labels = [ab_results['group_a']['name'], ab_results['group_b']['name']]
                    
                    fig_ab = px.bar(
                        x=groups_labels,
                        y=groups_data,
                        title="A/B Test Results Comparison",
                        labels={'x': 'Groups', 'y': 'Mean Value'}
                    )
                    st.plotly_chart(fig_ab, use_container_width=True)
    
    with tab3:
        st.header("📊 Comparative Analysis")
        st.markdown("Period-over-period comparison and growth analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_col = st.selectbox("Date Column", st.session_state.uploaded_data.columns, key="comp_date")
        with col2:
            metric_col = st.selectbox("Metric Column", st.session_state.uploaded_data.columns, key="comp_metric")
        with col3:
            periods = st.slider("Number of Periods", 2, 12, 2, key="comp_periods")
        
        if st.button("📊 Run Comparative Analysis", type="primary"):
            with st.spinner("Analyzing periods..."):
                comp_results = advanced_analytics.comparative_analysis(date_col, metric_col, periods)
                
                if comp_results:
                    # Display results
                    st.success("✅ Comparative analysis completed!")
                    
                    # Period comparison
                    period_data = []
                    for stat in comp_results['period_stats']:
                        period_data.append({
                            'Period': stat['period'],
                            'Mean': stat['mean'],
                            'Median': stat['median'],
                            'Count': stat['count'],
                            'Sum': stat['sum']
                        })
                    
                    period_df = pd.DataFrame(period_data)
                    st.dataframe(period_df, use_container_width=True)
                    
                    # Growth rate
                    growth_color = "green" if comp_results['growth_rate'] > 0 else "red"
                    st.markdown(f'''
                    <div class="metric-highlight" style="background: {growth_color};">
                        📈 Growth Rate: {comp_results['growth_rate']:.2f}%
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Visualization
                    fig_comp = px.bar(
                        period_df,
                        x='Period',
                        y='Mean',
                        title="Period-over-Period Comparison",
                        labels={'Mean': 'Average Value'}
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
    
    with tab4:
        st.header("🎯 Scenario Planning")
        st.markdown("What-if analysis and forecasting scenarios")
        
        st.info("🚧 Scenario Planning feature coming soon!")
        st.markdown("""
        **Planned Features:**
        - What-if analysis tools
        - Forecasting scenarios
        - Sensitivity analysis
        - Monte Carlo simulations
        - Risk assessment
        """)

else:
    st.markdown("""
    <div class="analytics-card">
        <h3>🚀 Get Started with Advanced Analytics</h3>
        <p>Upload a CSV file to access:</p>
        <ul>
            <li>📈 <strong>Cohort Analysis</strong> - Customer retention and behavior</li>
            <li>🧪 <strong>A/B Testing</strong> - Statistical significance testing</li>
            <li>📊 <strong>Comparative Analysis</strong> - Period-over-period comparisons</li>
            <li>🎯 <strong>Scenario Planning</strong> - What-if analysis (coming soon)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 AI Analytics Intelligence System - Advanced Analytics Edition</p>
    <p>💡 Professional-grade analytics with statistical rigor!</p>
</div>
""", unsafe_allow_html=True)
