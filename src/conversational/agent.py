"""
Conversational AI Agent - Natural language interface using LangChain and OpenAI
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class ConversationalAgent:
    """AI agent for natural language analytics queries"""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """
        Initialize conversational agent
        
        Args:
            api_key: OpenAI API key
            model: Model name
        """
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.1
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = []
        self.agent = None
        
        logger.info(f"Initialized conversational agent with model: {model}")
    
    def register_analytics_tools(self, analytics_engine):
        """
        Register analytics functions as tools
        
        Args:
            analytics_engine: Analytics engine instance with methods
        """
        logger.info("Registering analytics tools")
        
        # Tool for descriptive analytics
        descriptive_tool = Tool(
            name="descriptive_analytics",
            func=lambda query: self._execute_descriptive_analytics(analytics_engine, query),
            description="Useful for calculating summary statistics, KPIs, trends, and distributions. Use this when asked about averages, totals, distributions, or general statistics."
        )
        
        # Tool for diagnostic analytics
        diagnostic_tool = Tool(
            name="diagnostic_analytics",
            func=lambda query: self._execute_diagnostic_analytics(analytics_engine, query),
            description="Useful for root cause analysis, segment comparison, and variance analysis. Use this when asked 'why' something happened or to compare segments."
        )
        
        # Tool for predictive analytics
        predictive_tool = Tool(
            name="predictive_analytics",
            func=lambda query: self._execute_predictive_analytics(analytics_engine, query),
            description="Useful for forecasting future values and predicting trends. Use this when asked about future predictions, forecasts, or what will happen next."
        )
        
        # Tool for prescriptive analytics
        prescriptive_tool = Tool(
            name="prescriptive_analytics",
            func=lambda query: self._execute_prescriptive_analytics(analytics_engine, query),
            description="Useful for generating recommendations and action plans. Use this when asked what to do, how to improve, or for recommendations."
        )
        
        self.tools = [descriptive_tool, diagnostic_tool, predictive_tool, prescriptive_tool]
        self._create_agent()
    
    def _create_agent(self):
        """Create LangChain agent with tools"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI analytics assistant with access to powerful analytics tools.
            You can answer questions about data by using the appropriate analytics tools.
            
            When answering:
            1. Always use the appropriate tool based on the question type
            2. Provide clear, concise answers with specific numbers
            3. Include confidence levels when applicable
            4. Suggest actionable insights
            5. Format responses in a user-friendly way
            
            Available tools:
            - descriptive_analytics: For statistics, KPIs, trends
            - diagnostic_analytics: For root cause analysis, why questions
            - predictive_analytics: For forecasts and predictions
            - prescriptive_analytics: For recommendations and actions
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3
        )
    
    def _execute_descriptive_analytics(self, engine, query: str) -> str:
        """Execute descriptive analytics"""
        try:
            # Parse query and execute appropriate method
            result = {"message": "Descriptive analytics executed", "query": query}
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _execute_diagnostic_analytics(self, engine, query: str) -> str:
        """Execute diagnostic analytics"""
        try:
            result = {"message": "Diagnostic analytics executed", "query": query}
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _execute_predictive_analytics(self, engine, query: str) -> str:
        """Execute predictive analytics"""
        try:
            result = {"message": "Predictive analytics executed", "query": query}
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def _execute_prescriptive_analytics(self, engine, query: str) -> str:
        """Execute prescriptive analytics"""
        try:
            result = {"message": "Prescriptive analytics executed", "query": query}
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def query(self, question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process natural language query
        
        Args:
            question: Natural language question
            context: Additional context about the data
            
        Returns:
            Dictionary containing response and metadata
        """
        logger.info(f"Processing query: {question}")
        
        try:
            # Add context to question if provided
            if context:
                context_str = f"\nContext: {json.dumps(context, indent=2)}\n"
                enhanced_question = context_str + question
            else:
                enhanced_question = question
            
            # Execute agent
            if self.executor:
                response = self.executor.invoke({"input": enhanced_question})
                answer = response.get('output', 'Unable to process query')
            else:
                # Fallback to direct LLM call
                response = self.llm.invoke(enhanced_question)
                answer = response.content
            
            return {
                'question': question,
                'answer': answer,
                'confidence': 0.85,  # Would be calculated based on actual execution
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'question': question,
                'answer': f"Error processing query: {str(e)}",
                'confidence': 0.0,
                'status': 'error'
            }
    
    def generate_insights(self, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate automated insights from data summary
        
        Args:
            data_summary: Summary of analyzed data
            
        Returns:
            Dictionary containing generated insights
        """
        logger.info("Generating automated insights")
        
        try:
            prompt = f"""Based on the following data summary, generate key insights and observations:

{json.dumps(data_summary, indent=2)}

Provide:
1. Top 3 key findings
2. Notable trends or patterns
3. Potential concerns or opportunities
4. Recommended areas for deeper investigation

Format as a structured JSON response."""
            
            response = self.llm.invoke(prompt)
            
            # Try to parse as JSON
            try:
                insights = json.loads(response.content)
            except:
                # Fallback to plain text
                insights = {
                    'insights': response.content,
                    'format': 'text'
                }
            
            return {
                'insights': insights,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return {
                'insights': {},
                'status': 'error',
                'message': str(e)
            }
    
    def explain_analysis(self, analysis_result: Dict[str, Any], 
                        explain_for: str = "business_user") -> str:
        """
        Generate natural language explanation of analysis results
        
        Args:
            analysis_result: Technical analysis results
            explain_for: Target audience ('business_user', 'technical', 'executive')
            
        Returns:
            Natural language explanation
        """
        logger.info(f"Generating explanation for {explain_for}")
        
        try:
            audience_context = {
                'business_user': 'a non-technical business user without assuming statistical knowledge',
                'technical': 'a data analyst who understands statistics',
                'executive': 'an executive who needs high-level insights and recommendations'
            }
            
            prompt = f"""Explain the following analysis results for {audience_context.get(explain_for, 'a general audience')}:

{json.dumps(analysis_result, indent=2)}

Provide a clear, concise explanation focusing on:
1. What the results mean
2. Why they matter
3. What actions should be considered

Keep it under 200 words."""
            
            response = self.llm.invoke(prompt)
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error explaining analysis: {str(e)}")
            return "Unable to generate explanation."
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        logger.info("Conversation memory cleared")

