"""
OpenAI- and Ollama-powered Analytics Agent
Uses OpenAI when API key is set; otherwise Ollama (works in production if Ollama runs on a server).
Falls back to rule-based system when neither is available.
"""
import os
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Try to import OpenAI, fallback gracefully if not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI package not available. Using fallback system.")

from .smart_agent import SmartAnalyticsAgent

logger = logging.getLogger(__name__)


def _call_ollama(base_url: str, model: str, prompt: str, timeout: int = 60) -> Tuple[str, bool]:
    """Call Ollama /api/chat. Works in production if base_url points to your Ollama server."""
    url = (base_url.rstrip("/") + "/api/chat").replace("//api", "/api")
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert data analyst. Answer concisely with specific numbers and insights."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
            msg = data.get("message") or {}
            answer = (msg.get("content") or "").strip()
            return answer, bool(answer)
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        logger.warning("Ollama request failed: %s", e)
        return "", False


class OpenAIAnalyticsAgent(SmartAnalyticsAgent):
    """
    Analytics agent: OpenAI (if key set), else Ollama, else rule-based.
    Ollama works in production when OLLAMA_BASE_URL points to your Ollama server.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or ""
        self.openai_available = OPENAI_AVAILABLE and bool(self.api_key)
        self.openai_client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                openai.api_key = self.api_key
                self.openai_client = openai
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error("Failed to initialize OpenAI client: %s", e)
                self.openai_available = False
        
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2").strip()
        self.ollama_available = bool(self.ollama_base_url and self.ollama_model)
        
        if not self.openai_available and self.ollama_available:
            logger.info("Using Ollama at %s with model %s", self.ollama_base_url, self.ollama_model)
        elif not self.openai_available:
            logger.info("Using fallback rule-based system")
    
    def _build_data_context(self, df: pd.DataFrame) -> str:
        """Build comprehensive data context for OpenAI prompts"""
        context = f"""
        DATASET OVERVIEW:
        - Shape: {df.shape[0]} rows × {df.shape[1]} columns
        - Columns: {', '.join(df.columns.tolist())}
        
        COLUMN DETAILS:
        """
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            non_null = df[col].count()
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            
            context += f"""
        - {col}: {dtype} ({non_null} non-null, {null_count} null, {unique_count} unique)"""
            
            # Add sample values for categorical/string columns
            if df[col].dtype == 'object' or df[col].nunique() < 20:
                sample_values = df[col].dropna().head(5).tolist()
                context += f" [Sample: {sample_values}]"
        
        context += f"""
        
        DATA SUMMARY:
        - Numeric columns: {', '.join(df.select_dtypes(include=['number']).columns.tolist())}
        - Categorical columns: {', '.join(df.select_dtypes(include=['object']).columns.tolist())}
        - Date columns: {', '.join(df.select_dtypes(include=['datetime']).columns.tolist())}
        """
        
        return context
    
    def _build_analytics_context(self, question: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Build analytics context for better responses"""
        analytics_context = {
            "basic_stats": {},
            "column_info": {},
            "suggested_analyses": []
        }
        
        # Basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            analytics_context["basic_stats"] = df[numeric_cols].describe().to_dict()
        
        # Column information
        for col in df.columns:
            analytics_context["column_info"][col] = {
                "dtype": str(df[col].dtype),
                "null_count": df[col].isnull().sum(),
                "unique_count": df[col].nunique(),
                "sample_values": df[col].dropna().head(3).tolist()
            }
        
        # Suggest analyses based on question and data
        if "total" in question.lower() or "sum" in question.lower():
            analytics_context["suggested_analyses"].append("aggregation")
        if "average" in question.lower() or "mean" in question.lower():
            analytics_context["suggested_analyses"].append("statistical_summary")
        if "top" in question.lower() or "best" in question.lower():
            analytics_context["suggested_analyses"].append("ranking")
        if "trend" in question.lower() or "time" in question.lower():
            analytics_context["suggested_analyses"].append("trend_analysis")
        if "compare" in question.lower():
            analytics_context["suggested_analyses"].append("comparison")
        
        return analytics_context
    
    def _create_openai_prompt(self, question: str, df: pd.DataFrame) -> str:
        """Create optimized prompt for OpenAI"""
        
        data_context = self._build_data_context(df)
        analytics_context = self._build_analytics_context(question, df)
        
        prompt = f"""You are an expert data analyst and AI assistant specializing in business analytics. 
        Your role is to analyze data and provide insightful, accurate responses with visualizations when appropriate.

        {data_context}

        USER QUESTION: {question}

        ANALYTICS CONTEXT:
        {json.dumps(analytics_context, indent=2)}

        INSTRUCTIONS:
        1. Analyze the user's question in the context of the provided dataset
        2. Provide a clear, actionable answer with specific numbers and insights
        3. If the question requires visualization, indicate what type of chart would be helpful
        4. Be specific about which columns and data you're analyzing
        5. If the question is unclear or irrelevant to the data, politely redirect them
        6. Always provide confidence in your analysis

        RESPONSE FORMAT:
        - Start with a direct answer to the question
        - Provide supporting analysis and insights
        - Mention specific data points and statistics
        - Suggest follow-up questions if relevant
        - End with confidence level (High/Medium/Low)

        Keep your response concise but comprehensive (2-4 paragraphs max)."""

        return prompt
    
    def _call_openai(self, prompt: str) -> Tuple[str, bool]:
        """Call OpenAI API with error handling"""
        if not self.openai_available or not self.openai_client:
            return "", False
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert data analyst with deep knowledge of business analytics, statistics, and data visualization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,
                timeout=30
            )
            
            answer = response.choices[0].message.content.strip()
            return answer, True
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return "", False
    
    def _determine_chart_type(self, question: str, answer: str, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Determine if a chart should be generated and what type"""
        
        # Keywords that suggest chart generation
        chart_keywords = {
            "bar": ["top", "best", "worst", "highest", "lowest", "compare", "ranking", "chart", "show me a chart"],
            "line": ["trend", "over time", "time series", "evolution", "change"],
            "pie": ["percentage", "proportion", "share", "breakdown", "distribution"],
            "scatter": ["correlation", "relationship", "scatter", "plot"],
            "histogram": ["distribution", "frequency", "histogram"]
        }
        
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Determine chart type based on question and answer
        for chart_type, keywords in chart_keywords.items():
            if any(keyword in question_lower or keyword in answer_lower for keyword in keywords):
                return self._generate_chart_data(chart_type, question, df)
        
        return None
    
    def _generate_chart_data(self, chart_type: str, question: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate chart data based on question and data. Returns flat x/y for frontend Recharts."""
        try:
            if chart_type == "bar":
                question_lower = question.lower()
                # Prefer product/category + quantity or first numeric for "highest quantity" style
                cat_cols = df.select_dtypes(include=["object"]).columns
                num_cols = df.select_dtypes(include=["number"]).columns
                if "quantity" in question_lower or "product" in question_lower:
                    qty_col = next((c for c in num_cols if "quantity" in c.lower() or "qty" in c.lower()), None)
                    prod_col = next((c for c in cat_cols if "product" in c.lower() or "item" in c.lower()), cat_cols[0] if len(cat_cols) else None)
                    if qty_col is not None and prod_col is not None:
                        grouped = df.groupby(prod_col)[qty_col].sum().sort_values(ascending=False).head(10)
                        return {
                            "type": "bar",
                            "title": f"Top 10 by {qty_col}",
                            "x": grouped.index.tolist(),
                            "y": grouped.values.tolist(),
                        }
                if len(num_cols) > 0:
                    col = num_cols[0]
                    top_data = df.nlargest(10, col)
                    if len(cat_cols) > 0:
                        cat_col = cat_cols[0]
                        if cat_col in top_data.columns:
                            x_vals = top_data[cat_col].tolist()
                        else:
                            x_vals = top_data.index.astype(str).tolist()
                    else:
                        x_vals = top_data.index.astype(str).tolist()
                    return {
                        "type": "bar",
                        "title": f"Top 10 by {col}",
                        "x": x_vals,
                        "y": top_data[col].tolist(),
                    }
            
            elif chart_type == "line":
                # Look for date/time columns
                date_cols = df.select_dtypes(include=['datetime', 'object']).columns
                numeric_cols = df.select_dtypes(include=['number']).columns
                
                if len(date_cols) > 0 and len(numeric_cols) > 0:
                    # Try to convert first column to datetime
                    try:
                        df_temp = df.copy()
                        df_temp[date_cols[0]] = pd.to_datetime(df_temp[date_cols[0]])
                        df_temp = df_temp.sort_values(date_cols[0])
                        
                        chart_data = {
                            "data": [
                                {
                                    "x": df_temp[date_cols[0]].tolist(),
                                    "y": df_temp[numeric_cols[0]].tolist(),
                                    "type": "scatter",
                                    "mode": "lines",
                                    "name": numeric_cols[0]
                                }
                            ],
                            "layout": {
                                "title": f"{numeric_cols[0]} over time",
                                "template": "plotly_dark"
                            }
                        }
                        return {
                            "type": "line",
                            "data": chart_data,
                            "title": f"{numeric_cols[0]} over time"
                        }
                    except:
                        pass
            
            elif chart_type == "pie":
                # Find categorical column
                categorical_cols = df.select_dtypes(include=['object']).columns
                if len(categorical_cols) > 0:
                    col = categorical_cols[0]
                    value_counts = df[col].value_counts().head(8)
                    
                    chart_data = {
                        "data": [
                            {
                                "values": value_counts.values.tolist(),
                                "labels": value_counts.index.tolist(),
                                "type": "pie"
                            }
                        ],
                        "layout": {
                            "title": f"Distribution of {col}",
                            "template": "plotly_dark"
                        }
                    }
                    return {
                        "type": "pie",
                        "data": chart_data,
                        "title": f"Distribution of {col}"
                    }
            
        except Exception as e:
            logger.error(f"Chart generation failed: {e}")
        
        return None
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask a question using OpenAI with fallback to rule-based system
        """
        if not hasattr(self, 'current_data') or self.current_data is None:
            return {
                'answer': "Please load data first before asking questions.",
                'confidence': 0.0,
                'chart_data': None
            }
        
        # Check if question is vague or irrelevant
        vague_response = self._check_if_vague_or_irrelevant(question)
        if vague_response and vague_response.get('is_vague', False):
            return {
                'answer': vague_response.get('guidance_message', 'Please ask a more specific question about your data.'),
                'confidence': 0.8,
                'chart_data': None
            }
        
        # Try OpenAI first if available
        if self.openai_available and self.openai_client:
            logger.info("Using OpenAI for question analysis")
            try:
                prompt = self._create_openai_prompt(question, self.current_data)
                answer, success = self._call_openai(prompt)
                if success and answer:
                    chart_data = self._determine_chart_type(question, answer, self.current_data)
                    return {
                        "answer": answer,
                        "confidence": 0.9,
                        "chart_data": chart_data,
                        "source": "openai",
                    }
                logger.warning("OpenAI failed, trying Ollama or fallback")
            except Exception as e:
                logger.error("OpenAI error: %s", e)
        
        # Try Ollama if configured (works in production when Ollama runs on a server)
        if self.ollama_available:
            logger.info("Using Ollama for question analysis")
            try:
                prompt = self._create_openai_prompt(question, self.current_data)
                answer, success = _call_ollama(self.ollama_base_url, self.ollama_model, prompt)
                if success and answer:
                    chart_data = self._determine_chart_type(question, answer, self.current_data)
                    return {
                        "answer": answer,
                        "confidence": 0.85,
                        "chart_data": chart_data,
                        "source": "ollama",
                    }
                logger.warning("Ollama failed, using rule-based fallback")
            except Exception as e:
                logger.error("Ollama error: %s", e)
        
        # Fallback to rule-based system
        logger.info("Using rule-based fallback system")
        try:
            fallback_response = super().ask(question)
            fallback_response['source'] = 'fallback'
            return fallback_response
        except Exception as e:
            logger.error(f"Fallback system error: {e}")
            return {
                'answer': f"I encountered an error while processing your question: {str(e)}. Please try rephrasing your question or check if the data is properly loaded.",
                'confidence': 0.3,
                'chart_data': None,
                'source': 'fallback_error'
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and capabilities"""
        return {
            "openai_available": self.openai_available,
            "ollama_available": self.ollama_available,
            "api_key_configured": bool(self.api_key),
            "fallback_system": True,
            "capabilities": [
                "Natural language data analysis",
                "Automatic chart generation",
                "Statistical insights",
                "Context-aware responses",
                "Robust fallback system",
            ],
        }
