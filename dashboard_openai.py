"""
OpenAI-Powered Analytics Dashboard
Integrates GPT-4 with intelligent fallback system
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
from datetime import datetime
import json
import os

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.openai_agent import OpenAIAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Intelligence System - OpenAI Powered",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state - CRITICAL for state sharing
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'messages': [],
        'message_charts': {},
        'uploaded_data': None,
        'uploaded_filename': None,
        'theme': 'dark',
        'current_page': 'Chatbot',
        'chat_input': '',
        'file_uploaded': False,
        'openai_status': 'checking'
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Initialize session state
init_session_state()

# Professional CSS
def get_theme_css(theme):
    if theme == 'dark':
        return """
        <style>
            .stApp {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
                color: #ffffff !important;
            }
            
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                padding: 2rem !important;
                border-radius: 15px !important;
                margin-bottom: 2rem !important;
                text-align: center !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
                border: 2px solid #764ba2 !important;
            }
            
            .main-title {
                color: #ffffff !important;
                font-size: 2.5rem !important;
                font-weight: 700 !important;
                margin: 0 !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
            }
            
            .subtitle {
                color: #e0e0e0 !important;
                font-size: 1.2rem !important;
                margin: 0.5rem 0 0 0 !important;
                opacity: 0.9 !important;
            }
            
            .chat-container {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 15px !important;
                padding: 2rem !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
            }
            
            .chat-message {
                padding: 1rem !important;
                margin: 1rem 0 !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
            }
            
            .user-message {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
                color: #ffffff !important;
                margin-left: 2rem !important;
            }
            
            .assistant-message {
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
                color: #ffffff !important;
                margin-right: 2rem !important;
            }
            
            .sidebar-card {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 15px !important;
                padding: 1.5rem !important;
                margin: 1rem 0 !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            
            .status-indicator {
                display: inline-block !important;
                width: 12px !important;
                height: 12px !important;
                border-radius: 50% !important;
                margin-right: 8px !important;
            }
            
            .status-online {
                background-color: #4CAF50 !important;
                box-shadow: 0 0 10px rgba(76, 175, 80, 0.5) !important;
            }
            
            .status-offline {
                background-color: #f44336 !important;
                box-shadow: 0 0 10px rgba(244, 67, 54, 0.5) !important;
            }
            
            .stTextInput > div > div > input {
                background: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                color: #ffffff !important;
                border-radius: 10px !important;
                padding: 0.75rem !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #b0b0b0 !important;
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
            }
            
            .stSelectbox > div > div > select {
                background: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                color: #ffffff !important;
                border-radius: 10px !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background: rgba(255, 255, 255, 0.1) !important;
                border-radius: 10px !important;
                padding: 0.5rem !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent !important;
                color: #ffffff !important;
                border-radius: 8px !important;
                margin: 0.25rem !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
            }
            
            .stExpander {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 10px !important;
            }
            
            .stExpander > div > div > div {
                color: #ffffff !important;
            }
        </style>
        """
    else:
        return """
        <style>
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
                color: #333333 !important;
            }
            
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                padding: 2rem !important;
                border-radius: 15px !important;
                margin-bottom: 2rem !important;
                text-align: center !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
                border: 2px solid #764ba2 !important;
            }
            
            .main-title {
                color: #ffffff !important;
                font-size: 2.5rem !important;
                font-weight: 700 !important;
                margin: 0 !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
            }
            
            .subtitle {
                color: #e0e0e0 !important;
                font-size: 1.2rem !important;
                margin: 0.5rem 0 0 0 !important;
                opacity: 0.9 !important;
            }
            
            .chat-container {
                background: rgba(255, 255, 255, 0.9) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 15px !important;
                padding: 2rem !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
            }
            
            .chat-message {
                padding: 1rem !important;
                margin: 1rem 0 !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
            }
            
            .user-message {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
                color: #ffffff !important;
                margin-left: 2rem !important;
            }
            
            .assistant-message {
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%) !important;
                color: #ffffff !important;
                margin-right: 2rem !important;
            }
            
            .sidebar-card {
                background: rgba(255, 255, 255, 0.9) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 15px !important;
                padding: 1.5rem !important;
                margin: 1rem 0 !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            .status-indicator {
                display: inline-block !important;
                width: 12px !important;
                height: 12px !important;
                border-radius: 50% !important;
                margin-right: 8px !important;
            }
            
            .status-online {
                background-color: #4CAF50 !important;
                box-shadow: 0 0 10px rgba(76, 175, 80, 0.5) !important;
            }
            
            .status-offline {
                background-color: #f44336 !important;
                box-shadow: 0 0 10px rgba(244, 67, 54, 0.5) !important;
            }
            
            .stTextInput > div > div > input {
                background: rgba(255, 255, 255, 0.9) !important;
                border: 1px solid rgba(0, 0, 0, 0.2) !important;
                color: #333333 !important;
                border-radius: 10px !important;
                padding: 0.75rem !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #666666 !important;
            }
            
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
            }
            
            .stSelectbox > div > div > select {
                background: rgba(255, 255, 255, 0.9) !important;
                border: 1px solid rgba(0, 0, 0, 0.2) !important;
                color: #333333 !important;
                border-radius: 10px !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background: rgba(255, 255, 255, 0.9) !important;
                border-radius: 10px !important;
                padding: 0.5rem !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent !important;
                color: #333333 !important;
                border-radius: 8px !important;
                margin: 0.25rem !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
            }
            
            .stExpander {
                background: rgba(255, 255, 255, 0.8) !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                border-radius: 10px !important;
            }
            
            .stExpander > div > div > div {
                color: #333333 !important;
            }
        </style>
        """

# Apply CSS
st.markdown(get_theme_css(st.session_state.get('theme', 'dark')), unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">🚀 AI Analytics Intelligence System</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">OpenAI GPT-4 Powered Analytics Platform with Intelligent Fallback</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Chatbot", "📊 Data Overview", "🔧 Advanced Features", "⚙️ Settings"])

with tab1:
    # CHATBOT TAB - Main functionality
    
    # Show prominent welcome message if data is loaded but no messages yet
    if (st.session_state.get('uploaded_data') is not None and 
        st.session_state.get('file_uploaded', False) and 
        len(st.session_state.messages) == 0):
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                    border: 2px solid #764ba2; text-align: center;'>
            <h2 style='color: white; margin: 0;'>🚀 Data Loaded Successfully!</h2>
            <p style='color: white; margin: 1rem 0 0 0; font-size: 1.2rem;'>
                Ask me anything about your data and I'll provide instant insights with charts!
            </p>
            <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9;'>
                Try: "show me top 5 products" or "what is the total revenue?"
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.header("🤖 AI Analytics Assistant")
        
        # Display chat messages with charts
        for idx, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><b>AI:</b> {message["content"]}</div>', unsafe_allow_html=True)
                
                # Display chart if available
                if idx in st.session_state.message_charts:
                    try:
                        chart_data = st.session_state.message_charts[idx]
                        if chart_data:
                            # Handle different chart data formats
                            if 'data' in chart_data:
                                # Format from OpenAI agent with 'data' key
                                fig = go.Figure(chart_data['data'])
                            elif 'type' in chart_data and 'x' in chart_data and 'y' in chart_data:
                                # Format from smart agent with direct chart data
                                if chart_data['type'] == 'bar':
                                    fig = go.Figure(data=[
                                        go.Bar(
                                            x=chart_data['x'],
                                            y=chart_data['y'],
                                            name=chart_data.get('title', 'Chart')
                                        )
                                    ])
                                elif chart_data['type'] == 'line':
                                    fig = go.Figure(data=[
                                        go.Scatter(
                                            x=chart_data['x'],
                                            y=chart_data['y'],
                                            mode='lines',
                                            name=chart_data.get('title', 'Chart')
                                        )
                                    ])
                                elif chart_data['type'] == 'pie':
                                    fig = go.Figure(data=[
                                        go.Pie(
                                            labels=chart_data['x'],
                                            values=chart_data['y']
                                        )
                                    ])
                                else:
                                    fig = go.Figure()
                            else:
                                # Unknown format, skip
                                continue
                            
                            fig.update_layout(
                                template='plotly_dark', 
                                height=400,
                                title=chart_data.get('title', 'Chart')
                            )
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
                    except Exception as chart_error:
                        st.caption(f"⚠️ Chart display error: {str(chart_error)}")
                        # Debug: show chart data structure
                        st.caption(f"Chart data: {str(chart_data)[:200]}...")
        
        # Chat input with proper clearing
        if (st.session_state.get('uploaded_data') is not None and 
            st.session_state.get('file_uploaded', False)):
            # Use a form to handle input properly
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "Ask a question about your data...",
                    placeholder="e.g., What is the total revenue?",
                    help="Ask any question about your uploaded data",
                    key="chat_input_field"
                )
                
                col_send, col_clear = st.columns([1, 1])
                with col_send:
                    send_pressed = st.form_submit_button("🚀 Send", type="primary", use_container_width=True)
                with col_clear:
                    clear_pressed = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
            
            # Handle form submission
            if send_pressed and user_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get AI response
                try:
                    with st.spinner("🤖 AI is analyzing your data..."):
                        agent = OpenAIAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask(user_input)
                    
                    # Add AI response
                    message_idx = len(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
                    # Store chart data if exists
                    if 'chart_data' in response and response['chart_data']:
                        st.session_state.message_charts[message_idx] = response['chart_data']
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            if clear_pressed:
                st.session_state.messages = []
                st.session_state.message_charts = {}
                st.rerun()
                
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                        padding: 2rem; border-radius: 15px; margin: 2rem 0;
                        border: 2px solid #ee5a24; text-align: center;'>
                <h3 style='color: white; margin: 0;'>📁 No Data Uploaded</h3>
                <p style='color: white; margin: 1rem 0 0 0; font-size: 1.1rem;'>
                    Please upload a CSV file in the sidebar to start chatting with your data!
                </p>
                <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.9;'>
                    👈 Use the file uploader in the left sidebar
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Data metrics and quick actions
        if (st.session_state.get('uploaded_data') is not None and 
            st.session_state.get('file_uploaded', False)):
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            st.header("📊 Data Status")
            
            # Status indicator
            st.markdown('<span class="status-indicator status-online"></span> **System Online**', unsafe_allow_html=True)
            
            # File info
            st.subheader("📁 File Information")
            st.info(f"**File:** {st.session_state.uploaded_filename}")
            st.info(f"**Rows:** {len(st.session_state.uploaded_data)}")
            st.info(f"**Columns:** {len(st.session_state.uploaded_data.columns)}")
            
            # Quick actions
            st.subheader("⚡ Quick Actions")
            
            if st.button("📈 Show Data Summary", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Give me a summary of the data"})
                try:
                    with st.spinner("🤖 Analyzing..."):
                        agent = OpenAIAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask("Give me a summary of the data")
                    
                    message_idx = len(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
                    if 'chart_data' in response and response['chart_data']:
                        st.session_state.message_charts[message_idx] = response['chart_data']
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            if st.button("📊 Show Top Items", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Show me the top 5 items"})
                try:
                    with st.spinner("🤖 Analyzing..."):
                        agent = OpenAIAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask("Show me the top 5 items")
                    
                    message_idx = len(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
                    if 'chart_data' in response and response['chart_data']:
                        st.session_state.message_charts[message_idx] = response['chart_data']
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            if st.button("📈 Show Trends", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Show me trends in the data"})
                try:
                    with st.spinner("🤖 Analyzing..."):
                        agent = OpenAIAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask("Show me trends in the data")
                    
                    message_idx = len(st.session_state.messages)
                    st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
                    if 'chart_data' in response and response['chart_data']:
                        st.session_state.message_charts[message_idx] = response['chart_data']
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    # DATA OVERVIEW TAB
    st.header("📊 Data Overview")
    
    if (st.session_state.get('uploaded_data') is not None and 
        st.session_state.get('file_uploaded', False)):
        
        df = st.session_state.uploaded_data
        
        # Basic statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Data types
        st.subheader("📋 Column Information")
        type_counts = df.dtypes.value_counts()
        type_labels = [str(dtype) for dtype in type_counts.index]
        
        fig = px.pie(
            values=type_counts.values,
            names=type_labels,
            title="Data Types Distribution",
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Missing values
        st.subheader("🔍 Missing Values")
        missing_data = df.isnull().sum()
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Missing Percentage': (missing_data.values / len(df)) * 100
        }).sort_values('Missing Count', ascending=False)
        
        st.dataframe(missing_df, use_container_width=True)
        
        # Sample data
        st.subheader("👀 Sample Data")
        st.dataframe(df.head(10), use_container_width=True)
        
    else:
        st.info("👆 Please upload a CSV file to view data overview")

with tab3:
    # ADVANCED FEATURES TAB
    st.header("🔧 Advanced Features")
    
    st.subheader("🤖 AI Agent Status")
    
    # Check OpenAI status
    try:
        agent = OpenAIAnalyticsAgent()
        status = agent.get_status()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if status['openai_available']:
                st.success("✅ OpenAI GPT-4 Available")
            else:
                st.warning("⚠️ OpenAI GPT-4 Not Available")
            
            if status['api_key_configured']:
                st.success("✅ API Key Configured")
            else:
                st.warning("⚠️ API Key Not Configured")
        
        with col2:
            if status['fallback_system']:
                st.success("✅ Fallback System Active")
            
            st.info(f"🔧 {len(status['capabilities'])} Capabilities")
        
        # Capabilities
        st.subheader("🚀 System Capabilities")
        for capability in status['capabilities']:
            st.markdown(f"• {capability}")
            
    except Exception as e:
        st.error(f"Error checking agent status: {str(e)}")

with tab4:
    # SETTINGS TAB
    st.header("⚙️ Settings")
    
    st.subheader("🔧 System Configuration")
    
    # OpenAI API Key
    st.subheader("🔑 OpenAI API Key")
    current_key = os.getenv('OPENAI_API_KEY', '')
    if current_key:
        st.success("✅ API Key is configured")
        if st.button("🔍 Test Connection"):
            try:
                agent = OpenAIAnalyticsAgent()
                status = agent.get_status()
                if status['openai_available']:
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ No API key configured")
        st.info("Set OPENAI_API_KEY environment variable or add it to .env file")
    
    # System Information
    st.subheader("ℹ️ System Information")
    st.info(f"""
    **Current Session:**
    - Messages: {len(st.session_state.messages)}
    - Theme: {st.session_state.get('theme', 'dark')}
    - Data Loaded: {'Yes' if st.session_state.uploaded_data is not None else 'No'}
    - File: {st.session_state.uploaded_filename if st.session_state.uploaded_filename else 'None'}
    """)
    
    st.subheader("🔄 System Actions")
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.messages = []
        st.session_state.message_charts = {}
        st.session_state.uploaded_data = None
        st.session_state.uploaded_filename = None
        st.session_state.file_uploaded = False
        st.rerun()
    
    if st.button("🔄 Reset Session", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Sidebar - File Upload (always visible)
with st.sidebar:
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.header("📁 Upload Data")
    
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
            st.session_state.file_uploaded = True  # Set flag for main content
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.info(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            # Prominent instruction
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                        padding: 1rem; border-radius: 10px; margin: 1rem 0;
                        border: 2px solid #66bb6a;'>
                <h4 style='color: white; margin: 0;'>🚀 Ready to Chat!</h4>
                <p style='color: white; margin: 0.5rem 0 0 0;'>
                    Go to the <strong>🤖 AI Chatbot</strong> tab above to start asking questions!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Force rerun to update main content
            st.rerun()
            
            # Show preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())
            
            # Show columns
            with st.expander("📋 Columns"):
                for col in df.columns:
                    st.write(f"• {col} ({df[col].dtype})")
                    
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8rem;'>
        AI Analytics Intelligence System<br>
        OpenAI GPT-4 Powered Edition<br>
        <span style='color: #4CAF50;'>●</span> Professional Analytics Platform
    </div>
    """, unsafe_allow_html=True)
