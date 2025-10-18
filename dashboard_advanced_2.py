"""
ADVANCED AI-POWERED Analytics Dashboard - Feature #2
Voice Input/Output with Speech-to-Text and Text-to-Speech
Run: streamlit run dashboard_advanced_2.py
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

# Voice processing imports
try:
    import speech_recognition as sr
    import pyttsx3
    from gtts import gTTS
    import pygame
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    st.warning("Voice features require additional packages. Install with: pip install speech_recognition pyttsx3 gtts pygame")

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.smart_agent import SmartAnalyticsAgent

# Page configuration
st.set_page_config(
    page_title="AI Analytics Dashboard - Voice",
    page_icon="🎤",
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
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'speech_language' not in st.session_state:
    st.session_state.speech_language = 'en'
if 'voice_speed' not in st.session_state:
    st.session_state.voice_speed = 1.0

# Voice processing functions
class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        if VOICE_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
            except:
                pass
    
    def speech_to_text(self):
        """Convert speech to text"""
        if not VOICE_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                st.info("🎤 Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            st.info("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio, language=st.session_state.speech_language)
            return text
        except sr.WaitTimeoutError:
            st.error("⏰ No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            st.error("❌ Could not understand speech. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition error: {e}")
            return None
    
    def text_to_speech(self, text):
        """Convert text to speech"""
        if not VOICE_AVAILABLE:
            return False
        
        try:
            # Use gTTS for better quality
            tts = gTTS(text=text, lang=st.session_state.speech_language, slow=False)
            
            # Save to temporary file
            audio_file = "temp_audio.mp3"
            tts.save(audio_file)
            
            # Play audio
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            pygame.mixer.quit()
            Path(audio_file).unlink(missing_ok=True)
            
            return True
        except Exception as e:
            st.error(f"❌ Text-to-speech error: {e}")
            return False

# Initialize voice processor
if VOICE_AVAILABLE:
    voice_processor = VoiceProcessor()

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
            .voice-indicator {
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
                animation: pulse 1s infinite;
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
            .voice-indicator {
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                font-weight: bold;
                display: inline-block;
                margin: 0.5rem 0;
                animation: pulse 1s infinite;
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

# Title
st.markdown('<div class="main-header">🎤 AI Analytics Dashboard - Voice Edition</div>', unsafe_allow_html=True)
st.markdown("Ask questions **by voice** and get **spoken responses** with instant analytics")
st.markdown("---")

# Voice status indicator
if VOICE_AVAILABLE and st.session_state.voice_enabled:
    st.markdown('<div class="voice-indicator">🎤 Voice Mode: ON</div>', unsafe_allow_html=True)
elif VOICE_AVAILABLE:
    st.info("🎤 Voice features available - enable in sidebar")
else:
    st.warning("🎤 Voice features not available - install required packages")

# Sidebar with Voice Controls
with st.sidebar:
    st.header("🎤 Voice Settings")
    
    if VOICE_AVAILABLE:
        # Voice enable/disable
        voice_enabled = st.toggle(
            "Enable Voice",
            value=st.session_state.voice_enabled,
            help="Enable speech-to-text and text-to-speech features"
        )
        if voice_enabled != st.session_state.voice_enabled:
            st.session_state.voice_enabled = voice_enabled
            st.rerun()
        
        if st.session_state.voice_enabled:
            # Language selection
            language_options = {
                'en': 'English',
                'es': 'Spanish',
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese'
            }
            
            speech_language = st.selectbox(
                "Speech Language",
                options=list(language_options.keys()),
                format_func=lambda x: language_options[x],
                index=list(language_options.keys()).index(st.session_state.speech_language),
                help="Language for speech recognition and synthesis"
            )
            if speech_language != st.session_state.speech_language:
                st.session_state.speech_language = speech_language
                st.rerun()
            
            # Voice speed
            voice_speed = st.slider(
                "Voice Speed",
                min_value=0.5,
                max_value=2.0,
                value=st.session_state.voice_speed,
                step=0.1,
                help="Speed of text-to-speech playback"
            )
            if voice_speed != st.session_state.voice_speed:
                st.session_state.voice_speed = voice_speed
                st.rerun()
            
            # Test voice
            if st.button("🎤 Test Voice Input"):
                with st.spinner("Listening..."):
                    text = voice_processor.speech_to_text()
                    if text:
                        st.success(f"🎤 Heard: '{text}'")
                        st.session_state.messages.append({"role": "user", "content": text})
                        st.rerun()
            
            if st.button("🔊 Test Voice Output"):
                test_text = "Hello! This is a test of the voice output system."
                if voice_processor.text_to_speech(test_text):
                    st.success("🔊 Voice output test completed!")
                else:
                    st.error("❌ Voice output test failed")
    else:
        st.error("Voice features not available")
        st.code("pip install speech_recognition pyttsx3 gtts pygame")
    
    st.markdown("---")
    
    # Theme toggle
    st.header("🎨 Settings")
    theme = st.selectbox(
        "Theme",
        ["light", "dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        help="Choose your preferred theme"
    )
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
    
    st.markdown("---")
    
    # Quick Actions
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
    
    # Voice input button
    if VOICE_AVAILABLE and st.session_state.voice_enabled and st.session_state.uploaded_data is not None:
        col_voice1, col_voice2 = st.columns([1, 1])
        
        with col_voice1:
            if st.button("🎤 Ask by Voice", type="primary", help="Click and speak your question"):
                with st.spinner("🎤 Listening..."):
                    text = voice_processor.speech_to_text()
                    if text:
                        st.session_state.messages.append({"role": "user", "content": text})
                        st.rerun()
        
        with col_voice2:
            if st.button("🔊 Speak Last Response", help="Have the AI speak its last response"):
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
                    voice_processor.text_to_speech(st.session_state.messages[-1]["content"])
    
    # Text input
    if st.session_state.uploaded_data is not None:
        user_input = st.text_input(
            "Ask a question about your data...",
            placeholder="e.g., What is the total revenue?",
            help="Type your question or use voice input above"
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
                    
                    # Auto-speak response if voice is enabled
                    if VOICE_AVAILABLE and st.session_state.voice_enabled:
                        voice_processor.text_to_speech(response['answer'])
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to start chatting with your data")

with col2:
    # Voice metrics
    if st.session_state.uploaded_data is not None:
        st.header("🎤 Voice Analytics")
        
        # Voice status
        if VOICE_AVAILABLE and st.session_state.voice_enabled:
            st.markdown(f'''
            <div class="metric-card">
                <h3>🎤 Voice Status</h3>
                <h2>🟢 Active</h2>
                <p>Language: {st.session_state.speech_language.upper()}</p>
                <p>Speed: {st.session_state.voice_speed}x</p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="metric-card">
                <h3>🎤 Voice Status</h3>
                <h2>🔴 Inactive</h2>
                <p>Enable in sidebar</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Basic metrics
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
        
        # Voice interaction stats
        voice_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
        st.markdown(f'''
        <div class="metric-card">
            <h3>💬 Messages</h3>
            <h2>{len(voice_messages)}</h2>
            <p>Total interactions</p>
        </div>
        ''', unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="metric-card">
            <h3>🚀 Get Started</h3>
            <p>Upload a CSV file to begin voice-powered analytics!</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🎤 AI Analytics Intelligence System - Voice Edition</p>
    <p>💡 Speak your questions and hear the answers!</p>
</div>
""", unsafe_allow_html=True)
