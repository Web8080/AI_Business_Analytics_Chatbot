"""
ADVANCED AI-POWERED Analytics Dashboard - Feature #1
Real-time Data Refresh with Auto-updates every 30 seconds
Run: streamlit run dashboard_advanced_1.py
"""
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from pathlib import Path
import sys
import io
import base64
from datetime import datetime, timedelta
import time
import threading
import queue

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard - Real-time",
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
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30  # seconds
if 'data_version' not in st.session_state:
    st.session_state.data_version = 0

# Real-time refresh functionality
def check_for_data_updates():
    """Check if data has been updated and refresh if needed"""
    if st.session_state.uploaded_data is not None:
        # Simulate data updates (in real app, this would check file timestamps, database changes, etc.)
        current_time = datetime.now()
        time_since_refresh = (current_time - st.session_state.last_refresh).total_seconds()
        
        if time_since_refresh >= st.session_state.refresh_interval and st.session_state.auto_refresh:
            # Simulate data change (in real app, reload from source)
            st.session_state.data_version += 1
            st.session_state.last_refresh = current_time
            
            # Add a notification message
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f" **Data refreshed automatically** (v{st.session_state.data_version}) - {current_time.strftime('%H:%M:%S')}"
            })
            return True
    return False

# Theme CSS (same as before)
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
            .refresh-indicator {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }
            .metric-card {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 1rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
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
            .refresh-indicator {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
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
        </style>
        """

# Apply theme
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Title with real-time indicator
st.markdown('<div class="main-header"> AI Analytics Dashboard - Real-time</div>', unsafe_allow_html=True)
st.markdown("Ask questions, get instant analytics with **auto-refreshing data**")
st.markdown("---")

# Real-time status bar
col_status1, col_status2, col_status3 = st.columns([2, 1, 1])

with col_status1:
    if st.session_state.auto_refresh:
        next_refresh = st.session_state.last_refresh + timedelta(seconds=st.session_state.refresh_interval)
        time_until_refresh = (next_refresh - datetime.now()).total_seconds()
        if time_until_refresh > 0:
            st.markdown(f'<div class="refresh-indicator"> Auto-refresh in {int(time_until_refresh)}s</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="refresh-indicator"> Refreshing...</div>', unsafe_allow_html=True)

with col_status2:
    st.metric("Data Version", f"v{st.session_state.data_version}")

with col_status3:
    st.metric("Last Refresh", st.session_state.last_refresh.strftime("%H:%M:%S"))

# Check for updates
if check_for_data_updates():
    st.rerun()

# Sidebar with Real-time Controls
with st.sidebar:
    st.header(" Real-time Settings")
    
    # Auto-refresh toggle
    auto_refresh = st.toggle(
        "Auto-refresh",
        value=st.session_state.auto_refresh,
        help="Automatically refresh data every 30 seconds"
    )
    if auto_refresh != st.session_state.auto_refresh:
        st.session_state.auto_refresh = auto_refresh
        st.rerun()
    
    # Refresh interval
    refresh_interval = st.slider(
        "Refresh Interval (seconds)",
        min_value=10,
        max_value=300,
        value=st.session_state.refresh_interval,
        step=10,
        help="How often to refresh data automatically"
    )
    if refresh_interval != st.session_state.refresh_interval:
        st.session_state.refresh_interval = refresh_interval
        st.rerun()
    
    # Manual refresh button
    if st.button(" Refresh Now", type="primary"):
        st.session_state.data_version += 1
        st.session_state.last_refresh = datetime.now()
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f" **Manual refresh completed** (v{st.session_state.data_version}) - {datetime.now().strftime('%H:%M:%S')}"
        })
        st.rerun()
    
    st.markdown("---")
    
    # Theme toggle
    st.header(" Settings")
    theme = st.selectbox(
        "Theme",
        ["light", "dark"],
        index=0 if st.session_state.get('theme', 'light') == 'light' else 1,
        help="Choose your preferred theme"
    )
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.markdown("---")
    
    # Quick Actions
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
    
    st.markdown("---")
    
    # File Upload
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

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
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
        
        if st.button("Send", type="primary") or user_input:
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
                        st.markdown(f'<div class="refresh-indicator">Confidence: {response["confidence"]:.0%}</div>', unsafe_allow_html=True)
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f" Error: {str(e)}")
    else:
        st.info(" Please upload a CSV file to start chatting with your data")

with col2:
    # Real-time metrics
    if st.session_state.uploaded_data is not None:
        st.header(" Real-time Metrics")
        
        # Data freshness indicator
        time_since_refresh = (datetime.now() - st.session_state.last_refresh).total_seconds()
        if time_since_refresh < 60:
            freshness = " Fresh"
        elif time_since_refresh < 300:
            freshness = " Recent"
        else:
            freshness = " Stale"
        
        st.markdown(f'''
        <div class="metric-card">
            <h3> Data Freshness</h3>
            <h2>{freshness}</h2>
            <p>Updated {int(time_since_refresh)}s ago</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Basic metrics
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
        
        # Auto-refresh status
        if st.session_state.auto_refresh:
            st.success(" Auto-refresh enabled")
        else:
            st.warning("⏸ Auto-refresh disabled")
    
    else:
        st.markdown("""
        <div class="metric-card">
            <h3> Get Started</h3>
            <p>Upload a CSV file to begin real-time analytics!</p>
        </div>
        """, unsafe_allow_html=True)

# Auto-refresh mechanism
if st.session_state.auto_refresh:
    # Use st.empty() to create a placeholder for auto-refresh
    placeholder = st.empty()
    
    # Check if it's time to refresh
    current_time = datetime.now()
    time_since_refresh = (current_time - st.session_state.last_refresh).total_seconds()
    
    if time_since_refresh >= st.session_state.refresh_interval:
        # Trigger refresh
        st.session_state.data_version += 1
        st.session_state.last_refresh = current_time
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f" **Auto-refresh completed** (v{st.session_state.data_version}) - {current_time.strftime('%H:%M:%S')}"
        })
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p> AI Analytics Intelligence System - Real-time Edition</p>
    <p> Data refreshes automatically every {st.session_state.refresh_interval} seconds!</p>
</div>
""", unsafe_allow_html=True)
