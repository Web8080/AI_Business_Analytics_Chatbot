"""
Descriptive Analytics Module - KPI calculation, trend analysis, statistical summaries
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class DescriptiveAnalytics:
    """Descriptive analytics for data summarization and KPI calculation"""
    
    def __init__(self):
        """Initialize descriptive analytics engine"""
        pass
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing summary statistics
        """
        if df.empty:
            return {'status': 'empty', 'message': 'No data to analyze'}
        
        logger.info("Generating summary statistics")
        
        summary = {
            'overview': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
            },
            'numeric_columns': {},
            'categorical_columns': {},
            'date_columns': {}
        }
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary['numeric_columns'][col] = {
                'count': int(df[col].count()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q1': float(df[col].quantile(0.25)),
                'q3': float(df[col].quantile(0.75)),
                'skewness': float(df[col].skew()),
                'kurtosis': float(df[col].kurtosis())
            }
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            summary['categorical_columns'][col] = {
                'unique_values': int(df[col].nunique()),
                'most_common': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                'top_5_values': value_counts.head(5).to_dict()
            }
        
        # Date columns
        date_cols = df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            summary['date_columns'][col] = {
                'min_date': str(df[col].min()),
                'max_date': str(df[col].max()),
                'date_range_days': (df[col].max() - df[col].min()).days
            }
        
        summary['status'] = 'success'
        return summary
    
    def calculate_kpis(self, df: pd.DataFrame, kpi_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate business KPIs based on configuration
        
        Args:
            df: Input DataFrame
            kpi_config: KPI calculation configuration
            
        Returns:
            Dictionary containing calculated KPIs
        """
        logger.info("Calculating KPIs")
        
        kpis = {}
        
        # Revenue metrics
        if 'revenue_column' in kpi_config and kpi_config['revenue_column'] in df.columns:
            revenue_col = kpi_config['revenue_column']
            kpis['revenue'] = {
                'total_revenue': float(df[revenue_col].sum()),
                'average_revenue': float(df[revenue_col].mean()),
                'median_revenue': float(df[revenue_col].median()),
                'revenue_growth_rate': self._calculate_growth_rate(df, revenue_col, kpi_config.get('date_column'))
            }
        
        # Customer metrics
        if 'customer_column' in kpi_config and kpi_config['customer_column'] in df.columns:
            customer_col = kpi_config['customer_column']
            kpis['customers'] = {
                'total_customers': int(df[customer_col].nunique()),
                'average_transactions_per_customer': float(len(df) / df[customer_col].nunique()) if df[customer_col].nunique() > 0 else 0
            }
        
        # Product metrics
        if 'product_column' in kpi_config and kpi_config['product_column'] in df.columns:
            product_col = kpi_config['product_column']
            product_performance = df.groupby(product_col).agg({
                kpi_config.get('revenue_column', df.columns[0]): ['sum', 'count']
            }).sort_values((kpi_config.get('revenue_column', df.columns[0]), 'sum'), ascending=False)
            
            kpis['products'] = {
                'total_products': int(df[product_col].nunique()),
                'top_product': str(product_performance.index[0]) if len(product_performance) > 0 else None
            }
        
        kpis['status'] = 'success'
        return kpis
    
    def _calculate_growth_rate(self, df: pd.DataFrame, value_column: str, date_column: Optional[str]) -> Optional[float]:
        """Calculate growth rate over time"""
        if date_column is None or date_column not in df.columns:
            return None
        
        try:
            df_sorted = df.sort_values(date_column)
            first_period = df_sorted[value_column].iloc[:len(df_sorted)//4].sum()
            last_period = df_sorted[value_column].iloc[-len(df_sorted)//4:].sum()
            
            if first_period > 0:
                growth_rate = ((last_period - first_period) / first_period) * 100
                return round(growth_rate, 2)
        except Exception:
            pass
        
        return None
    
    def analyze_trends(self, df: pd.DataFrame, date_column: str, value_columns: List[str]) -> Dict[str, Any]:
        """
        Analyze trends over time
        
        Args:
            df: Input DataFrame
            date_column: Column containing dates
            value_columns: Columns to analyze for trends
            
        Returns:
            Dictionary containing trend analysis
        """
        if date_column not in df.columns:
            return {'status': 'error', 'message': f'Date column {date_column} not found'}
        
        logger.info(f"Analyzing trends for {len(value_columns)} columns")
        
        trends = {}
        
        df_sorted = df.sort_values(date_column)
        
        for col in value_columns:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            # Aggregate by date
            daily_values = df_sorted.groupby(date_column)[col].sum().reset_index()
            
            if len(daily_values) < 2:
                continue
            
            # Calculate trend
            x = np.arange(len(daily_values))
            y = daily_values[col].values
            
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Determine trend direction
            if slope > 0 and p_value < 0.05:
                direction = 'increasing'
            elif slope < 0 and p_value < 0.05:
                direction = 'decreasing'
            else:
                direction = 'stable'
            
            trends[col] = {
                'direction': direction,
                'slope': float(slope),
                'r_squared': float(r_value ** 2),
                'p_value': float(p_value),
                'confidence': 'high' if p_value < 0.01 else 'medium' if p_value < 0.05 else 'low',
                'total_change': float(y[-1] - y[0]),
                'percent_change': float(((y[-1] - y[0]) / y[0] * 100)) if y[0] != 0 else 0
            }
        
        return {'trends': trends, 'status': 'success'}
    
    def calculate_distributions(self, df: pd.DataFrame, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Calculate distribution statistics for numeric columns
        
        Args:
            df: Input DataFrame
            columns: Specific columns to analyze (None = all numeric)
            
        Returns:
            Dictionary containing distribution analysis
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        logger.info(f"Calculating distributions for {len(columns)} columns")
        
        distributions = {}
        
        for col in columns:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            data = df[col].dropna()
            
            if len(data) == 0:
                continue
            
            # Test for normality
            _, normality_p_value = stats.normaltest(data) if len(data) >= 8 else (None, None)
            
            distributions[col] = {
                'mean': float(data.mean()),
                'median': float(data.median()),
                'mode': float(data.mode()[0]) if not data.mode().empty else None,
                'std': float(data.std()),
                'variance': float(data.var()),
                'skewness': float(data.skew()),
                'kurtosis': float(data.kurtosis()),
                'is_normal': bool(normality_p_value > 0.05) if normality_p_value else None,
                'percentiles': {
                    '5th': float(data.quantile(0.05)),
                    '25th': float(data.quantile(0.25)),
                    '50th': float(data.quantile(0.50)),
                    '75th': float(data.quantile(0.75)),
                    '95th': float(data.quantile(0.95))
                }
            }
        
        return {'distributions': distributions, 'status': 'success'}
    
    def correlation_analysis(self, df: pd.DataFrame, method: str = 'pearson') -> Dict[str, Any]:
        """
        Perform correlation analysis on numeric columns
        
        Args:
            df: Input DataFrame
            method: Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
            Dictionary containing correlation matrix and insights
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {'status': 'error', 'message': 'Insufficient numeric columns for correlation'}
        
        logger.info(f"Performing {method} correlation analysis")
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr(method=method)
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:  # Threshold for "strong" correlation
                    strong_correlations.append({
                        'variable_1': corr_matrix.columns[i],
                        'variable_2': corr_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'strong' if abs(corr_value) > 0.7 else 'moderate'
                    })
        
        # Sort by absolute correlation value
        strong_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'strong_correlations': strong_correlations,
            'method': method,
            'status': 'success'
        }

