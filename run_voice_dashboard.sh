#!/bin/bash

# Voice Dashboard Launch Script

echo "=========================================================================="
echo "🎤 AI ANALYTICS DASHBOARD - VOICE EDITION"
echo "=========================================================================="
echo ""
echo "✨ ADVANCED FEATURE #2:"
echo "   🎤 Speech-to-Text Input"
echo "   🔊 Text-to-Speech Output"
echo "   🌍 Multi-language Support"
echo "   ⚡ Voice Speed Control"
echo "   🎛️  Voice Settings Panel"
echo "   🔊 Auto-speak Responses"
echo "   🎤 Voice Test Functions"
echo ""
echo "📦 Installing voice dependencies..."
pip install -q speech_recognition pyttsx3 gtts pygame
echo ""
echo "Starting Voice Dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8503"
echo ""
echo "=========================================================================="
echo "Press Ctrl+C to stop the dashboard"
echo "=========================================================================="
echo ""

# Launch voice dashboard on different port
streamlit run dashboard_advanced_2.py --server.port 8503 --server.headless true
