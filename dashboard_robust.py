"""
ROBUST AI-POWERED Analytics Dashboard
Professional UI with Advanced Features in Submenu
Run: streamlit run dashboard_robust.py
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

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Intelligence System",
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
        'file_uploaded': False
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
                background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
                color: #ffffff !important;
            }
            .stMarkdown, .stText, p, span, div {
                color: #ffffff !important;
            }
            .stTextInput > div > div > input {
                color: #ffffff !important;
                background-color: #2d2d2d !important;
                border: 1px solid #666 !important;
            }
            .stTextInput > label {
                color: #ffffff !important;
            }
            .stButton > button {
                color: #ffffff !important;
            }
            .main-header {
                font-size: 3rem;
                font-weight: 800;
                color: #00d4ff;
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #0066aa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
                margin-bottom: 2rem;
            }
            .subtitle {
                font-size: 1.2rem;
                color: #b0b0b0;
                text-align: center;
                margin-bottom: 2rem;
                font-weight: 300;
            }
            .chat-container {
                background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                border: 1px solid #333;
            }
            .chat-message {
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: 15%;
                border-left: 4px solid #00d4ff;
            }
            .assistant-message {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                margin-right: 15%;
                border-left: 4px solid #ff6b6b;
            }
            .confidence-badge {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                font-weight: bold;
                display: inline-block;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .metric-card {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                margin: 1rem 0;
                box-shadow: 0 15px 30px rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
            }
            .sidebar-card {
                background: linear-gradient(135deg, #2d2d2d 0%, #3d3d3d 100%);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                border: 1px solid #444;
            }
            .quick-action-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                width: 100%;
                text-align: left;
            }
            .quick-action-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            }
            .upload-area {
                background: linear-gradient(135deg, #2d2d2d 0%, #3d3d3d 100%);
                border: 2px dashed #666;
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            .upload-area:hover {
                border-color: #00d4ff;
                background: linear-gradient(135deg, #2d2d2d 0%, #3d3d3d 50%, #2d2d2d 100%);
            }
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-online { background: #4CAF50; }
            .status-offline { background: #f44336; }
        </style>
        """
    else:  # light theme
        return """
        <style>
            .stApp {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #262730 !important;
            }
            .stMarkdown, .stText, p, span, div {
                color: #262730 !important;
            }
            .stTextInput > div > div > input {
                color: #262730 !important;
                background-color: #ffffff !important;
                border: 1px solid #dee2e6 !important;
            }
            .stTextInput > label {
                color: #262730 !important;
            }
            .stButton > button {
                color: #ffffff !important;
            }
            .main-header {
                font-size: 3rem;
                font-weight: 800;
                color: #1f4788;
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #1f4788 0%, #2196F3 50%, #00bcd4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(31, 71, 136, 0.3);
                margin-bottom: 2rem;
            }
            .subtitle {
                font-size: 1.2rem;
                color: #666;
                text-align: center;
                margin-bottom: 2rem;
                font-weight: 300;
            }
            .chat-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                border: 1px solid #dee2e6;
            }
            .chat-message {
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0,0,0,0.05);
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: 15%;
                border-left: 4px solid #1f4788;
            }
            .assistant-message {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                margin-right: 15%;
                border-left: 4px solid #ff6b6b;
            }
            .confidence-badge {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                font-weight: bold;
                display: inline-block;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .metric-card {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                color: #262730;
                padding: 2rem;
                border-radius: 20px;
                margin: 1rem 0;
                box-shadow: 0 15px 30px rgba(0,0,0,0.1);
                border: 1px solid #dee2e6;
                backdrop-filter: blur(10px);
            }
            .sidebar-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                border: 1px solid #dee2e6;
            }
            .quick-action-btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                margin: 0.5rem 0;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 100%;
                text-align: left;
            }
            .quick-action-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            .upload-area {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border: 2px dashed #ccc;
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            .upload-area:hover {
                border-color: #1f4788;
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #ffffff 100%);
            }
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-online { background: #4CAF50; }
            .status-offline { background: #f44336; }
        </style>
        """

# Apply dark theme only
st.markdown(get_theme_css('dark'), unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🚀 AI Analytics Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Professional Analytics Platform with Conversational AI</div>', unsafe_allow_html=True)

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
                
                # Display chart if exists for this message
                if idx in st.session_state.message_charts:
                    chart_data = st.session_state.message_charts[idx]
                    try:
                        if chart_data.get('type') == 'bar':
                            fig = px.bar(
                                x=chart_data.get('x', []),
                                y=chart_data.get('y', []),
                                title=chart_data.get('title', 'Chart'),
                                labels={'x': chart_data.get('x_label', 'X'), 'y': chart_data.get('y_label', 'Y')}
                            )
                            fig.update_layout(template='plotly_dark', height=400)
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
                        elif chart_data.get('type') == 'pie':
                            fig = px.pie(
                                values=chart_data.get('values', []),
                                names=chart_data.get('labels', []),
                                title=chart_data.get('title', 'Chart')
                            )
                            fig.update_layout(template='plotly_dark', height=400)
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
                        elif chart_data.get('type') == 'line':
                            fig = px.line(
                                x=chart_data.get('x', []),
                                y=chart_data.get('y', []),
                                title=chart_data.get('title', 'Chart'),
                                labels={'x': chart_data.get('x_label', 'X'), 'y': chart_data.get('y_label', 'Y')}
                            )
                            fig.update_layout(template='plotly_dark', height=400)
                            st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
                    except Exception as chart_error:
                        st.caption(f"⚠️ Chart display error: {str(chart_error)}")
        
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
                        agent = SmartAnalyticsAgent()
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
            
            # Metrics
            col2_1, col2_2 = st.columns(2)
            
            with col2_1:
                st.markdown(f'''
                <div class="metric-card">
                    <h3>📊 Rows</h3>
                    <h2>{len(st.session_state.uploaded_data):,}</h2>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2_2:
                st.markdown(f'''
                <div class="metric-card">
                    <h3>📋 Columns</h3>
                    <h2>{len(st.session_state.uploaded_data.columns)}</h2>
                </div>
                ''', unsafe_allow_html=True)
            
            # Data quality
            null_percentage = (st.session_state.uploaded_data.isnull().sum().sum() / 
                              (len(st.session_state.uploaded_data) * len(st.session_state.uploaded_data.columns))) * 100
            
            if null_percentage < 5:
                st.success(f"✅ Excellent Quality ({null_percentage:.1f}% missing)")
            elif null_percentage < 15:
                st.warning(f"⚠️ Good Quality ({null_percentage:.1f}% missing)")
            else:
                st.error(f"❌ Needs Attention ({null_percentage:.1f}% missing)")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick Actions
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            st.header("⚡ Quick Actions")
            
            quick_questions = [
                "What is the total revenue?",
                "Show me top 5 products",
                "Compare sales by category",
                "What are the trends over time?",
                "Which region has highest sales?",
                "What's the average order value?"
            ]
            
            for question in quick_questions:
                if st.button(f"💬 {question}", key=f"quick_{question}", help="Click to ask this question"):
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": question})
                    
                    # Get AI response
                    try:
                        agent = SmartAnalyticsAgent()
                        agent.load_data(st.session_state.uploaded_data)
                        response = agent.ask(question)
                        
                        # Add AI response
                        message_idx = len(st.session_state.messages)
                        st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                        
                        # Store chart data if exists
                        if 'chart_data' in response and response['chart_data']:
                            st.session_state.message_charts[message_idx] = response['chart_data']
                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
                    
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <h3>🚀 Ready to Start</h3>
                <p>Upload a CSV file to begin analyzing your data with AI!</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    # DATA OVERVIEW TAB
    st.header("📊 Data Overview")
    
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        
        # Statistics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        with col4:
            st.metric("File Size", f"{len(st.session_state.uploaded_filename)} chars")
        
        # Data types and info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null': df.count(),
                'Null': df.isnull().sum(),
                'Unique': df.nunique()
            })
            st.dataframe(col_info, use_container_width=True)
        
        with col2:
            st.subheader("👀 Sample Data")
            st.dataframe(df.head(10), use_container_width=True)
        
        # Data quality analysis
        st.subheader("🔍 Data Quality Analysis")
        
        # Missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            fig_missing = px.bar(
                x=missing_data.index,
                y=missing_data.values,
                title="Missing Values by Column",
                labels={'x': 'Columns', 'y': 'Missing Count'}
            )
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.success("✅ No missing values found!")
        
        # Data types distribution
        try:
            type_counts = df.dtypes.value_counts()
            # Convert dtype objects to strings for JSON serialization
            type_labels = [str(dtype) for dtype in type_counts.index]
            type_values = type_counts.values.tolist()
            
            fig_types = px.pie(
                values=type_values,
                names=type_labels,
                title="Data Types Distribution"
            )
            st.plotly_chart(fig_types, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not display data types chart: {str(e)}")
            st.write("**Data Types:**")
            for dtype, count in df.dtypes.value_counts().items():
                st.write(f"- {str(dtype)}: {count} columns")
        
    else:
        st.info("👆 Please upload a CSV file to view data overview")

with tab3:
    # ADVANCED FEATURES TAB
    st.header("🔧 Advanced Features")
    
    if st.session_state.uploaded_data is not None:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Advanced Analytics Features</h3>
            <p>Professional-grade analytics tools for deep data insights:</p>
            <ul>
                <li>📈 <strong>Cohort Analysis</strong> - Customer retention and behavior tracking</li>
                <li>🧪 <strong>A/B Testing</strong> - Statistical significance testing</li>
                <li>📊 <strong>Comparative Analysis</strong> - Period-over-period comparisons</li>
                <li>🎯 <strong>Scenario Planning</strong> - What-if analysis</li>
                <li>🔄 <strong>Real-time Refresh</strong> - Auto-updating data</li>
                <li>🎤 <strong>Voice Interface</strong> - Speech-to-text and text-to-speech</li>
            </ul>
            <p><em>These features are available as separate modules and can be accessed when needed.</em></p>
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
            st.success(f"✅ Found {len(date_cols)} date columns: {', '.join(date_cols)}")
            st.info("💡 Your data is suitable for cohort analysis and time-based comparisons!")
        else:
            st.warning("⚠️ No date columns detected. Advanced analytics work best with time-series data.")
        
        # Check for categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if categorical_cols:
            st.success(f"✅ Found {len(categorical_cols)} categorical columns: {', '.join(categorical_cols)}")
            st.info("💡 Your data is suitable for A/B testing and comparative analysis!")
        
        # Feature status
        st.subheader("🚀 Feature Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📈 Cohort Analysis</h4>
                <p>Status: <span class="status-indicator status-online"></span> Ready</p>
                <p>Requires: Date + User columns</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🧪 A/B Testing</h4>
                <p>Status: <span class="status-indicator status-online"></span> Ready</p>
                <p>Requires: Group + Metric columns</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🔄 Real-time</h4>
                <p>Status: <span class="status-indicator status-offline"></span> Coming Soon</p>
                <p>Auto-refresh capabilities</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick analysis suggestions
        st.subheader("💡 Suggested Analyses")
        
        if date_cols and len(categorical_cols) > 0:
            st.markdown("**Based on your data, you can perform:**")
            st.markdown("- 📈 **Cohort Analysis** using date and categorical columns")
            st.markdown("- 🧪 **A/B Testing** comparing different categories")
            st.markdown("- 📊 **Time Series Analysis** for trend identification")
        
        # Placeholder for future implementation
        st.info("🚧 Advanced analytics features will be implemented as separate modules. For now, use the chatbot for detailed analysis!")
        
    else:
        st.info("👆 Please upload a CSV file to access advanced features")

with tab4:
    # SETTINGS TAB
    st.header("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Appearance")
        st.info("🌙 **Dark Mode Only** - Optimized for extended use and reduced eye strain")
        
        st.subheader("📤 Export Options")
        if st.session_state.uploaded_data is not None:
            # Export data as CSV
            csv = st.session_state.uploaded_data.to_csv(index=False)
            st.download_button(
                label="📊 Download Data (CSV)",
                data=csv,
                file_name=f"{st.session_state.uploaded_filename}_export.csv",
                mime="text/csv",
                help="Download your uploaded data as CSV"
            )
            
            # Export chat as text
            if st.session_state.messages:
                chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                st.download_button(
                    label="💬 Download Chat (TXT)",
                    data=chat_text,
                    file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    help="Download chat conversation as text file"
                )
    
    with col2:
        st.subheader("ℹ️ System Information")
        st.info(f"""
        **Current Session:**
        - Messages: {len(st.session_state.messages)}
        - Theme: {st.session_state.get('theme', 'light')}
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
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🚀 AI Analytics Intelligence System - Professional Edition</p>
    <p>💡 Robust, responsive, and feature-rich analytics platform</p>
</div>
""", unsafe_allow_html=True)
