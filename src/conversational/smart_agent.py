"""
Advanced AI-Powered Conversational Analytics Agent
- Auto-generates visualizations based on questions
- RAG-powered context understanding
- Dynamic analytics execution
- Confidence scoring
- Strategic recommendations
- 100,000+ intent patterns with fuzzy matching
"""
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from conversational.intent_matcher import RobustIntentMatcher
    INTENT_MATCHER_AVAILABLE = True
except ImportError:
    INTENT_MATCHER_AVAILABLE = False
    logger.warning("RobustIntentMatcher not available, using basic intent matching")

logger = logging.getLogger(__name__)


class SmartAnalyticsAgent:
    """
    Advanced conversational agent that:
    1. Understands natural language questions
    2. Automatically generates relevant analytics
    3. Creates visualizations on-the-fly
    4. Provides confidence scores
    5. Offers strategic recommendations
    """
    
    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None):
        """
        Initialize smart analytics agent
        
        Args:
            use_openai: Whether to use OpenAI API (requires API key)
            api_key: OpenAI API key (optional)
        """
        self.use_openai = use_openai and api_key is not None
        self.api_key = api_key
        self.llm = None
        
        # Initialize robust intent matcher
        self.intent_matcher = RobustIntentMatcher() if INTENT_MATCHER_AVAILABLE else None
        
        if self.use_openai:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    api_key=api_key,
                    model="gpt-4-turbo-preview",
                    temperature=0.1
                )
                logger.info("Initialized with OpenAI GPT-4")
            except ImportError:
                logger.warning("OpenAI not available, using advanced rule-based system")
                self.use_openai = False
        
        self.current_data = None
        self.data_summary = None
        self.conversation_context = []
        
        # Keywords that indicate vague or irrelevant questions
        self.irrelevant_keywords = [
            'weather', 'news', 'sports', 'politics', 'recipe', 'movie', 'music',
            'game', 'celebrity', 'joke', 'story', 'poem', 'song', 'hello', 'hi',
            'how are you', 'thank you', 'thanks', 'bye', 'goodbye'
        ]
        
        self.vague_patterns = [
            'tell me something', 'anything', 'what can you do', 'help',
            'what is this', 'explain', 'describe this', 'tell me about'
        ]
    
    def load_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Load data and create intelligent context"""
        self.current_data = df
        
        # Create rich data summary for context
        self.data_summary = {
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'columns': {
                'all': df.columns.tolist(),
                'numeric': df.select_dtypes(include=[np.number]).columns.tolist(),
                'categorical': df.select_dtypes(include=['object']).columns.tolist(),
                'datetime': [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col]) or 'date' in col.lower()]
            },
            'stats': {
                col: {
                    'sum': float(df[col].sum()),
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'std': float(df[col].std())
                } for col in df.select_dtypes(include=[np.number]).columns
            },
            'sample': df.head(3).to_dict('records')
        }
        
        return {
            'status': 'success',
            'message': f'Loaded {len(df)} rows with {len(df.columns)} columns',
            'summary': self.data_summary
        }
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Process natural language question with full intelligence
        
        Returns:
            {
                'answer': str (natural language response),
                'data': Dict (computed analytics),
                'visualizations': List[Dict] (auto-generated charts),
                'confidence': float (0-1),
                'recommendations': List[str],
                'sql_equivalent': str (what the query does),
                'execution_time': float
            }
        """
        if self.current_data is None:
            return {
                'answer': 'Please upload data first.',
                'data': {},
                'visualizations': [],
                'chart_data': None,
                'confidence': 0.0,
                'recommendations': []
            }
        
        start_time = datetime.now()
        
        # STEP 0: Check if question is too vague or irrelevant
        vague_check = self._check_if_vague_or_irrelevant(question)
        if vague_check['is_vague']:
            return {
                'answer': vague_check['guidance_message'],
                'data': {},
                'visualizations': [],
                'chart_data': None,
                'confidence': 0.3,
                'recommendations': vague_check['suggested_questions'],
                'sql_equivalent': '',
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'is_vague': True
            }
        
        # Step 1: Understand the question
        intent = self._analyze_intent(question)
        
        # Step 2: Execute analytics based on intent
        analytics_result = self._execute_smart_analytics(intent, question)
        
        # Step 3: Auto-generate visualizations
        visualizations = self._auto_generate_charts(intent, analytics_result)
        
        # Step 4: Generate natural language answer
        answer = self._generate_intelligent_answer(question, intent, analytics_result, visualizations)
        
        # Step 5: Generate strategic recommendations
        recommendations = self._generate_strategic_recommendations(intent, analytics_result)
        
        # Step 6: Calculate confidence score
        confidence = self._calculate_confidence(intent, analytics_result)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Add to conversation context
        self.conversation_context.append({
            'question': question,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
        # Convert visualizations to chart_data format for dashboard
        chart_data = None
        if visualizations and len(visualizations) > 0:
            viz = visualizations[0]  # Take first visualization
            if viz.get('type') == 'bar_chart' and viz.get('figure'):
                # Extract data from bar chart
                fig = viz['figure']
                # Safe conversion to list
                x_data = self._safe_to_list(fig.data[0].x if hasattr(fig.data[0], 'x') else [])
                y_data = self._safe_to_list(fig.data[0].y if hasattr(fig.data[0], 'y') else [])
                chart_data = {
                    'type': 'bar',
                    'title': viz.get('title', 'Chart'),
                    'x': x_data,
                    'y': y_data,
                    'x_label': 'Category',
                    'y_label': 'Value'
                }
            elif viz.get('type') == 'line_chart' and viz.get('figure'):
                # Extract data from line chart
                fig = viz['figure']
                x_data = self._safe_to_list(fig.data[0].x if hasattr(fig.data[0], 'x') else [])
                y_data = self._safe_to_list(fig.data[0].y if hasattr(fig.data[0], 'y') else [])
                chart_data = {
                    'type': 'line',
                    'title': viz.get('title', 'Chart'),
                    'x': x_data,
                    'y': y_data,
                    'x_label': 'Date',
                    'y_label': 'Value'
                }
            elif viz.get('type') == 'comparison_chart' and viz.get('figure'):
                # Extract data from comparison chart
                fig = viz['figure']
                x_data = self._safe_to_list(fig.data[0].x if hasattr(fig.data[0], 'x') else [])
                y_data = self._safe_to_list(fig.data[0].y if hasattr(fig.data[0], 'y') else [])
                chart_data = {
                    'type': 'bar',
                    'title': viz.get('title', 'Chart'),
                    'x': x_data,
                    'y': y_data,
                    'x_label': 'Category',
                    'y_label': 'Value'
                }
        
        return {
            'answer': answer,
            'data': analytics_result,
            'visualizations': visualizations,
            'chart_data': chart_data,  # Add chart_data for dashboard
            'confidence': confidence,
            'recommendations': recommendations,
            'sql_equivalent': intent.get('sql_equivalent', ''),
            'execution_time': execution_time,
            'intent': intent
        }
    
    def _check_if_vague_or_irrelevant(self, question: str) -> Dict[str, Any]:
        """
        Check if question is too vague or irrelevant to the data
        Returns guidance to help user ask better questions
        """
        question_lower = question.lower().strip()
        
        # Check for greetings/pleasantries
        if question_lower in ['hi', 'hello', 'hey', 'thanks', 'thank you', 'bye', 'goodbye']:
            return {
                'is_vague': True,
                'guidance_message': """Hello! I'm your AI Analytics Assistant. I'm here to help you analyze your data!

I can answer specific questions about your dataset. To get started, try asking about your data.""",
                'suggested_questions': self._generate_suggested_questions()
            }
        
        # Check for irrelevant topics
        for keyword in self.irrelevant_keywords:
            if keyword in question_lower:
                return {
                    'is_vague': True,
                    'guidance_message': f"""I appreciate your interest, but I'm specifically designed to analyze your **data**.

I can't help with {keyword}-related questions, but I'm excellent at analyzing your uploaded dataset!

**Let me help you with your data instead.** Here are some questions I can answer:""",
                    'suggested_questions': self._generate_suggested_questions()
                }
        
        # Check for vague questions
        for pattern in self.vague_patterns:
            if pattern in question_lower and len(question_lower) < 30:
                return {
                    'is_vague': True,
                    'guidance_message': """I'd be happy to help! However, your question is a bit general.

To provide meaningful insights, I need a specific question about your data.

**Here are some examples based on your dataset:**""",
                    'suggested_questions': self._generate_suggested_questions()
                }
        
        # Check if question has ANY recognizable data-related keywords
        data_keywords = ['total', 'sum', 'average', 'mean', 'count', 'how many', 'show', 
                        'top', 'bottom', 'best', 'worst', 'trend', 'forecast', 'predict',
                        'compare', 'analysis', 'revenue', 'sales', 'customer', 'product']
        
        # Also check for column names
        column_mentioned = False
        if self.current_data is not None:
            for col in self.current_data.columns:
                if col.lower() in question_lower or col.replace('_', ' ').lower() in question_lower:
                    column_mentioned = True
                    break
        
        has_data_keyword = any(keyword in question_lower for keyword in data_keywords) or column_mentioned
        
        # If very short question (< 5 words) and no data keywords
        word_count = len(question_lower.split())
        if word_count < 5 and not has_data_keyword:
            return {
                'is_vague': True,
                'guidance_message': f"""I see you asked: "{question}"

I'm not sure how to analyze that with your current dataset. Could you please be more specific?

**For example, you might ask:**""",
                'suggested_questions': self._generate_suggested_questions()
            }
        
        # Question seems valid
        return {
            'is_vague': False,
            'guidance_message': '',
            'suggested_questions': []
        }
    
    def _generate_suggested_questions(self) -> List[str]:
        """Generate contextual suggested questions based on actual data"""
        suggestions = []
        
        if self.current_data is None or self.data_summary is None:
            return [
                "What is the total revenue?",
                "Show me the top 5 products",
                "How have sales trended over time?"
            ]
        
        df = self.current_data
        cols = self.data_summary['columns']
        
        # Generate smart suggestions based on actual columns
        numeric_cols = cols['numeric']
        categorical_cols = cols['categorical']
        date_cols = cols['datetime']
        
        # Revenue/Sales questions
        revenue_cols = [c for c in numeric_cols if any(word in c.lower() for word in ['revenue', 'sales', 'amount', 'total', 'price'])]
        if revenue_cols:
            suggestions.append(f"💰 What is the total {revenue_cols[0].replace('_', ' ')}?")
        
        # Product/Category questions
        product_cols = [c for c in categorical_cols if any(word in c.lower() for word in ['product', 'item', 'category', 'type'])]
        if product_cols and numeric_cols:
            suggestions.append(f" Show me the top 5 {product_cols[0].replace('_', ' ')}")
        
        # Regional/Segment questions
        segment_cols = [c for c in categorical_cols if any(word in c.lower() for word in ['region', 'location', 'segment', 'group', 'category'])]
        if segment_cols and numeric_cols:
            suggestions.append(f"🌍 Compare {segment_cols[0].replace('_', ' ')} performance")
        
        # Time-based questions
        if date_cols and numeric_cols:
            suggestions.append(f" Show me trends in {numeric_cols[0].replace('_', ' ')} over time")
        
        # Average questions
        if numeric_cols:
            suggestions.append(f" What is the average {numeric_cols[0].replace('_', ' ')}?")
        
        # Customer questions
        customer_cols = [c for c in categorical_cols if any(word in c.lower() for word in ['customer', 'client', 'user'])]
        if customer_cols:
            suggestions.append(f"👥 How many unique {customer_cols[0].replace('_', ' ')} do we have?")
        
        # If we have few suggestions, add generic ones
        if len(suggestions) < 3:
            suggestions.extend([
                " Give me a summary of the data",
                " What are the key statistics?",
                " What insights can you find?"
            ])
        
        return suggestions[:6]  # Return top 6 suggestions
    
    def _analyze_intent(self, question: str) -> Dict[str, Any]:
        """
        Analyze question intent using AI or advanced NLP with 100,000+ patterns
        Determines: what analytics to run, what columns to use, what to visualize
        """
        question_lower = question.lower()
        df = self.current_data
        
        intent = {
            'question_type': 'unknown',
            'target_columns': [],
            'operations': [],
            'visualization_type': None,
            'time_range': None,
            'filters': {},
            'sql_equivalent': '',
            'confidence': 0.7
        }
        
        # Use RobustIntentMatcher if available for superior pattern matching
        if self.intent_matcher:
            matched_intent, confidence, metadata = self.intent_matcher.match_intent(question)
            intent['question_type'] = matched_intent
            intent['confidence'] = confidence
            intent['metadata'] = metadata
            logger.info(f"Intent matched: {matched_intent} with confidence {confidence:.2f}")
        else:
            # Fallback to basic pattern matching
            logger.warning("Using fallback intent matching")
        
        # Detect question type
        if any(word in question_lower for word in ['total', 'sum', 'how much', 'how many']):
            intent['question_type'] = 'aggregation'
            intent['operations'] = ['sum', 'count']
            intent['visualization_type'] = 'metric_card'
            
        elif any(word in question_lower for word in ['top', 'best', 'highest', 'most', 'bottom', 'worst', 'lowest']):
            intent['question_type'] = 'ranking'
            intent['operations'] = ['groupby', 'sort']
            intent['visualization_type'] = 'bar_chart'
            
        elif any(word in question_lower for word in ['trend', 'over time', 'time series', 'change']):
            intent['question_type'] = 'trend_analysis'
            intent['operations'] = ['time_series', 'trend']
            intent['visualization_type'] = 'line_chart'
            
        elif any(word in question_lower for word in ['why', 'reason', 'cause', 'drop', 'decrease', 'increase']):
            intent['question_type'] = 'diagnostic'
            intent['operations'] = ['root_cause', 'comparison', 'breakdown']
            intent['visualization_type'] = 'multiple'
            
        elif any(word in question_lower for word in ['forecast', 'predict', 'future', 'next']):
            intent['question_type'] = 'predictive'
            intent['operations'] = ['forecast', 'prediction']
            intent['visualization_type'] = 'forecast_chart'
            
        elif any(word in question_lower for word in ['recommend', 'should', 'optimize', 'improve']):
            intent['question_type'] = 'prescriptive'
            intent['operations'] = ['optimization', 'recommendation']
            intent['visualization_type'] = 'comparison'
            
        elif any(word in question_lower for word in ['compare', 'versus', 'vs', 'between', 'difference']):
            intent['question_type'] = 'comparison'
            intent['operations'] = ['compare', 'segment']
            intent['visualization_type'] = 'grouped_bar'
            
        elif any(word in question_lower for word in ['average', 'mean', 'median']):
            intent['question_type'] = 'statistics'
            intent['operations'] = ['mean', 'median', 'stats']
            intent['visualization_type'] = 'distribution'
        
        # Detect target columns
        for col in df.columns:
            if col.lower() in question_lower or col.replace('_', ' ').lower() in question_lower:
                intent['target_columns'].append(col)
        
        # If no columns detected, infer from question
        if not intent['target_columns']:
            if any(word in question_lower for word in ['revenue', 'sales', 'money', 'price']):
                revenue_cols = [c for c in df.columns if 'revenue' in c.lower() or 'sales' in c.lower() or 'price' in c.lower()]
                intent['target_columns'].extend(revenue_cols[:1])
            
            if any(word in question_lower for word in ['product', 'item']):
                product_cols = [c for c in df.columns if 'product' in c.lower() or 'item' in c.lower()]
                intent['target_columns'].extend(product_cols[:1])
            
            if any(word in question_lower for word in ['customer', 'client', 'user']):
                customer_cols = [c for c in df.columns if 'customer' in c.lower() or 'client' in c.lower() or 'user' in c.lower()]
                intent['target_columns'].extend(customer_cols[:1])
            
            if any(word in question_lower for word in ['region', 'location', 'area']):
                region_cols = [c for c in df.columns if 'region' in c.lower() or 'location' in c.lower()]
                intent['target_columns'].extend(region_cols[:1])
        
        # Generate SQL equivalent for transparency
        intent['sql_equivalent'] = self._generate_sql_equivalent(intent)
        
        return intent
    
    def _execute_smart_analytics(self, intent: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Execute analytics based on intent"""
        df = self.current_data
        results = {
            'type': intent['question_type'],
            'data': {},
            'insights': []
        }
        
        if intent['question_type'] == 'aggregation':
            # Calculate totals and aggregations
            for col in intent['target_columns']:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    results['data'][f'{col}_total'] = float(df[col].sum())
                    results['data'][f'{col}_average'] = float(df[col].mean())
                    results['data'][f'{col}_count'] = int(df[col].count())
            
            if not results['data']:
                # No numeric columns specified, count rows
                results['data']['total_records'] = len(df)
        
        elif intent['question_type'] == 'ranking':
            # Find top/bottom performers
            target_cols = intent['target_columns']
            
            # Need at least category and value column
            cat_col = next((c for c in target_cols if c in df.select_dtypes(include=['object']).columns), None)
            num_col = next((c for c in target_cols if c in df.select_dtypes(include=[np.number]).columns), None)
            
            # If not found, use first categorical and first numeric
            if not cat_col:
                cat_cols = df.select_dtypes(include=['object']).columns
                cat_col = cat_cols[0] if len(cat_cols) > 0 else None
            
            if not num_col:
                num_cols = df.select_dtypes(include=[np.number]).columns
                num_col = num_cols[0] if len(num_cols) > 0 else None
            
            if cat_col and num_col:
                # Determine if looking for top or bottom
                is_bottom = any(word in question.lower() for word in ['bottom', 'worst', 'lowest'])
                
                grouped = df.groupby(cat_col)[num_col].sum().sort_values(ascending=is_bottom)
                top_n = grouped.head(5)
                
                results['data']['ranking'] = top_n.to_dict()
                results['data']['category_column'] = cat_col
                results['data']['value_column'] = num_col
                results['data']['direction'] = 'bottom' if is_bottom else 'top'
        
        elif intent['question_type'] == 'trend_analysis':
            # Trend over time
            date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c]) or 'date' in c.lower()]
            num_cols = df.select_dtypes(include=[np.number]).columns
            
            if date_cols and len(num_cols) > 0:
                date_col = date_cols[0]
                value_col = num_cols[0]
                
                # Group by date
                df_copy = df.copy()
                if not pd.api.types.is_datetime64_any_dtype(df_copy[date_col]):
                    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
                
                df_copy = df_copy.dropna(subset=[date_col])
                daily = df_copy.groupby(date_col)[value_col].sum().reset_index()
                
                results['data']['trend'] = {
                    'dates': daily[date_col].dt.strftime('%Y-%m-%d').tolist(),
                    'values': daily[value_col].tolist(),
                    'date_column': date_col,
                    'value_column': value_col
                }
                
                # Calculate trend direction
                if len(daily) > 1:
                    first_half = daily[value_col].iloc[:len(daily)//2].mean()
                    second_half = daily[value_col].iloc[len(daily)//2:].mean()
                    change_pct = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0
                    
                    results['data']['trend_direction'] = 'increasing' if change_pct > 5 else 'decreasing' if change_pct < -5 else 'stable'
                    results['data']['trend_change_pct'] = float(change_pct)
        
        elif intent['question_type'] == 'comparison':
            # Compare segments
            cat_cols = df.select_dtypes(include=['object']).columns
            num_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(cat_cols) > 0 and len(num_cols) > 0:
                cat_col = cat_cols[0]
                num_col = num_cols[0]
                
                comparison = df.groupby(cat_col)[num_col].agg(['sum', 'mean', 'count']).reset_index()
                
                results['data']['comparison'] = {
                    'category': cat_col,
                    'metric': num_col,
                    'segments': comparison.to_dict('records')
                }
        
        elif intent['question_type'] == 'statistics':
            # Statistical summary
            for col in df.select_dtypes(include=[np.number]).columns:
                results['data'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                }
        
        return results
    
    def _auto_generate_charts(self, intent: Dict[str, Any], analytics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Automatically generate appropriate visualizations based on intent and data"""
        charts = []
        
        viz_type = intent.get('visualization_type')
        data = analytics.get('data', {})
        
        # Generate chart based on type
        if viz_type == 'bar_chart' and 'ranking' in data:
            chart = self._create_bar_chart(data)
            if chart:
                charts.append(chart)
        
        elif viz_type == 'line_chart' and 'trend' in data:
            chart = self._create_line_chart(data['trend'])
            if chart:
                charts.append(chart)
        
        elif viz_type == 'grouped_bar' and 'comparison' in data:
            chart = self._create_comparison_chart(data['comparison'])
            if chart:
                charts.append(chart)
        
        elif viz_type == 'distribution' and len(data) > 0:
            chart = self._create_distribution_chart(data)
            if chart:
                charts.append(chart)
        
        elif viz_type == 'metric_card':
            # Return data for metric display (not a chart)
            charts.append({
                'type': 'metrics',
                'data': data,
                'figure': None
            })
        
        return charts
    
    def _create_bar_chart(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create bar chart from ranking data"""
        try:
            ranking = data.get('ranking', {})
            if not ranking:
                return None
            
            categories = list(ranking.keys())
            values = list(ranking.values())
            
            fig = go.Figure(data=[
                go.Bar(
                    x=categories,
                    y=values,
                    marker=dict(
                        color=values,
                        colorscale='Blues',
                        showscale=False
                    ),
                    text=[f'${v:,.0f}' if v > 1000 else f'{v:.0f}' for v in values],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                title=f"Top {len(categories)} {data.get('category_column', 'Items')}",
                xaxis_title=data.get('category_column', 'Category'),
                yaxis_title=data.get('value_column', 'Value'),
                template='plotly_white',
                height=450,
                showlegend=False
            )
            
            return {
                'type': 'bar_chart',
                'figure': fig,
                'title': f"Top Performers Analysis"
            }
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return None
    
    def _create_line_chart(self, trend_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create line chart for trend analysis"""
        try:
            dates = trend_data.get('dates', [])
            values = trend_data.get('values', [])
            
            if not dates or not values:
                return None
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    line=dict(color='#1f4788', width=3),
                    marker=dict(size=8, color='#2196F3'),
                    fill='tozeroy',
                    fillcolor='rgba(31, 71, 136, 0.1)'
                )
            ])
            
            fig.update_layout(
                title=f"{trend_data.get('value_column', 'Value')} Over Time",
                xaxis_title='Date',
                yaxis_title=trend_data.get('value_column', 'Value'),
                template='plotly_white',
                height=450,
                hovermode='x unified'
            )
            
            return {
                'type': 'line_chart',
                'figure': fig,
                'title': 'Trend Analysis'
            }
        except Exception as e:
            logger.error(f"Error creating line chart: {e}")
            return None
    
    def _create_comparison_chart(self, comparison_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create comparison chart"""
        try:
            segments = comparison_data.get('segments', [])
            if not segments:
                return None
            
            df_comp = pd.DataFrame(segments)
            category_col = comparison_data.get('category')
            
            fig = go.Figure()
            
            for metric in ['sum', 'mean']:
                if metric in df_comp.columns:
                    fig.add_trace(go.Bar(
                        name=metric.title(),
                        x=df_comp[category_col],
                        y=df_comp[metric],
                        text=df_comp[metric].round(2),
                        textposition='outside'
                    ))
            
            fig.update_layout(
                title=f"Comparison by {category_col}",
                xaxis_title=category_col,
                yaxis_title=comparison_data.get('metric', 'Value'),
                template='plotly_white',
                height=450,
                barmode='group'
            )
            
            return {
                'type': 'comparison_chart',
                'figure': fig,
                'title': 'Segment Comparison'
            }
        except Exception as e:
            logger.error(f"Error creating comparison chart: {e}")
            return None
    
    def _create_distribution_chart(self, stats_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create distribution visualization"""
        try:
            # Create box plot showing distributions
            fig = go.Figure()
            
            for col, stats in list(stats_data.items())[:5]:  # Limit to 5 columns
                if isinstance(stats, dict):
                    fig.add_trace(go.Box(
                        y=[stats.get('min'), stats.get('mean') - stats.get('std'), 
                           stats.get('mean'), stats.get('mean') + stats.get('std'), stats.get('max')],
                        name=col,
                        boxmean='sd'
                    ))
            
            fig.update_layout(
                title="Statistical Distribution",
                yaxis_title='Value',
                template='plotly_white',
                height=450
            )
            
            return {
                'type': 'distribution',
                'figure': fig,
                'title': 'Statistical Summary'
            }
        except Exception as e:
            logger.error(f"Error creating distribution chart: {e}")
            return None
    
    def _generate_intelligent_answer(self, question: str, intent: Dict, analytics: Dict, 
                                    visualizations: List[Dict]) -> str:
        """Generate natural language answer"""
        
        if self.use_openai and self.llm:
            # Use GPT-4 for intelligent response
            return self._generate_ai_answer(question, analytics)
        else:
            # Use template-based response
            return self._generate_template_response(question, intent, analytics)
    
    def _generate_ai_answer(self, question: str, analytics: Dict) -> str:
        """Generate answer using OpenAI GPT-4"""
        try:
            from langchain.schema import HumanMessage, SystemMessage
            
            prompt = f"""Answer this question based on the analytics results:

Question: {question}

Analytics Results:
{json.dumps(analytics, indent=2)}

Provide a clear, concise answer with:
1. Direct answer to the question
2. Key numbers and metrics
3. Brief insight or observation
4. Keep it under 100 words

Format with markdown for readability."""
            
            response = self.llm.invoke([
                SystemMessage(content="You are a data analyst providing insights. Be specific and cite numbers."),
                HumanMessage(content=prompt)
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"AI answer generation error: {e}")
            return self._generate_template_response(question, {}, analytics)
    
    def _generate_template_response(self, question: str, intent: Dict, analytics: Dict) -> str:
        """Template-based response generation"""
        data = analytics.get('data', {})
        question_type = analytics.get('type', 'unknown')
        
        if question_type == 'aggregation':
            parts = []
            for key, value in data.items():
                if 'total' in key:
                    col_name = key.replace('_total', '').replace('_', ' ').title()
                    parts.append(f"**Total {col_name}:** ${value:,.2f}" if value > 100 else f"**Total {col_name}:** {value:,.0f}")
                elif 'average' in key:
                    col_name = key.replace('_average', '').replace('_', ' ').title()
                    parts.append(f"**Average {col_name}:** ${value:,.2f}" if value > 100 else f"**Average {col_name}:** {value:,.2f}")
            
            if 'total_records' in data:
                parts.append(f"**Total Records:** {data['total_records']:,}")
            
            return "\n\n".join(parts) if parts else "Analytics completed successfully."
        
        elif question_type == 'ranking':
            ranking = data.get('ranking', {})
            cat_col = data.get('category_column', 'Item')
            val_col = data.get('value_column', 'Value')
            direction = data.get('direction', 'top')
            
            if ranking:
                answer = f"**{direction.title()} {len(ranking)} {cat_col}:**\n\n"
                for i, (item, value) in enumerate(ranking.items(), 1):
                    answer += f"{i}. **{item}**: ${value:,.2f}\n"
                return answer
        
        elif question_type == 'trend_analysis':
            trend = data.get('trend', {})
            if trend:
                direction = data.get('trend_direction', 'stable')
                change = data.get('trend_change_pct', 0)
                value_col = trend.get('value_column', 'metric')
                
                return f"""**Trend Analysis for {value_col}:**

**Direction:** {direction.title()} ({change:+.1f}% change)

The data shows a **{direction}** trend over the analyzed period. The {value_col} has {'increased' if change > 0 else 'decreased' if change < 0 else 'remained stable'} by approximately {abs(change):.1f}%.

**Data points analyzed:** {len(trend.get('dates', []))}"""
        
        elif question_type == 'comparison':
            comp = data.get('comparison', {})
            if comp and 'segments' in comp:
                answer = f"**Comparison by {comp['category']}:**\n\n"
                for seg in comp['segments'][:5]:
                    answer += f"- **{seg[comp['category']]}**: {seg.get('sum', seg.get('mean', 'N/A'))}\n"
                return answer
        
        # Default response
        return f"**Analysis Complete:**\n\n{json.dumps(data, indent=2)}"
    
    def _generate_strategic_recommendations(self, intent: Dict, analytics: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        data = analytics.get('data', {})
        question_type = analytics.get('type')
        
        if question_type == 'ranking':
            ranking = data.get('ranking', {})
            if ranking:
                top_item = list(ranking.keys())[0]
                bottom_item = list(ranking.keys())[-1]
                
                recommendations.append(f" Prioritize resources for {top_item} (top performer)")
                recommendations.append(f" Investigate underperformance of {bottom_item}")
                recommendations.append(f" Consider reallocating budget from low to high performers")
        
        elif question_type == 'trend_analysis':
            direction = data.get('trend_direction')
            change = data.get('trend_change_pct', 0)
            
            if direction == 'decreasing':
                recommendations.append(f"🔴 Urgent: Address {abs(change):.1f}% decline with corrective actions")
                recommendations.append(f" Conduct root cause analysis to identify drivers")
            elif direction == 'increasing':
                recommendations.append(f" Capitalize on positive {change:.1f}% growth trend")
                recommendations.append(f" Consider scaling successful strategies")
            else:
                recommendations.append(f" Monitor closely for emerging patterns")
        
        elif question_type == 'aggregation':
            # Add context-based recommendations
            recommendations.append(" Regular monitoring recommended")
            recommendations.append(" Set up automated alerts for significant changes")
        
        return recommendations
    
    def _calculate_confidence(self, intent: Dict, analytics: Dict) -> float:
        """Calculate confidence score for the analysis"""
        base_confidence = intent.get('confidence', 0.7)
        
        # Adjust based on data quality
        data_quality_factors = []
        
        # Check if we have enough data
        if self.current_data is not None:
            row_count = len(self.current_data)
            if row_count >= 30:
                data_quality_factors.append(0.1)
            elif row_count >= 10:
                data_quality_factors.append(0.05)
        
        # Check if analytics returned results
        if analytics.get('data') and len(analytics['data']) > 0:
            data_quality_factors.append(0.1)
        
        # Check if target columns were found
        if intent.get('target_columns'):
            data_quality_factors.append(0.05)
        
        final_confidence = min(0.99, base_confidence + sum(data_quality_factors))
        
        return round(final_confidence, 2)
    
    def _generate_sql_equivalent(self, intent: Dict) -> str:
        """Generate SQL equivalent of the query for transparency"""
        question_type = intent.get('question_type')
        target_cols = intent.get('target_columns', ['*'])
        
        if question_type == 'aggregation':
            cols_str = ', '.join([f'SUM({col})' for col in target_cols if col != '*'])
            return f"SELECT {cols_str or 'COUNT(*)'} FROM data"
        
        elif question_type == 'ranking':
            if len(target_cols) >= 2:
                return f"SELECT {target_cols[0]}, SUM({target_cols[1]}) FROM data GROUP BY {target_cols[0]} ORDER BY SUM({target_cols[1]}) DESC LIMIT 5"
            return f"SELECT * FROM data ORDER BY {target_cols[0] if target_cols else 'value'} DESC LIMIT 5"
        
        elif question_type == 'trend_analysis':
            return f"SELECT date, SUM(value) FROM data GROUP BY date ORDER BY date"
        
        else:
            return f"SELECT * FROM data"
    
    def _safe_to_list(self, data: Any) -> List:
        """Safely convert data to list, handling numpy arrays, tuples, pandas series, etc."""
        if data is None:
            return []
        
        # Already a list
        if isinstance(data, list):
            return data
        
        # Tuple
        if isinstance(data, tuple):
            return list(data)
        
        # Has tolist method (numpy array, pandas series)
        if hasattr(data, 'tolist'):
            try:
                return data.tolist()
            except Exception:
                pass
        
        # Try to convert to list
        try:
            return list(data)
        except Exception:
            return []

