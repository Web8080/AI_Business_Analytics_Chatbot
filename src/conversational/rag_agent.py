"""
Advanced RAG-Based Conversational Agent
Auto-generates analytics and visualizations based on natural language questions
"""
from typing import Dict, Any, Optional, List
import pandas as pd
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


class RAGAnalyticsAgent:
    """
    Advanced conversational agent with RAG capabilities
    Automatically generates analytics and visualizations based on questions
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        """Initialize RAG agent"""
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.1
        )
        self.conversation_history = []
        self.current_data = None
        self.data_context = None
        
    def load_data_context(self, df: pd.DataFrame, metadata: Dict[str, Any]):
        """Load and create context from dataframe"""
        self.current_data = df
        
        # Create rich context about the data
        self.data_context = {
            'shape': f"{len(df)} rows × {len(df.columns)} columns",
            'columns': df.columns.tolist(),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'date_columns': [col for col in df.columns if 'date' in col.lower()],
            'sample_data': df.head(3).to_dict('records'),
            'summary_stats': {
                col: {
                    'mean': float(df[col].mean()),
                    'sum': float(df[col].sum()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                } for col in df.select_dtypes(include=['number']).columns
            }
        }
        
    def query_with_analytics(self, question: str) -> Dict[str, Any]:
        """
        Process question and return answer with analytics and visualizations
        
        Returns:
            {
                'answer': str,
                'analytics': Dict,
                'visualizations': List[Dict],
                'confidence': float,
                'recommendations': List[str]
            }
        """
        if self.current_data is None:
            return {
                'answer': 'Please upload data first.',
                'analytics': {},
                'visualizations': [],
                'confidence': 0.0
            }
        
        # Step 1: Analyze the question and determine what analytics to run
        analytics_plan = self._plan_analytics(question)
        
        # Step 2: Execute analytics
        analytics_results = self._execute_analytics(analytics_plan)
        
        # Step 3: Generate visualizations
        visualizations = self._generate_visualizations(question, analytics_results)
        
        # Step 4: Generate natural language response
        answer = self._generate_answer(question, analytics_results, visualizations)
        
        # Step 5: Generate recommendations
        recommendations = self._generate_recommendations(question, analytics_results)
        
        return {
            'answer': answer,
            'analytics': analytics_results,
            'visualizations': visualizations,
            'confidence': analytics_plan.get('confidence', 0.8),
            'recommendations': recommendations
        }
    
    def _plan_analytics(self, question: str) -> Dict[str, Any]:
        """Use LLM to plan what analytics to run"""
        
        planning_prompt = f"""Given this question about data: "{question}"

Data context:
- Columns: {', '.join(self.data_context['columns'])}
- Numeric columns: {', '.join(self.data_context['numeric_columns'])}
- Rows: {self.data_context['shape']}

Determine what analytics to perform. Return JSON with:
{{
    "analytics_type": "descriptive|diagnostic|predictive|prescriptive",
    "operations": ["operation1", "operation2"],
    "target_columns": ["col1", "col2"],
    "visualization_types": ["chart_type1", "chart_type2"],
    "confidence": 0.0-1.0
}}

Examples:
- "What is total revenue?" → {{"analytics_type": "descriptive", "operations": ["sum"], "target_columns": ["revenue"]}}
- "Why did sales drop?" → {{"analytics_type": "diagnostic", "operations": ["trend_analysis", "segment_comparison"]}}
- "Forecast next month" → {{"analytics_type": "predictive", "operations": ["forecast"], "visualization_types": ["time_series"]}}
"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an analytics planning expert. Always return valid JSON."),
                HumanMessage(content=planning_prompt)
            ])
            
            # Parse response
            plan = json.loads(response.content)
            return plan
            
        except Exception as e:
            logger.error(f"Planning error: {e}")
            # Fallback to rule-based planning
            return self._fallback_planning(question)
    
    def _fallback_planning(self, question: str) -> Dict[str, Any]:
        """Fallback rule-based planning"""
        question_lower = question.lower()
        
        if 'total' in question_lower or 'sum' in question_lower:
            return {
                'analytics_type': 'descriptive',
                'operations': ['sum', 'count'],
                'target_columns': self.data_context['numeric_columns'],
                'visualization_types': ['bar_chart'],
                'confidence': 0.9
            }
        elif 'trend' in question_lower or 'over time' in question_lower:
            return {
                'analytics_type': 'descriptive',
                'operations': ['trend_analysis'],
                'target_columns': self.data_context['date_columns'] + self.data_context['numeric_columns'][:1],
                'visualization_types': ['time_series'],
                'confidence': 0.85
            }
        elif 'forecast' in question_lower or 'predict' in question_lower:
            return {
                'analytics_type': 'predictive',
                'operations': ['forecast'],
                'target_columns': self.data_context['numeric_columns'][:1],
                'visualization_types': ['forecast_chart'],
                'confidence': 0.8
            }
        elif 'top' in question_lower or 'best' in question_lower:
            return {
                'analytics_type': 'descriptive',
                'operations': ['ranking'],
                'target_columns': self.data_context['categorical_columns'][:1] + self.data_context['numeric_columns'][:1],
                'visualization_types': ['bar_chart'],
                'confidence': 0.9
            }
        else:
            return {
                'analytics_type': 'descriptive',
                'operations': ['summary'],
                'target_columns': self.data_context['numeric_columns'],
                'visualization_types': [],
                'confidence': 0.7
            }
    
    def _execute_analytics(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planned analytics"""
        results = {}
        df = self.current_data
        
        for operation in plan.get('operations', []):
            if operation == 'sum':
                for col in plan.get('target_columns', []):
                    if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                        results[f'{col}_sum'] = float(df[col].sum())
            
            elif operation == 'count':
                results['total_count'] = len(df)
            
            elif operation == 'ranking':
                cols = plan.get('target_columns', [])
                if len(cols) >= 2:
                    cat_col, num_col = cols[0], cols[1]
                    if cat_col in df.columns and num_col in df.columns:
                        top = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(5)
                        results['top_items'] = top.to_dict()
            
            elif operation == 'trend_analysis':
                # Simple trend
                numeric_cols = [c for c in plan.get('target_columns', []) if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
                if numeric_cols:
                    for col in numeric_cols[:1]:
                        results[f'{col}_trend'] = {
                            'mean': float(df[col].mean()),
                            'std': float(df[col].std()),
                            'min': float(df[col].min()),
                            'max': float(df[col].max())
                        }
        
        return results
    
    def _generate_visualizations(self, question: str, analytics_results: Dict) -> List[Dict[str, Any]]:
        """Generate visualization specifications"""
        visualizations = []
        
        # For now, return specs that the UI can render
        if 'top_items' in analytics_results:
            visualizations.append({
                'type': 'bar_chart',
                'data': analytics_results['top_items'],
                'title': 'Top Items by Performance'
            })
        
        return visualizations
    
    def _generate_answer(self, question: str, analytics: Dict, visualizations: List) -> str:
        """Generate natural language answer using LLM"""
        
        prompt = f"""Question: {question}

Data Analysis Results:
{json.dumps(analytics, indent=2)}

Visualizations Generated: {len(visualizations)}

Provide a clear, concise answer to the question using the analysis results.
Include specific numbers and insights.
Format with markdown for readability.
"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a helpful analytics assistant. Provide clear, data-driven answers."),
                HumanMessage(content=prompt)
            ])
            return response.content
        except Exception as e:
            # Fallback to template-based response
            return self._generate_template_answer(analytics)
    
    def _generate_template_answer(self, analytics: Dict) -> str:
        """Template-based answer generation"""
        answer_parts = []
        
        for key, value in analytics.items():
            if 'sum' in key:
                answer_parts.append(f"**Total {key.replace('_sum', '')}:** ${value:,.2f}")
            elif key == 'total_count':
                answer_parts.append(f"**Total records:** {value}")
            elif 'top_items' in key:
                answer_parts.append(f"**Top performers identified:** {len(value)} items")
        
        return "\n\n".join(answer_parts) if answer_parts else "Analysis completed successfully."
    
    def _generate_recommendations(self, question: str, analytics: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Simple recommendation logic
        if 'top_items' in analytics:
            recommendations.append("Focus resources on top-performing items")
            recommendations.append("Investigate why bottom items are underperforming")
        
        return recommendations

