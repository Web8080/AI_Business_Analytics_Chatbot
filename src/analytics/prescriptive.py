"""
Prescriptive Analytics Module - Optimization recommendations, action planning
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class PrescriptiveAnalytics:
    """Prescriptive analytics for optimization and actionable recommendations"""
    
    def __init__(self):
        """Initialize prescriptive analytics engine"""
        pass
    
    def generate_recommendations(self, analysis_results: Dict[str, Any], 
                                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate actionable recommendations based on analysis results
        
        Args:
            analysis_results: Results from descriptive/diagnostic/predictive analytics
            context: Additional business context
            
        Returns:
            Dictionary containing recommendations
        """
        logger.info("Generating prescriptive recommendations")
        
        recommendations = []
        
        # Analyze trends and generate recommendations
        if 'trends' in analysis_results:
            recommendations.extend(self._recommendations_from_trends(analysis_results['trends']))
        
        # Analyze root causes and generate recommendations
        if 'root_causes' in analysis_results:
            recommendations.extend(self._recommendations_from_root_causes(analysis_results['root_causes']))
        
        # Analyze forecast and generate recommendations
        if 'forecast' in analysis_results:
            recommendations.extend(self._recommendations_from_forecast(analysis_results['forecast']))
        
        # Analyze anomalies and generate recommendations
        if 'anomalies' in analysis_results:
            recommendations.extend(self._recommendations_from_anomalies(analysis_results['anomalies']))
        
        # Prioritize recommendations
        prioritized = self._prioritize_recommendations(recommendations)
        
        return {
            'recommendations': prioritized,
            'total_recommendations': len(prioritized),
            'status': 'success'
        }
    
    def _recommendations_from_trends(self, trends: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations from trend analysis"""
        recommendations = []
        
        for metric, trend_data in trends.items():
            if trend_data['direction'] == 'decreasing' and trend_data['confidence'] in ['high', 'medium']:
                recommendations.append({
                    'type': 'trend_alert',
                    'priority': 'high',
                    'metric': metric,
                    'issue': f'{metric} is decreasing by {abs(trend_data["percent_change"]):.1f}%',
                    'recommendation': f'Investigate reasons for decline in {metric} and implement corrective actions',
                    'expected_impact': 'high',
                    'confidence': trend_data['confidence']
                })
            
            elif trend_data['direction'] == 'increasing' and trend_data['confidence'] in ['high', 'medium']:
                recommendations.append({
                    'type': 'opportunity',
                    'priority': 'medium',
                    'metric': metric,
                    'issue': f'{metric} is increasing by {trend_data["percent_change"]:.1f}%',
                    'recommendation': f'Capitalize on positive trend in {metric} by increasing investment in related activities',
                    'expected_impact': 'medium',
                    'confidence': trend_data['confidence']
                })
        
        return recommendations
    
    def _recommendations_from_root_causes(self, root_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations from root cause analysis"""
        recommendations = []
        
        for cause in root_causes[:5]:  # Top 5 causes
            if cause['direction'] == 'below':
                recommendations.append({
                    'type': 'performance_issue',
                    'priority': 'high',
                    'segment': f"{cause['dimension']}: {cause['segment']}",
                    'issue': f'{cause["segment"]} is {abs(cause["impact_percentage"]):.1f}% below average',
                    'recommendation': f'Focus improvement efforts on {cause["segment"]} segment - analyze barriers and implement targeted interventions',
                    'expected_impact': 'high',
                    'confidence': 'high'
                })
            else:
                recommendations.append({
                    'type': 'best_practice',
                    'priority': 'medium',
                    'segment': f"{cause['dimension']}: {cause['segment']}",
                    'issue': f'{cause["segment"]} is {cause["impact_percentage"]:.1f}% above average',
                    'recommendation': f'Document and replicate best practices from {cause["segment"]} segment to other segments',
                    'expected_impact': 'high',
                    'confidence': 'high'
                })
        
        return recommendations
    
    def _recommendations_from_forecast(self, forecast: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate recommendations from forecast results"""
        recommendations = []
        
        if len(forecast) > 0:
            # Analyze forecast trend
            first_value = forecast[0]['yhat']
            last_value = forecast[-1]['yhat']
            change_pct = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
            
            if change_pct < -10:
                recommendations.append({
                    'type': 'forecast_alert',
                    'priority': 'high',
                    'issue': f'Forecast indicates {abs(change_pct):.1f}% decline in upcoming period',
                    'recommendation': 'Develop contingency plan and implement proactive measures to prevent forecasted decline',
                    'expected_impact': 'critical',
                    'confidence': 'medium'
                })
            elif change_pct > 20:
                recommendations.append({
                    'type': 'capacity_planning',
                    'priority': 'medium',
                    'issue': f'Forecast indicates {change_pct:.1f}% growth in upcoming period',
                    'recommendation': 'Ensure adequate capacity and resources to handle forecasted growth',
                    'expected_impact': 'high',
                    'confidence': 'medium'
                })
        
        return recommendations
    
    def _recommendations_from_anomalies(self, anomalies: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations from anomaly detection"""
        recommendations = []
        
        for metric, anomaly_data in anomalies.items():
            if anomaly_data['count'] > 0:
                recommendations.append({
                    'type': 'anomaly_investigation',
                    'priority': 'medium',
                    'metric': metric,
                    'issue': f'Detected {anomaly_data["count"]} anomalies ({anomaly_data["percentage"]:.1f}%) in {metric}',
                    'recommendation': f'Investigate anomalies in {metric} to identify data quality issues or special events',
                    'expected_impact': 'medium',
                    'confidence': 'high'
                })
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize recommendations based on impact and confidence"""
        priority_scores = {
            'high': 3,
            'medium': 2,
            'low': 1
        }
        
        for rec in recommendations:
            priority = priority_scores.get(rec.get('priority', 'low'), 1)
            impact = priority_scores.get(rec.get('expected_impact', 'low'), 1)
            confidence = priority_scores.get(rec.get('confidence', 'low'), 1)
            rec['score'] = priority * 2 + impact + confidence
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations
    
    def optimize_inventory(self, df: pd.DataFrame, product_column: str, 
                          sales_column: str, stock_column: Optional[str] = None,
                          lead_time_days: int = 7) -> Dict[str, Any]:
        """
        Optimize inventory levels based on sales patterns
        
        Args:
            df: Input DataFrame with sales data
            product_column: Column identifying products
            sales_column: Column with sales quantities
            stock_column: Current stock levels (optional)
            lead_time_days: Lead time for restocking in days
            
        Returns:
            Dictionary containing inventory optimization recommendations
        """
        logger.info("Optimizing inventory levels")
        
        try:
            # Calculate product statistics
            product_stats = df.groupby(product_column)[sales_column].agg([
                ('total_sales', 'sum'),
                ('avg_daily_sales', 'mean'),
                ('std_sales', 'std'),
                ('max_sales', 'max')
            ]).reset_index()
            
            # Calculate safety stock (to handle variability)
            product_stats['safety_stock'] = product_stats['std_sales'] * np.sqrt(lead_time_days) * 1.65  # 95% service level
            
            # Calculate reorder point
            product_stats['reorder_point'] = (product_stats['avg_daily_sales'] * lead_time_days) + product_stats['safety_stock']
            
            # Calculate optimal order quantity (simple EOQ approximation)
            product_stats['optimal_order_quantity'] = product_stats['avg_daily_sales'] * lead_time_days * 2
            
            # Add current stock if provided
            if stock_column and stock_column in df.columns:
                current_stock = df.groupby(product_column)[stock_column].last().reset_index()
                product_stats = product_stats.merge(current_stock, on=product_column, how='left')
                product_stats['stock_status'] = product_stats.apply(
                    lambda row: 'reorder' if row[stock_column] < row['reorder_point'] else 'adequate',
                    axis=1
                )
            
            # Generate recommendations
            recommendations = []
            for _, row in product_stats.iterrows():
                if stock_column and row.get('stock_status') == 'reorder':
                    recommendations.append({
                        'product': str(row[product_column]),
                        'action': 'reorder',
                        'current_stock': float(row[stock_column]) if stock_column else None,
                        'reorder_point': round(float(row['reorder_point']), 2),
                        'suggested_quantity': round(float(row['optimal_order_quantity']), 2),
                        'priority': 'high'
                    })
            
            result = {
                'product_statistics': product_stats.to_dict('records'),
                'reorder_recommendations': recommendations,
                'total_products': len(product_stats),
                'products_needing_reorder': len(recommendations),
                'status': 'success'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Inventory optimization error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def optimize_pricing(self, df: pd.DataFrame, price_column: str, 
                        quantity_column: str, segment_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze pricing and provide optimization recommendations
        
        Args:
            df: Input DataFrame with sales data
            price_column: Column with prices
            quantity_column: Column with quantities sold
            segment_columns: Columns for segment analysis
            
        Returns:
            Dictionary containing pricing optimization recommendations
        """
        logger.info("Analyzing pricing optimization")
        
        try:
            df['revenue'] = df[price_column] * df[quantity_column]
            
            # Calculate price elasticity (simplified)
            price_points = df.groupby(price_column).agg({
                quantity_column: 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            # Find optimal price point (max revenue)
            optimal_price_idx = price_points['revenue'].idxmax()
            optimal_price = price_points.loc[optimal_price_idx, price_column]
            max_revenue = price_points.loc[optimal_price_idx, 'revenue']
            
            # Current average price
            current_avg_price = df[price_column].mean()
            
            recommendations = []
            
            if abs(optimal_price - current_avg_price) / current_avg_price > 0.1:  # More than 10% difference
                recommendations.append({
                    'type': 'price_adjustment',
                    'current_avg_price': round(float(current_avg_price), 2),
                    'optimal_price': round(float(optimal_price), 2),
                    'expected_revenue_increase': round(float((max_revenue - df['revenue'].sum()) / df['revenue'].sum() * 100), 2),
                    'recommendation': f'Consider adjusting average price to ${optimal_price:.2f} to maximize revenue'
                })
            
            # Segment analysis
            if segment_columns:
                for segment_col in segment_columns:
                    if segment_col in df.columns:
                        segment_analysis = df.groupby(segment_col).agg({
                            price_column: 'mean',
                            quantity_column: 'sum',
                            'revenue': 'sum'
                        }).reset_index()
                        
                        recommendations.append({
                            'type': 'segment_pricing',
                            'segment': segment_col,
                            'analysis': segment_analysis.to_dict('records'),
                            'recommendation': f'Consider differentiated pricing strategy for {segment_col}'
                        })
            
            return {
                'optimal_price': round(float(optimal_price), 2),
                'current_avg_price': round(float(current_avg_price), 2),
                'price_points_analysis': price_points.to_dict('records'),
                'recommendations': recommendations,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Pricing optimization error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def resource_allocation(self, df: pd.DataFrame, resource_column: str, 
                           performance_metric: str, budget: float) -> Dict[str, Any]:
        """
        Optimize resource allocation based on performance
        
        Args:
            df: Input DataFrame
            resource_column: Column identifying resources (e.g., marketing channels)
            performance_metric: Metric to optimize (e.g., ROI, conversions)
            budget: Total budget to allocate
            
        Returns:
            Dictionary containing resource allocation recommendations
        """
        logger.info("Optimizing resource allocation")
        
        try:
            # Calculate performance by resource
            resource_performance = df.groupby(resource_column)[performance_metric].sum().reset_index()
            resource_performance['efficiency'] = resource_performance[performance_metric]
            
            # Calculate current allocation (assuming equal distribution)
            total_resources = len(resource_performance)
            resource_performance['current_allocation'] = budget / total_resources
            
            # Calculate optimal allocation (proportional to performance)
            total_performance = resource_performance['efficiency'].sum()
            resource_performance['optimal_allocation'] = (resource_performance['efficiency'] / total_performance) * budget
            
            # Calculate expected improvement
            resource_performance['allocation_change'] = resource_performance['optimal_allocation'] - resource_performance['current_allocation']
            resource_performance['allocation_change_pct'] = (resource_performance['allocation_change'] / resource_performance['current_allocation'] * 100)
            
            recommendations = []
            for _, row in resource_performance.iterrows():
                if abs(row['allocation_change_pct']) > 10:  # Significant change
                    action = 'increase' if row['allocation_change'] > 0 else 'decrease'
                    recommendations.append({
                        'resource': str(row[resource_column]),
                        'action': action,
                        'current_allocation': round(float(row['current_allocation']), 2),
                        'optimal_allocation': round(float(row['optimal_allocation']), 2),
                        'change_amount': round(float(row['allocation_change']), 2),
                        'change_percentage': round(float(row['allocation_change_pct']), 2)
                    })
            
            return {
                'resource_analysis': resource_performance.to_dict('records'),
                'recommendations': recommendations,
                'total_budget': budget,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Resource allocation error: {str(e)}")
            return {'status': 'error', 'message': str(e)}

