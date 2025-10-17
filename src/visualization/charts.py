"""
Visualization Module - Interactive Plotly dashboards and charts
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generate interactive Plotly visualizations"""
    
    def __init__(self):
        """Initialize chart generator"""
        self.theme = {
            'template': 'plotly_white',
            'color_palette': px.colors.qualitative.Set2
        }
    
    def create_time_series_chart(self, df: pd.DataFrame, date_column: str, 
                                value_columns: List[str], title: str = "Time Series") -> Dict[str, Any]:
        """
        Create interactive time series chart
        
        Args:
            df: Input DataFrame
            date_column: Date column
            value_columns: Columns to plot
            title: Chart title
            
        Returns:
            Dictionary containing Plotly figure JSON
        """
        try:
            logger.info(f"Creating time series chart for {len(value_columns)} series")
            
            fig = go.Figure()
            
            for i, col in enumerate(value_columns):
                if col in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df[date_column],
                        y=df[col],
                        mode='lines+markers',
                        name=col,
                        line=dict(width=2),
                        marker=dict(size=6)
                    ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Date',
                yaxis_title='Value',
                template=self.theme['template'],
                hovermode='x unified',
                showlegend=True,
                height=500
            )
            
            return {
                'type': 'time_series',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating time series chart: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_bar_chart(self, df: pd.DataFrame, x_column: str, y_column: str,
                        title: str = "Bar Chart", orientation: str = 'v') -> Dict[str, Any]:
        """Create interactive bar chart"""
        try:
            logger.info(f"Creating bar chart: {x_column} vs {y_column}")
            
            # Aggregate if needed
            if df[x_column].duplicated().any():
                plot_df = df.groupby(x_column)[y_column].sum().reset_index()
            else:
                plot_df = df[[x_column, y_column]].copy()
            
            # Sort by value
            plot_df = plot_df.sort_values(y_column, ascending=False).head(20)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=plot_df[x_column] if orientation == 'v' else plot_df[y_column],
                    y=plot_df[y_column] if orientation == 'v' else plot_df[x_column],
                    orientation=orientation,
                    marker=dict(
                        color=plot_df[y_column],
                        colorscale='Blues',
                        showscale=True
                    )
                )
            ])
            
            fig.update_layout(
                title=title,
                xaxis_title=x_column if orientation == 'v' else y_column,
                yaxis_title=y_column if orientation == 'v' else x_column,
                template=self.theme['template'],
                height=500
            )
            
            return {
                'type': 'bar_chart',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_distribution_chart(self, df: pd.DataFrame, column: str,
                                  title: str = "Distribution") -> Dict[str, Any]:
        """Create distribution histogram with KDE"""
        try:
            logger.info(f"Creating distribution chart for {column}")
            
            fig = go.Figure()
            
            # Histogram
            fig.add_trace(go.Histogram(
                x=df[column],
                name='Distribution',
                nbinsx=30,
                marker=dict(color='lightblue', line=dict(color='darkblue', width=1))
            ))
            
            fig.update_layout(
                title=title,
                xaxis_title=column,
                yaxis_title='Frequency',
                template=self.theme['template'],
                showlegend=True,
                height=500
            )
            
            return {
                'type': 'distribution',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating distribution chart: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame,
                                   title: str = "Correlation Matrix") -> Dict[str, Any]:
        """Create correlation heatmap"""
        try:
            logger.info("Creating correlation heatmap")
            
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=correlation_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title=title,
                template=self.theme['template'],
                height=600,
                width=700
            )
            
            return {
                'type': 'heatmap',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_forecast_chart(self, historical_df: pd.DataFrame, forecast_df: pd.DataFrame,
                             date_column: str, value_column: str,
                             title: str = "Forecast") -> Dict[str, Any]:
        """Create forecast visualization with confidence intervals"""
        try:
            logger.info("Creating forecast chart")
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_df[date_column],
                y=historical_df[value_column],
                mode='lines',
                name='Historical',
                line=dict(color='blue', width=2)
            ))
            
            # Forecast
            if 'ds' in forecast_df.columns and 'yhat' in forecast_df.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat'],
                    mode='lines',
                    name='Forecast',
                    line=dict(color='red', width=2, dash='dash')
                ))
                
                # Confidence interval
                if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
                    fig.add_trace(go.Scatter(
                        x=forecast_df['ds'],
                        y=forecast_df['yhat_upper'],
                        mode='lines',
                        name='Upper Bound',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    fig.add_trace(go.Scatter(
                        x=forecast_df['ds'],
                        y=forecast_df['yhat_lower'],
                        mode='lines',
                        name='Lower Bound',
                        fill='tonexty',
                        fillcolor='rgba(255, 0, 0, 0.2)',
                        line=dict(width=0),
                        showlegend=True
                    ))
            
            fig.update_layout(
                title=title,
                xaxis_title='Date',
                yaxis_title='Value',
                template=self.theme['template'],
                hovermode='x unified',
                height=500
            )
            
            return {
                'type': 'forecast',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating forecast chart: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_dashboard(self, charts: List[Dict[str, Any]], 
                        title: str = "Analytics Dashboard") -> Dict[str, Any]:
        """Create multi-chart dashboard"""
        try:
            logger.info(f"Creating dashboard with {len(charts)} charts")
            
            # Create subplots
            rows = (len(charts) + 1) // 2
            fig = make_subplots(
                rows=rows,
                cols=2,
                subplot_titles=[chart.get('title', f'Chart {i+1}') for i, chart in enumerate(charts)]
            )
            
            for i, chart_data in enumerate(charts):
                row = i // 2 + 1
                col = i % 2 + 1
                
                if 'figure' in chart_data:
                    # Parse existing figure and add traces
                    import json
                    fig_json = json.loads(chart_data['figure'])
                    for trace in fig_json.get('data', []):
                        fig.add_trace(go.Scatter(trace), row=row, col=col)
            
            fig.update_layout(
                title_text=title,
                template=self.theme['template'],
                height=400 * rows,
                showlegend=False
            )
            
            return {
                'type': 'dashboard',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_pie_chart(self, df: pd.DataFrame, values_column: str, 
                        names_column: str, title: str = "Distribution") -> Dict[str, Any]:
        """Create pie chart"""
        try:
            logger.info(f"Creating pie chart for {names_column}")
            
            # Aggregate if needed
            plot_df = df.groupby(names_column)[values_column].sum().reset_index()
            plot_df = plot_df.sort_values(values_column, ascending=False).head(10)
            
            fig = go.Figure(data=[go.Pie(
                labels=plot_df[names_column],
                values=plot_df[values_column],
                hole=0.3,
                marker=dict(colors=self.theme['color_palette'])
            )])
            
            fig.update_layout(
                title=title,
                template=self.theme['template'],
                height=500
            )
            
            return {
                'type': 'pie_chart',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating pie chart: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def create_box_plot(self, df: pd.DataFrame, y_column: str, 
                       x_column: Optional[str] = None, title: str = "Box Plot") -> Dict[str, Any]:
        """Create box plot for outlier visualization"""
        try:
            logger.info(f"Creating box plot for {y_column}")
            
            if x_column and x_column in df.columns:
                fig = go.Figure()
                for category in df[x_column].unique():
                    fig.add_trace(go.Box(
                        y=df[df[x_column] == category][y_column],
                        name=str(category)
                    ))
            else:
                fig = go.Figure(data=[go.Box(y=df[y_column], name=y_column)])
            
            fig.update_layout(
                title=title,
                yaxis_title=y_column,
                template=self.theme['template'],
                height=500
            )
            
            return {
                'type': 'box_plot',
                'figure': fig.to_json(),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating box plot: {str(e)}")
            return {'status': 'error', 'message': str(e)}

