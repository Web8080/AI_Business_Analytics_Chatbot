"""
Streamlit Cloud Optimized Dashboard
Minimal, fast-loading version for production deployment
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="AI Analytics Intelligence System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    .user-message {
        background: linear-gradient(135deg, #00c853 0%, #00e676 100%);
        color: #1a1a1a;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #2196F3 0%, #64b5f6 100%);
        color: #1a1a1a;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'agent_loaded' not in st.session_state:
    st.session_state.agent_loaded = False
if 'agent' not in st.session_state:
    st.session_state.agent = None

# Header
st.markdown("""
<div class="main-header">
    <h1 style='color: white; margin: 0;'>🚀 AI Analytics Intelligence System</h1>
    <p style='color: #e0e0e0; margin: 0.5rem 0 0 0;'>
        OpenAI GPT-4 Powered with Intelligent Fallback
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - File Upload
with st.sidebar:
    st.header("📁 Upload Data")
    
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload your CSV file for analysis"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.info(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Data status
    if st.session_state.uploaded_data is not None:
        st.success("🟢 Data Loaded")
    else:
        st.warning("⚠️ No Data Loaded")
    
    # Clear button
    if st.button("🗑️ Clear All Data"):
        st.session_state.messages = []
        st.session_state.uploaded_data = None
        st.session_state.agent_loaded = False
        st.session_state.agent = None
        st.rerun()

# Main content
if st.session_state.uploaded_data is None:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 3rem; border-radius: 15px; text-align: center;'>
        <h2 style='color: white;'>👋 Welcome!</h2>
        <p style='color: #e0e0e0; font-size: 1.2rem;'>
            Upload a CSV file to get started with AI-powered analytics!
        </p>
        <br>
        <p style='color: #b0b0b0;'>
            👈 Use the sidebar to upload your data
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Lazy load agent only when needed
    if not st.session_state.agent_loaded:
        with st.spinner("🤖 Initializing AI agent... (this may take 5-10 seconds)"):
            try:
                from src.conversational.openai_agent import OpenAIAnalyticsAgent
                st.session_state.agent = OpenAIAnalyticsAgent()
                st.session_state.agent.load_data(st.session_state.uploaded_data)
                st.session_state.agent_loaded = True
            except Exception as e:
                st.error(f"Error loading agent: {str(e)}")
                st.stop()
    
    # Show agent status
    if st.session_state.agent:
        try:
            status = st.session_state.agent.get_status()
            if status.get('openai_available'):
                st.success("🟢 OpenAI GPT-4 Mode Active")
            else:
                st.info("🟡 Fallback Mode Active (Advanced Rules)")
        except:
            st.info("🟡 Fallback Mode Active")
    
    st.markdown("---")
    
    # Display chat history
    st.subheader("🤖 AI Analytics Assistant")
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><b>AI:</b> {message["content"]}</div>', unsafe_allow_html=True)
            
            # Display chart if exists
            if "chart" in message:
                try:
                    chart_data = message["chart"]
                    if chart_data and 'type' in chart_data and 'x' in chart_data and 'y' in chart_data:
                        if chart_data['type'] == 'bar':
                            fig = go.Figure(data=[go.Bar(x=chart_data['x'], y=chart_data['y'])])
                        elif chart_data['type'] == 'line':
                            fig = go.Figure(data=[go.Scatter(x=chart_data['x'], y=chart_data['y'], mode='lines')])
                        elif chart_data['type'] == 'pie':
                            fig = go.Figure(data=[go.Pie(labels=chart_data['x'], values=chart_data['y'])])
                        else:
                            fig = None
                        
                        if fig:
                            fig.update_layout(template='plotly_dark', height=400, title=chart_data.get('title', ''))
                            st.plotly_chart(fig, key=f"chart_{st.session_state.messages.index(message)}")
                except:
                    pass
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Ask a question about your data...",
            placeholder="e.g., What is the total revenue?",
            key="chat_input"
        )
        send_pressed = st.form_submit_button("📤 Send")
        
        if send_pressed and user_input and st.session_state.agent:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            try:
                with st.spinner("🤖 Analyzing..."):
                    response = st.session_state.agent.ask(user_input)
                    
                    # Add AI message
                    ai_message = {
                        "role": "assistant",
                        "content": response.get('answer', 'No response')
                    }
                    
                    # Add chart if exists
                    if response.get('chart_data'):
                        ai_message['chart'] = response['chart_data']
                    
                    st.session_state.messages.append(ai_message)
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Show Summary", key="btn_summary"):
            st.session_state.messages.append({"role": "user", "content": "Give me a summary"})
            try:
                response = st.session_state.agent.ask("Give me a summary of the data")
                ai_message = {"role": "assistant", "content": response.get('answer', 'No response')}
                if response.get('chart_data'):
                    ai_message['chart'] = response['chart_data']
                st.session_state.messages.append(ai_message)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("📈 Top Items", key="btn_top"):
            st.session_state.messages.append({"role": "user", "content": "Show top 5 items"})
            try:
                response = st.session_state.agent.ask("Show me the top 5 items")
                ai_message = {"role": "assistant", "content": response.get('answer', 'No response')}
                if response.get('chart_data'):
                    ai_message['chart'] = response['chart_data']
                st.session_state.messages.append(ai_message)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col3:
        if st.button("📉 Trends", key="btn_trends"):
            st.session_state.messages.append({"role": "user", "content": "Show trends"})
            try:
                response = st.session_state.agent.ask("Show me trends in the data")
                ai_message = {"role": "assistant", "content": response.get('answer', 'No response')}
                if response.get('chart_data'):
                    ai_message['chart'] = response['chart_data']
                st.session_state.messages.append(ai_message)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", key="btn_clear_chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.caption("🔒 Your data stays private and is never stored permanently")

