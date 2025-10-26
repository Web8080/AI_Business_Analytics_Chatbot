#!/usr/bin/env python3
"""
Comprehensive Chatbot Testing Suite
Tests all aspects of the chatbot functionality
"""
import sys
import pytest
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.conversational.openai_agent import OpenAIAnalyticsAgent

class TestChatbotFunctionality:
    """Test chatbot core functionality"""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance"""
        return OpenAIAnalyticsAgent()
    
    @pytest.fixture
    def sample_data(self):
        """Load sample data"""
        return pd.read_csv('data/sample/retail_demo.csv')
    
    def test_agent_initialization(self, agent):
        """Test agent can be initialized"""
        assert agent is not None
        assert hasattr(agent, 'ask')
        assert hasattr(agent, 'load_data')
    
    def test_data_loading(self, agent, sample_data):
        """Test data loading works"""
        agent.load_data(sample_data)
        assert agent.current_data is not None
        assert len(agent.current_data) > 0
    
    def test_basic_questions(self, agent, sample_data):
        """Test basic question answering"""
        agent.load_data(sample_data)
        
        questions = [
            "what is the total revenue?",
            "how many transactions?",
            "what is the average sale?",
            "what is the highest sale?"
        ]
        
        for question in questions:
            response = agent.ask(question)
            assert 'answer' in response
            assert 'confidence' in response
            assert len(response['answer']) > 0
            print(f"[OK] {question} -> {response['answer'][:50]}...")
    
    def test_chart_generation(self, agent, sample_data):
        """Test chart generation for various questions"""
        agent.load_data(sample_data)
        
        chart_questions = [
            ("show me top 5 products", "bar"),
            ("top products by revenue", "bar"),
            ("show trends over time", "line"),
        ]
        
        for question, expected_type in chart_questions:
            response = agent.ask(question)
            assert 'chart_data' in response
            if response['chart_data']:
                assert 'type' in response['chart_data']
                assert response['chart_data']['type'] == expected_type
                assert 'x' in response['chart_data']
                assert 'y' in response['chart_data']
                print(f"[OK] {question} -> {expected_type} chart generated")
    
    def test_vague_questions(self, agent, sample_data):
        """Test handling of vague questions"""
        agent.load_data(sample_data)
        
        vague_questions = [
            "hello",
            "how are you?",
            "what is the weather?",
            "tell me a joke"
        ]
        
        for question in vague_questions:
            response = agent.ask(question)
            assert 'answer' in response
            # Vague questions should have guidance
            assert any(keyword in response['answer'].lower() for keyword in ['help', 'data', 'ask', 'questions'])
            print(f"[OK] {question} -> Handled gracefully")
    
    def test_no_data_scenario(self, agent):
        """Test behavior when no data is loaded"""
        response = agent.ask("what is the total revenue?")
        assert 'answer' in response
        assert 'no data' in response['answer'].lower() or 'load data' in response['answer'].lower()
        print("[OK] No data scenario handled")
    
    def test_confidence_scores(self, agent, sample_data):
        """Test confidence scores are reasonable"""
        agent.load_data(sample_data)
        
        questions = [
            "what is the total revenue?",  # Should have high confidence
            "something random",  # Should have low confidence
        ]
        
        for question in questions:
            response = agent.ask(question)
            assert 'confidence' in response
            assert 0 <= response['confidence'] <= 1
            print(f"[OK] {question} -> Confidence: {response['confidence']:.2f}")
    
    def test_edge_cases(self, agent, sample_data):
        """Test edge cases"""
        agent.load_data(sample_data)
        
        edge_cases = [
            "",  # Empty question
            "   ",  # Whitespace only
            "a" * 1000,  # Very long question
            "!@#$%^&*()",  # Special characters
        ]
        
        for question in edge_cases:
            try:
                response = agent.ask(question)
                assert 'answer' in response
                print(f"[OK] Edge case handled: {repr(question[:50])}")
            except Exception as e:
                print(f"[WARN] Edge case failed: {repr(question[:50])} -> {e}")


class TestChartTypes:
    """Test different chart types"""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance"""
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/retail_demo.csv')
        agent.load_data(df)
        return agent
    
    def test_bar_chart(self, agent):
        """Test bar chart generation"""
        response = agent.ask("show me top 5 products")
        assert response['chart_data'] is not None
        assert response['chart_data']['type'] == 'bar'
        assert len(response['chart_data']['x']) > 0
        assert len(response['chart_data']['y']) > 0
        print("[OK] Bar chart generated successfully")
    
    def test_line_chart(self, agent):
        """Test line chart generation"""
        response = agent.ask("show trends over time")
        assert response['chart_data'] is not None
        assert response['chart_data']['type'] == 'line'
        print("[OK] Line chart generated successfully")
    
    def test_chart_data_format(self, agent):
        """Test chart data has correct format"""
        response = agent.ask("top products")
        if response['chart_data']:
            chart = response['chart_data']
            assert 'type' in chart
            assert 'x' in chart
            assert 'y' in chart
            assert 'title' in chart
            assert len(chart['x']) == len(chart['y'])
            print("[OK] Chart data format is correct")


class TestDataTypes:
    """Test with different data types"""
    
    def test_sales_data(self):
        """Test with sales data"""
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/retail_demo.csv')
        agent.load_data(df)
        
        response = agent.ask("what is the total revenue?")
        assert 'answer' in response
        print("[OK] Sales data processed successfully")
    
    def test_ecommerce_data(self):
        """Test with ecommerce data"""
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/ecommerce_demo.csv')
        agent.load_data(df)
        
        response = agent.ask("what is the total?")
        assert 'answer' in response
        print("[OK] Ecommerce data processed successfully")
    
    def test_customer_data(self):
        """Test with customer data"""
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/customer_records.csv')
        agent.load_data(df)
        
        response = agent.ask("how many customers?")
        assert 'answer' in response
        print("[OK] Customer data processed successfully")


class TestPerformance:
    """Test performance and speed"""
    
    def test_response_time(self):
        """Test response time is reasonable"""
        import time
        
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/retail_demo.csv')
        agent.load_data(df)
        
        start_time = time.time()
        response = agent.ask("what is the total revenue?")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0  # Should respond within 2 seconds
        print(f"[OK] Response time: {response_time:.2f}s")
    
    def test_chart_generation_time(self):
        """Test chart generation time"""
        import time
        
        agent = OpenAIAnalyticsAgent()
        df = pd.read_csv('data/sample/retail_demo.csv')
        agent.load_data(df)
        
        start_time = time.time()
        response = agent.ask("show me top 5 products")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 3.0  # Should generate chart within 3 seconds
        print(f"[OK] Chart generation time: {response_time:.2f}s")


if __name__ == "__main__":
    print("🧪 Running Comprehensive Chatbot Tests...")
    print("=" * 60)
    pytest.main([__file__, "-v", "--tb=short"])

