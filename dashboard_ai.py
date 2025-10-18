"""
AI-POWERED Analytics Dashboard
With auto-chart generation and intelligent responses
Run: streamlit run dashboard_ai.py
"""
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
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
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .confidence-high {
        background-color: #4caf50;
        color: white;
    }
    .confidence-medium {
        background-color: #ff9800;
        color: white;
    }
    .confidence-low {
        background-color: #f44336;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = SmartAnalyticsAgent(use_openai=False)
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# Title
st.markdown('<div class="main-header">🤖 AI-Powered Analytics Intelligence System</div>', unsafe_allow_html=True)
st.markdown("##### Ask questions, get instant analytics with auto-generated visualizations")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📤 Upload Data")
    
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload your data to start asking questions"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.session_state.agent.load_data(df)
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            st.info(f"📊 {len(df)} rows × {len(df.columns)} columns")
            
            # Data preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head(5), use_container_width=True)
            
            # Column info
            with st.expander("📋 Columns"):
                for col in df.columns:
                    dtype = 'Numeric' if pd.api.types.is_numeric_dtype(df[col]) else 'Text'
                    st.text(f"• {col} ({dtype})")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Sample questions
    st.markdown("### 💡 Example Questions")
    example_questions = [
        "What is the total revenue?",
        "Show me top 5 products",
        "Which region has highest sales?",
        "What are the trends over time?",
        "Compare sales by category",
        "What's the average order value?"
    ]
    
    for q in example_questions:
        if st.button(q, key=f"example_{q}", use_container_width=True):
            st.session_state.current_question = q
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat area
if st.session_state.uploaded_data is not None:
    
    # Display conversation history
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # AI response with visualizations
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>AI Assistant:</strong><br>{msg['content']['answer']}
            </div>
            """, unsafe_allow_html=True)
            
            # Show confidence
            confidence = msg['content'].get('confidence', 0)
            conf_class = 'high' if confidence > 0.8 else 'medium' if confidence > 0.6 else 'low'
            st.markdown(f"""
            <span class="confidence-badge confidence-{conf_class}">
                Confidence: {confidence*100:.0f}%
            </span>
            """, unsafe_allow_html=True)
            
            # Show visualizations if any
            if msg['content'].get('visualizations'):
                for viz in msg['content']['visualizations']:
                    if viz.get('figure'):
                        st.plotly_chart(viz['figure'], use_container_width=True, key=f"viz_{msg['timestamp']}")
                    elif viz['type'] == 'metrics':
                        # Display metrics
                        cols = st.columns(min(4, len(viz['data'])))
                        for i, (key, value) in enumerate(list(viz['data'].items())[:4]):
                            with cols[i]:
                                label = key.replace('_', ' ').title()
                                if isinstance(value, (int, float)):
                                    display_value = f"${value:,.2f}" if value > 100 else f"{value:,.2f}"
                                    st.metric(label, display_value)
            
            # Show recommendations or suggested questions
            if msg.get('is_vague') and msg['content'].get('recommendations'):
                # This is a vague question - show suggested questions
                st.markdown("**📝 Try asking:**")
                for suggestion in msg['content']['recommendations']:
                    st.markdown(f"- {suggestion}")
            elif msg['content'].get('recommendations'):
                # Strategic recommendations
                with st.expander("💡 Strategic Recommendations"):
                    for rec in msg['content']['recommendations']:
                        st.markdown(f"- {rec}")
            
            # Show SQL equivalent
            if msg['content'].get('sql_equivalent'):
                with st.expander("🔍 Query Details"):
                    st.code(msg['content']['sql_equivalent'], language='sql')
                    st.caption(f"Execution time: {msg['content'].get('execution_time', 0):.3f}s")
    
    # Chat input
    user_input = st.chat_input("Ask a question about your data...")
    
    # Handle example question clicks
    if hasattr(st.session_state, 'current_question'):
        user_input = st.session_state.current_question
        delattr(st.session_state, 'current_question')
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
        # Get AI response with analytics and visualizations
        with st.spinner('🤖 Analyzing your data...'):
            response = st.session_state.agent.ask(user_input)
            response['timestamp'] = pd.Timestamp.now().isoformat()
        
        # Add assistant message
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response,
            'timestamp': response['timestamp'],
            'is_vague': response.get('is_vague', False)
        })
        
        st.rerun()

else:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 👋 Welcome to AI Analytics Intelligence System
        
        ### Get Started in 3 Steps:
        
        1. **📤 Upload** your CSV file (left sidebar)
        2. **💬 Ask** questions in natural language
        3. **📊 Get** instant analytics with auto-generated charts
        
        ---
        
        ### What You Can Ask:
        
        - **Aggregations**: "What is the total revenue?"
        - **Rankings**: "Show me top 10 products"
        - **Trends**: "How have sales changed over time?"
        - **Comparisons**: "Compare regions by performance"
        - **Predictions**: "Forecast next month's sales"
        - **Diagnostics**: "Why did revenue drop in Q3?"
        
        ---
        
        ### Sample Demo Files Available:
        - `retail_demo.csv` - Retail sales data
        - `ecommerce_demo.csv` - E-commerce orders
        - `sales_data.csv` - Sales transactions
        
        Located in: `data/sample/`
        """)
        
        st.info("👈 Upload a CSV file from the sidebar to begin!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <strong>AI Analytics Intelligence System</strong><br>
    Powered by Advanced Analytics Engine | Auto-Chart Generation | Smart Insights
</div>
""", unsafe_allow_html=True)

