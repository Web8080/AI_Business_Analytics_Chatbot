#!/usr/bin/env python3
"""
Test OpenAI Integration
Quick test to verify the OpenAI agent works with fallback
"""
import sys
import os
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.conversational.openai_agent import OpenAIAnalyticsAgent

def test_openai_integration():
    """Test OpenAI integration with sample data"""
    print("🚀 Testing OpenAI Integration...")
    print("=" * 50)
    
    # Load sample data
    try:
        df = pd.read_csv('data/sample/retail_demo.csv')
        print(f"✅ Loaded sample data: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"📊 Columns: {', '.join(df.columns.tolist())}")
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        return
    
    # Initialize agent
    print("\n🤖 Initializing OpenAI Agent...")
    agent = OpenAIAnalyticsAgent()
    agent.load_data(df)
    
    # Check status
    status = agent.get_status()
    print(f"📋 Agent Status:")
    print(f"   - OpenAI Available: {status['openai_available']}")
    print(f"   - API Key Configured: {status['api_key_configured']}")
    print(f"   - Fallback System: {status['fallback_system']}")
    
    # Test questions
    test_questions = [
        "What is the total revenue?",
        "Show me the top 5 products",
        "Give me a summary of the data"
    ]
    
    print(f"\n🧪 Testing with {len(test_questions)} questions...")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        try:
            response = agent.ask(question)
            answer = response.get('answer', 'No answer')
            print(f"   ✅ Answer: {str(answer)[:100]}...")
            print(f"   📊 Confidence: {response['confidence']}")
            print(f"   🔧 Source: {response.get('source', 'unknown')}")
            if response.get('chart_data'):
                print(f"   📈 Chart generated: {response['chart_data'].get('type', 'unknown')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ OpenAI Integration Test Complete!")
    
    if not status['openai_available']:
        print("⚠️  Note: OpenAI not available, using fallback system")
        print("   To enable OpenAI: set OPENAI_API_KEY environment variable")

if __name__ == "__main__":
    test_openai_integration()
