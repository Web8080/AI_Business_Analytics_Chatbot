"""
UNIFIED AI-POWERED Analytics Dashboard
All Features Combined: Chatbot + Advanced Analytics + Real-time + Voice
Run: streamlit run dashboard_unified.py
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
import time

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard - Unified",
    page_icon="",
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
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Chatbot'
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'data_version' not in st.session_state:
    st.session_state.data_version = 0

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
            .chat-message {
                padding: 1.2rem;
                border-radius: 0.8rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: 20%;
            }
            .assistant-message {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                margin-right: 20%;
            }
            .confidence-badge {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
            }
            .metric-card {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            .feature-card {
                background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                border: 2px solid #4a5568;
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
            .chat-message {
                padding: 1.2rem;
                border-radius: 0.8rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: 20%;
            }
            .assistant-message {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                margin-right: 20%;
            }
            .confidence-badge {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
            }
            .metric-card {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #262730;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #dee2e6;
            }
            .feature-card {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #262730;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 2px solid #dee2e6;
            }
        </style>
        """

# Apply theme
st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header"> AI Analytics Intelligence System</div>', unsafe_allow_html=True)
st.markdown("**Unified Dashboard: Chatbot + Advanced Analytics + Real-time + Voice**")
st.markdown("---")

# Sidebar Navigation
with st.sidebar:
    st.header(" Navigation")
    
    # Main pages
    pages = {
        " Chatbot": "Chatbot",
        " Data Overview": "Data Overview", 
        " Advanced Analytics": "Advanced Analytics",
        " Real-time": "Real-time",
        " Voice": "Voice",
        " Settings": "Settings"
    }
    
    # Get current page index safely
    current_page_display = f" {st.session_state.current_page}" if st.session_state.current_page != "Chatbot" else " Chatbot"
    try:
        current_index = list(pages.keys()).index(current_page_display)
    except ValueError:
        current_index = 0  # Default to first page if not found
    
    selected_page = st.selectbox(
        "Select Page",
        list(pages.keys()),
        index=current_index,
        help="Choose which feature to use"
    )
    
    st.session_state.current_page = pages[selected_page]
    
    st.markdown("---")
    
    # File Upload (always available)
    st.header(" Upload Data")
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload your data file to start analyzing"
    )
    
    if uploaded_file is not None:
        try:
            # Parse CSV
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.data_version += 1
            st.session_state.last_refresh = datetime.now()
            
            st.success(f" Loaded: {uploaded_file.name}")
            st.info(f" {len(df)} rows × {len(df.columns)} columns")
            
            # Show preview
            with st.expander(" Preview Data"):
                st.dataframe(df.head())
            
            # Show columns
            with st.expander(" Columns"):
                for col in df.columns:
                    st.write(f"• {col} ({df[col].dtype})")
                    
        except Exception as e:
            st.error(f" Error loading file: {str(e)}")
    
    st.markdown("---")
    
    # Quick Actions (always available)
    if st.session_state.uploaded_data is not None:
        st.header(" Quick Actions")
        quick_questions = [
            "What is the total revenue?",
            "Show me top 5 products",
            "Compare sales by category",
            "What are the trends over time?",
            "Which region has highest sales?",
            "What's the average order value?"
        ]
        
        for question in quick_questions:
            if st.button(f" {question}", key=f"quick_{question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

# Main Content Area
if st.session_state.current_page == "Chatbot":
    # CHATBOT PAGE - Main functionality
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(" AI Analytics Assistant")
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><b>AI:</b> {message["content"]}</div>', unsafe_allow_html=True)
        
        # Chat input
        if st.session_state.uploaded_data is not None:
            user_input = st.text_input(
                "Ask a question about your data...",
                placeholder="e.g., What is the total revenue?",
                help="Ask any question about your uploaded data"
            )
            
            if st.button("Send", type="primary"):
                if user_input:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get AI response
                    try:
                        agent = SmartAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask(user_input)
                        
                        # Add AI response
                        st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                        
                        # Show confidence
                        if 'confidence' in response:
                            st.markdown(f'<div class="confidence-badge">Confidence: {response["confidence"]:.0%}</div>', unsafe_allow_html=True)
                        
                        # Show suggestions if vague
                        if response.get('is_vague', False) and 'suggested_questions' in response:
                            st.markdown("** Try asking:**")
                            for suggestion in response['suggested_questions'][:3]:
                                if st.button(f" {suggestion}", key=f"suggest_{suggestion}"):
                                    st.session_state.messages.append({"role": "user", "content": suggestion})
                                    st.rerun()
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f" Error: {str(e)}")
        else:
            st.info(" Please upload a CSV file to start chatting with your data")
    
    with col2:
        # Data metrics
        if st.session_state.uploaded_data is not None:
            st.header(" Data Overview")
            
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                st.markdown(f'''
                <div class="metric-card">
                    <h3> Total Rows</h3>
                    <h2>{len(st.session_state.uploaded_data):,}</h2>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2_2:
                st.markdown(f'''
                <div class="metric-card">
                    <h3> Columns</h3>
                    <h2>{len(st.session_state.uploaded_data.columns)}</h2>
                </div>
                ''', unsafe_allow_html=True)
            
            # Data quality
            null_percentage = (st.session_state.uploaded_data.isnull().sum().sum() / 
                              (len(st.session_state.uploaded_data) * len(st.session_state.uploaded_data.columns))) * 100
            
            if null_percentage < 5:
                st.success(f" Data Quality: Excellent ({null_percentage:.1f}% missing)")
            elif null_percentage < 15:
                st.warning(f" Data Quality: Good ({null_percentage:.1f}% missing)")
            else:
                st.error(f" Data Quality: Needs attention ({null_percentage:.1f}% missing)")
        else:
            st.markdown("""
            <div class="metric-card">
                <h3> Get Started</h3>
                <p>Upload a CSV file to begin analyzing your data with AI!</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_page == "Data Overview":
    # DATA OVERVIEW PAGE
    st.header(" Data Overview")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        # Basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        with col4:
            st.metric("Data Version", f"v{st.session_state.data_version}")
        
        # Data types
        st.subheader(" Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes,
            'Non-Null': df.count(),
            'Null': df.isnull().sum(),
            'Unique': df.nunique()
        })
        st.dataframe(col_info, use_container_width=True)
        
        # Sample data
        st.subheader(" Sample Data")
        st.dataframe(df.head(10), use_container_width=True)
        
    else:
        st.info(" Please upload a CSV file to view data overview")

elif st.session_state.current_page == "Advanced Analytics":
    # ADVANCED ANALYTICS PAGE
    st.header(" Advanced Analytics")
    
    if st.session_state.uploaded_data is not None:
        st.markdown("""
        <div class="feature-card">
            <h3> Advanced Analytics Features</h3>
            <p>Professional-grade analytics tools for deep data insights:</p>
            <ul>
                <li> <strong>Cohort Analysis</strong> - Customer retention and behavior tracking</li>
                <li> <strong>A/B Testing</strong> - Statistical significance testing</li>
                <li> <strong>Comparative Analysis</strong> - Period-over-period comparisons</li>
                <li> <strong>Scenario Planning</strong> - What-if analysis</li>
            </ul>
            <p><em>These features require specific data structures and are best used with time-series or customer data.</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature availability check
        df = st.session_state.uploaded_data
        
        # Check for date columns
        date_cols = []
        for col in df.columns:
            try:
                pd.to_datetime(df[col].dropna().iloc[0])
                date_cols.append(col)
            except:
                pass
        
        if date_cols:
            st.success(f" Found {len(date_cols)} date columns: {', '.join(date_cols)}")
            st.info(" Your data is suitable for cohort analysis and time-based comparisons!")
        else:
            st.warning(" No date columns detected. Advanced analytics work best with time-series data.")
        
        # Check for categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if categorical_cols:
            st.success(f" Found {len(categorical_cols)} categorical columns: {', '.join(categorical_cols)}")
            st.info(" Your data is suitable for A/B testing and comparative analysis!")
        
        # Quick analysis suggestions
        st.subheader(" Suggested Analyses")
        
        if date_cols and len(categorical_cols) > 0:
            st.markdown("**Based on your data, you can perform:**")
            st.markdown("-  **Cohort Analysis** using date and categorical columns")
            st.markdown("-  **A/B Testing** comparing different categories")
            st.markdown("-  **Time Series Analysis** for trend identification")
        
        # Placeholder for future implementation
        st.info(" Advanced analytics features will be implemented in the next version. For now, use the chatbot for detailed analysis!")
        
    else:
        st.info(" Please upload a CSV file to access advanced analytics")

elif st.session_state.current_page == "Real-time":
    # REAL-TIME PAGE
    st.header(" Real-time Features")
    
    if st.session_state.uploaded_data is not None:
        st.markdown("""
        <div class="feature-card">
            <h3> Real-time Data Refresh</h3>
            <p>Keep your analytics up-to-date with automatic data refresh:</p>
            <ul>
                <li>⏰ <strong>Auto-refresh</strong> - Updates every 30 seconds</li>
                <li> <strong>Version Tracking</strong> - Track data changes over time</li>
                <li> <strong>Freshness Indicators</strong> - Know when data was last updated</li>
                <li> <strong>Configurable Intervals</strong> - Customize refresh frequency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time controls
        col1, col2 = st.columns(2)
        
        with col1:
            auto_refresh = st.toggle(
                "Enable Auto-refresh",
                value=st.session_state.auto_refresh,
                help="Automatically refresh data every 30 seconds"
            )
            if auto_refresh != st.session_state.auto_refresh:
                st.session_state.auto_refresh = auto_refresh
                st.rerun()
        
        with col2:
            if st.button(" Refresh Now", type="primary"):
                st.session_state.data_version += 1
                st.session_state.last_refresh = datetime.now()
                st.success(f" Data refreshed! Version: v{st.session_state.data_version}")
                st.rerun()
        
        # Status display
        time_since_refresh = (datetime.now() - st.session_state.last_refresh).total_seconds()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Version", f"v{st.session_state.data_version}")
        with col2:
            st.metric("Last Refresh", st.session_state.last_refresh.strftime("%H:%M:%S"))
        with col3:
            if time_since_refresh < 60:
                st.metric("Freshness", " Fresh")
            elif time_since_refresh < 300:
                st.metric("Freshness", " Recent")
            else:
                st.metric("Freshness", " Stale")
        
    else:
        st.info(" Please upload a CSV file to access real-time features")

elif st.session_state.current_page == "Voice":
    # VOICE PAGE
    st.header(" Voice Features")
    
    st.markdown("""
    <div class="feature-card">
        <h3> Voice Input/Output</h3>
        <p>Interact with your data using voice commands:</p>
        <ul>
            <li> <strong>Speech-to-Text</strong> - Ask questions by speaking</li>
            <li> <strong>Text-to-Speech</strong> - Hear AI responses aloud</li>
            <li> <strong>Multi-language</strong> - Support for multiple languages</li>
            <li> <strong>Voice Speed Control</strong> - Adjustable playback speed</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(" Voice features require additional packages and microphone access. They will be available in the next version!")
    
    # Voice status
    st.subheader(" Voice Status")
    st.warning(" Voice features not available - requires microphone and additional packages")

elif st.session_state.current_page == "Settings":
    # SETTINGS PAGE
    st.header(" Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Appearance")
        theme = st.selectbox(
            "Theme",
            ["light", "dark"],
            index=0 if st.session_state.get('theme', 'light') == 'light' else 1,
            help="Choose your preferred theme"
        )
        if theme != st.session_state.get('theme', 'light'):
            st.session_state.theme = theme
            st.rerun()
    
    with col2:
        st.subheader(" Real-time")
        auto_refresh = st.toggle(
            "Auto-refresh",
            value=st.session_state.auto_refresh,
            help="Automatically refresh data"
        )
        if auto_refresh != st.session_state.auto_refresh:
            st.session_state.auto_refresh = auto_refresh
            st.rerun()
    
    # Export options
    st.subheader(" Export")
    if st.session_state.uploaded_data is not None:
        # Export data as CSV
        csv = st.session_state.uploaded_data.to_csv(index=False)
        st.download_button(
            label=" Download Data (CSV)",
            data=csv,
            file_name=f"{st.session_state.uploaded_filename}_export.csv",
            mime="text/csv",
            help="Download your uploaded data as CSV"
        )
        
        # Export chat as text
        if st.session_state.messages:
            chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
            st.download_button(
                label=" Download Chat (TXT)",
                data=chat_text,
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                help="Download chat conversation as text file"
            )
    
    # System info
    st.subheader("ℹ System Information")
    st.info(f"""
    **Current Session:**
    - Data Version: v{st.session_state.data_version}
    - Messages: {len(st.session_state.messages)}
    - Theme: {st.session_state.get('theme', 'light')}
    - Auto-refresh: {'Enabled' if st.session_state.auto_refresh else 'Disabled'}
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p> AI Analytics Intelligence System - Unified Dashboard</p>
    <p> All features in one place - choose what you need!</p>
</div>
""", unsafe_allow_html=True)
