"""
SIMPLE AI-POWERED Analytics Dashboard
Core Chatbot Functionality - No Infinite Loops
Run: streamlit run dashboard_simple.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="🤖",
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
        </style>
        """

# Apply theme
st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🤖 AI Analytics Intelligence System</div>', unsafe_allow_html=True)
st.markdown("**Ask questions, get instant analytics with auto-generated visualizations**")
st.markdown("---")

# Sidebar
with st.sidebar:
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
        help="Upload your data file to start analyzing"
    )
    
    if uploaded_file is not None:
        try:
            # Parse CSV
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.session_state.uploaded_filename = uploaded_file.name
            
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
    
    st.markdown("---")
    
    # Quick Actions
    if st.session_state.uploaded_data is not None:
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
            if st.button(f"💬 {question}", key=f"quick_{question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.header("🤖 AI Analytics Assistant")
    
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
            help="Ask any question about your uploaded data",
            key="chat_input"
        )
        
        # Send button
        if st.button("Send", type="primary", key="send_button"):
            if user_input:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get AI response
                try:
                    with st.spinner("🤖 AI is thinking..."):
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
                        st.markdown("**💡 Try asking:**")
                        for suggestion in response['suggested_questions'][:3]:
                            if st.button(f"💬 {suggestion}", key=f"suggest_{suggestion}"):
                                st.session_state.messages.append({"role": "user", "content": suggestion})
                                st.rerun()
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
            
    else:
        st.info("👆 Please upload a CSV file to start chatting with your data")

with col2:
    # Data metrics
    if st.session_state.uploaded_data is not None:
        st.header("📊 Data Overview")
        
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            st.markdown(f'''
            <div class="metric-card">
                <h3>📊 Total Rows</h3>
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
            st.success(f"✅ Data Quality: Excellent ({null_percentage:.1f}% missing)")
        elif null_percentage < 15:
            st.warning(f"⚠️ Data Quality: Good ({null_percentage:.1f}% missing)")
        else:
            st.error(f"❌ Data Quality: Needs attention ({null_percentage:.1f}% missing)")
        
        # Export options
        st.markdown("---")
        st.header("📤 Export")
        
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
        
    else:
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 Get Started</h3>
            <p>Upload a CSV file to begin analyzing your data with AI!</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 AI Analytics Intelligence System - Simple & Reliable</p>
    <p>💡 No infinite loops - just clean, working analytics!</p>
</div>
""", unsafe_allow_html=True)
