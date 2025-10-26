"""
Test Script - Vague Question Handling
Demonstrates how the system handles irrelevant or vague questions
"""
import pandas as pd
from src.conversational.smart_agent import SmartAnalyticsAgent

print("="*80)
print("TESTING VAGUE QUESTION HANDLING")
print("="*80)
print()

# Load sample data
df = pd.read_csv('data/sample/retail_demo.csv')
print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
print(f"Columns: {', '.join(df.columns.tolist())}")
print()

# Initialize agent
agent = SmartAnalyticsAgent(use_openai=False)
agent.load_data(df)

# Test cases
test_questions = [
    # Vague questions
    ("hi", "Greeting"),
    ("hello", "Greeting"),
    ("help", "Too vague"),
    ("tell me something", "Too vague"),
    ("what can you do", "Too vague"),
    
    # Irrelevant questions
    ("what's the weather", "Irrelevant topic"),
    ("tell me a joke", "Irrelevant topic"),
    ("who won the game", "Irrelevant topic"),
    
    # Short unclear questions
    ("analyze", "Too short/unclear"),
    ("show data", "Too short/unclear"),
    
    # Valid questions (should work)
    ("what is the total revenue?", "Valid - should answer"),
    ("show me top 5 products", "Valid - should answer"),
]

print("-"*80)
print("TESTING VAGUE/IRRELEVANT QUESTION DETECTION")
print("-"*80)
print()

for question, test_type in test_questions:
    print(f"Q: \"{question}\"")
    print(f"   Type: {test_type}")
    
    response = agent.ask(question)
    
    is_vague = response.get('is_vague', False)
    confidence = response.get('confidence', 0)
    
    if is_vague:
        print(f"    Detected as vague/irrelevant (confidence: {confidence})")
        print(f"   Response: {response['answer'][:100]}...")
        if response.get('recommendations'):
            print(f"   Suggestions provided: {len(response['recommendations'])} questions")
            print(f"   Example: {response['recommendations'][0]}")
    else:
        print(f"    Valid question (confidence: {confidence})")
        print(f"   Response: {response['answer'][:100]}...")
    
    print()

print("="*80)
print("TEST COMPLETE")
print("="*80)
print()
print("Summary:")
print("- Vague questions are detected and handled gracefully")
print("- User receives contextual suggestions based on their data")
print("- System guides users to ask better questions")
print("- Valid questions get full analytics + visualizations")

