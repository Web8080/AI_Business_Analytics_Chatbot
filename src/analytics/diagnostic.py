"""
Diagnostic Analytics Module - Root cause analysis, segment analysis, variance analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class DiagnosticAnalytics:
    """Diagnostic analytics for root cause identification and deep-dive analysis"""
    
    def __init__(self):
        """Initialize diagnostic analytics engine"""
        pass
    
    def root_cause_analysis(self, df: pd.DataFrame, target_column: str, 
                           dimension_columns: List[str], threshold: float = 0.1) -> Dict[str, Any]:
        """
        Identify root causes of changes in target metric
        
        Args:
            df: Input DataFrame
            target_column: Metric to analyze
            dimension_columns: Dimensions to break down by
            threshold: Minimum impact threshold (10% by default)
            
        Returns:
            Dictionary containing root cause analysis
        """
        if target_column not in df.columns:
            return {'status': 'error', 'message': f'Target column {target_column} not found'}
        
        logger.info(f"Performing root cause analysis on {target_column}")
        
        root_causes = []
        overall_mean = df[target_column].mean()
        
        for dim in dimension_columns:
            if dim not in df.columns:
                continue
            
            # Calculate segment performance
            segment_stats = df.groupby(dim)[target_column].agg(['count', 'mean', 'sum']).reset_index()
            segment_stats['variance_from_mean'] = segment_stats['mean'] - overall_mean
            segment_stats['impact_percentage'] = (segment_stats['variance_from_mean'] / overall_mean * 100).abs()
            
            # Filter significant segments
            significant_segments = segment_stats[segment_stats['impact_percentage'] > threshold * 100]
            
            for _, row in significant_segments.iterrows():
                root_causes.append({
                    'dimension': dim,
                    'segment': str(row[dim]),
                    'segment_mean': float(row['mean']),
                    'overall_mean': float(overall_mean),
                    'variance': float(row['variance_from_mean']),
                    'impact_percentage': float(row['impact_percentage']),
                    'sample_size': int(row['count']),
                    'direction': 'above' if row['variance_from_mean'] > 0 else 'below'
                })
        
        # Sort by impact
        root_causes.sort(key=lambda x: x['impact_percentage'], reverse=True)
        
        return {
            'target_metric': target_column,
            'overall_mean': float(overall_mean),
            'root_causes': root_causes[:20],  # Top 20
            'total_causes_found': len(root_causes),
            'status': 'success'
        }
    
    def segment_analysis(self, df: pd.DataFrame, segment_column: str, 
                        metrics: List[str]) -> Dict[str, Any]:
        """
        Detailed segment-by-segment analysis
        
        Args:
            df: Input DataFrame
            segment_column: Column to segment by
            metrics: Metrics to analyze for each segment
            
        Returns:
            Dictionary containing segment analysis
        """
        if segment_column not in df.columns:
            return {'status': 'error', 'message': f'Segment column {segment_column} not found'}
        
        logger.info(f"Performing segment analysis on {segment_column}")
        
        segments = {}
        
        for segment_value in df[segment_column].unique():
            segment_df = df[df[segment_column] == segment_value]
            
            segment_metrics = {
                'count': len(segment_df),
                'percentage_of_total': round(len(segment_df) / len(df) * 100, 2)
            }
            
            for metric in metrics:
                if metric in segment_df.columns and pd.api.types.is_numeric_dtype(segment_df[metric]):
                    segment_metrics[metric] = {
                        'sum': float(segment_df[metric].sum()),
                        'mean': float(segment_df[metric].mean()),
                        'median': float(segment_df[metric].median()),
                        'std': float(segment_df[metric].std())
                    }
            
            segments[str(segment_value)] = segment_metrics
        
        # Calculate segment comparisons
        comparisons = self._compare_segments(df, segment_column, metrics)
        
        return {
            'segment_column': segment_column,
            'total_segments': len(segments),
            'segments': segments,
            'comparisons': comparisons,
            'status': 'success'
        }
    
    def _compare_segments(self, df: pd.DataFrame, segment_column: str, 
                         metrics: List[str]) -> Dict[str, Any]:
        """Compare segments using statistical tests"""
        comparisons = {}
        
        for metric in metrics:
            if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
                continue
            
            segments = [group[metric].dropna().values for name, group in df.groupby(segment_column)]
            
            if len(segments) >= 2:
                # Perform ANOVA if more than 2 groups
                if len(segments) > 2:
                    f_stat, p_value = stats.f_oneway(*segments)
                    comparisons[metric] = {
                        'test': 'ANOVA',
                        'f_statistic': float(f_stat),
                        'p_value': float(p_value),
                        'significant': bool(p_value < 0.05)
                    }
                else:
                    # T-test for 2 groups
                    t_stat, p_value = stats.ttest_ind(segments[0], segments[1])
                    comparisons[metric] = {
                        'test': 't-test',
                        't_statistic': float(t_stat),
                        'p_value': float(p_value),
                        'significant': bool(p_value < 0.05)
                    }
        
        return comparisons
    
    def variance_analysis(self, df: pd.DataFrame, actual_column: str, 
                         expected_column: Optional[str] = None,
                         breakdown_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Variance analysis comparing actual vs expected values
        
        Args:
            df: Input DataFrame
            actual_column: Column with actual values
            expected_column: Column with expected/budget values
            breakdown_columns: Columns to break down variance by
            
        Returns:
            Dictionary containing variance analysis
        """
        if actual_column not in df.columns:
            return {'status': 'error', 'message': f'Actual column {actual_column} not found'}
        
        logger.info("Performing variance analysis")
        
        # If no expected column, use overall mean as expected
        if expected_column is None or expected_column not in df.columns:
            expected_value = df[actual_column].mean()
            df['_expected'] = expected_value
            expected_column = '_expected'
        
        # Calculate overall variance
        df['_variance'] = df[actual_column] - df[expected_column]
        df['_variance_pct'] = (df['_variance'] / df[expected_column] * 100).replace([np.inf, -np.inf], np.nan)
        
        overall_variance = {
            'total_actual': float(df[actual_column].sum()),
            'total_expected': float(df[expected_column].sum()),
            'total_variance': float(df['_variance'].sum()),
            'variance_percentage': float(df['_variance'].sum() / df[expected_column].sum() * 100) if df[expected_column].sum() != 0 else 0,
            'favorable': bool(df['_variance'].sum() > 0)
        }
        
        # Breakdown by dimensions
        breakdowns = {}
        if breakdown_columns:
            for col in breakdown_columns:
                if col not in df.columns:
                    continue
                
                breakdown = df.groupby(col).agg({
                    actual_column: 'sum',
                    expected_column: 'sum',
                    '_variance': 'sum'
                }).reset_index()
                
                breakdown['variance_pct'] = (breakdown['_variance'] / breakdown[expected_column] * 100).replace([np.inf, -np.inf], np.nan)
                
                breakdowns[col] = breakdown.to_dict('records')
        
        # Clean up temporary columns
        df.drop(['_variance', '_variance_pct'], axis=1, inplace=True, errors='ignore')
        if '_expected' in df.columns:
            df.drop('_expected', axis=1, inplace=True)
        
        return {
            'overall_variance': overall_variance,
            'breakdowns': breakdowns,
            'status': 'success'
        }
    
    def cohort_analysis(self, df: pd.DataFrame, user_column: str, 
                       date_column: str, value_column: str) -> Dict[str, Any]:
        """
        Cohort analysis for retention and behavior patterns
        
        Args:
            df: Input DataFrame
            user_column: Column identifying users/customers
            date_column: Date column
            value_column: Metric to track (revenue, activity, etc.)
            
        Returns:
            Dictionary containing cohort analysis
        """
        if not all(col in df.columns for col in [user_column, date_column, value_column]):
            return {'status': 'error', 'message': 'Required columns not found'}
        
        logger.info("Performing cohort analysis")
        
        df[date_column] = pd.to_datetime(df[date_column])
        
        # Determine cohort (first activity month)
        df['cohort'] = df.groupby(user_column)[date_column].transform('min').dt.to_period('M')
        df['activity_period'] = df[date_column].dt.to_period('M')
        
        # Calculate cohort period (months since first activity)
        df['cohort_period'] = (df['activity_period'] - df['cohort']).apply(lambda x: x.n)
        
        # Cohort size
        cohort_sizes = df.groupby('cohort')[user_column].nunique()
        
        # Retention matrix
        retention = df.groupby(['cohort', 'cohort_period'])[user_column].nunique().reset_index()
        retention_pivot = retention.pivot(index='cohort', columns='cohort_period', values=user_column)
        
        # Calculate retention rates
        retention_rate = retention_pivot.div(cohort_sizes, axis=0) * 100
        
        # Value by cohort
        cohort_value = df.groupby(['cohort', 'cohort_period'])[value_column].sum().reset_index()
        value_pivot = cohort_value.pivot(index='cohort', columns='cohort_period', values=value_column)
        
        return {
            'cohort_sizes': cohort_sizes.to_dict(),
            'retention_rates': retention_rate.to_dict(),
            'cohort_values': value_pivot.to_dict(),
            'status': 'success'
        }
    
    def anomaly_detection(self, df: pd.DataFrame, columns: List[str], 
                         method: str = 'zscore', threshold: float = 3.0) -> Dict[str, Any]:
        """
        Detect anomalies in data
        
        Args:
            df: Input DataFrame
            columns: Columns to check for anomalies
            method: Detection method ('zscore', 'iqr')
            threshold: Threshold for anomaly detection
            
        Returns:
            Dictionary containing detected anomalies
        """
        logger.info(f"Detecting anomalies using {method} method")
        
        anomalies = {}
        
        for col in columns:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            if method == 'zscore':
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                anomaly_indices = np.where(z_scores > threshold)[0]
            elif method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                anomaly_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
            else:
                continue
            
            if len(anomaly_indices) > 0:
                anomalies[col] = {
                    'count': len(anomaly_indices),
                    'percentage': round(len(anomaly_indices) / len(df) * 100, 2),
                    'indices': anomaly_indices.tolist()[:100],  # Limit to first 100
                    'values': df[col].iloc[anomaly_indices].tolist()[:100]
                }
        
        return {
            'method': method,
            'threshold': threshold,
            'anomalies': anomalies,
            'total_anomalies': sum(a['count'] for a in anomalies.values()),
            'status': 'success'
        }

