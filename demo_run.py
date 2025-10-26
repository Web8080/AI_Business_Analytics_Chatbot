"""
Comprehensive Demo Script - Train Models, Generate Analytics, Create Reports
"""
import sys
from pathlib import Path
import json
import pandas as pd
from datetime import datetime
import time

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_ingestion.csv_parser import CSVParser
from src.data_cleaning.cleaner import DataCleaner
from src.analytics.descriptive import DescriptiveAnalytics
from src.analytics.diagnostic import DiagnosticAnalytics
from src.analytics.predictive import PredictiveAnalytics
from src.analytics.prescriptive import PrescriptiveAnalytics
from src.visualization.charts import ChartGenerator
from src.reports.generator import ReportGenerator

print("="*80)
print("AI ANALYTICS INTELLIGENCE SYSTEM - COMPREHENSIVE DEMO")
print("="*80)
print()

# Initialize components
csv_parser = CSVParser()
data_cleaner = DataCleaner()
descriptive = DescriptiveAnalytics()
diagnostic = DiagnosticAnalytics()
predictive = PredictiveAnalytics()
prescriptive = PrescriptiveAnalytics()
chart_gen = ChartGenerator()
report_gen = ReportGenerator()

results = {
    'timestamp': datetime.now().isoformat(),
    'stages': {}
}

# Stage 1: Load and Clean Data
print("STAGE 1: DATA INGESTION & CLEANING")
print("-" * 80)
start_time = time.time()

parse_result = csv_parser.parse_csv('data/sample/sales_data.csv')
print(f" Loaded sales data: {parse_result['rows']} rows, {parse_result['columns']} columns")

df = parse_result['dataframe']
cleaned_df, cleaning_report = data_cleaner.clean_dataframe(df)
print(f" Data cleaned: {len(cleaned_df)} rows after cleaning")
print(f"  - Duplicates removed: {cleaning_report['rows_removed']}")
print(f"  - Quality score: {data_cleaner.validate_data_quality(cleaned_df)['quality_score']}/100")

results['stages']['data_ingestion'] = {
    'duration': time.time() - start_time,
    'rows_loaded': parse_result['rows'],
    'rows_after_cleaning': len(cleaned_df),
    'quality_score': data_cleaner.validate_data_quality(cleaned_df)['quality_score']
}

# Save cleaned data
cleaned_df.to_csv('results/cleaned_sales_data.csv', index=False)
print(f" Saved cleaned data to results/cleaned_sales_data.csv")
print()

# Stage 2: Descriptive Analytics
print("STAGE 2: DESCRIPTIVE ANALYTICS")
print("-" * 80)
start_time = time.time()

summary = descriptive.generate_summary_statistics(cleaned_df)
print(f" Summary Statistics Generated")
print(f"  - Numeric columns: {len(summary['numeric_columns'])}")
print(f"  - Categorical columns: {len(summary['categorical_columns'])}")

# Save summary
with open('results/descriptive_summary.json', 'w') as f:
    json.dump(summary, f, indent=2, default=str)
print(f" Saved to results/descriptive_summary.json")

# KPI Calculation
kpi_config = {
    'revenue_column': 'revenue',
    'customer_column': 'customer_id',
    'product_column': 'product',
    'date_column': 'date'
}
kpis = descriptive.calculate_kpis(cleaned_df, kpi_config)
print(f" KPIs Calculated:")
if 'revenue' in kpis:
    print(f"  - Total Revenue: ${kpis['revenue']['total_revenue']:,.2f}")
    print(f"  - Average Revenue: ${kpis['revenue']['average_revenue']:,.2f}")
if 'customers' in kpis:
    print(f"  - Total Customers: {kpis['customers']['total_customers']}")

# Trend Analysis
trends = descriptive.analyze_trends(cleaned_df, 'date', ['revenue', 'quantity'])
print(f" Trend Analysis:")
for col, trend in trends.get('trends', {}).items():
    print(f"  - {col}: {trend['direction']} ({trend['percent_change']:+.1f}%)")

# Correlation Analysis
corr_analysis = descriptive.correlation_analysis(cleaned_df)
print(f" Correlation Analysis: {len(corr_analysis.get('strong_correlations', []))} strong correlations found")

results['stages']['descriptive'] = {
    'duration': time.time() - start_time,
    'kpis': kpis,
    'trends': trends,
    'correlations': len(corr_analysis.get('strong_correlations', []))
}

# Save all descriptive analytics
with open('results/kpis.json', 'w') as f:
    json.dump(kpis, f, indent=2, default=str)
with open('results/trends.json', 'w') as f:
    json.dump(trends, f, indent=2, default=str)
with open('results/correlations.json', 'w') as f:
    json.dump(corr_analysis, f, indent=2, default=str)
print()

# Stage 3: Diagnostic Analytics
print("STAGE 3: DIAGNOSTIC ANALYTICS")
print("-" * 80)
start_time = time.time()

# Root Cause Analysis
root_causes = diagnostic.root_cause_analysis(
    cleaned_df, 
    'revenue', 
    ['region', 'category', 'product']
)
print(f" Root Cause Analysis:")
print(f"  - {root_causes['total_causes_found']} potential causes identified")
if root_causes['root_causes']:
    top_cause = root_causes['root_causes'][0]
    print(f"  - Top factor: {top_cause['segment']} ({top_cause['impact_percentage']:.1f}% impact)")

# Segment Analysis
segment_analysis = diagnostic.segment_analysis(cleaned_df, 'region', ['revenue', 'quantity'])
print(f" Segment Analysis: {segment_analysis['total_segments']} segments analyzed")

# Anomaly Detection
anomalies = diagnostic.anomaly_detection(cleaned_df, ['revenue', 'quantity', 'price'])
print(f" Anomaly Detection: {anomalies['total_anomalies']} anomalies detected")

results['stages']['diagnostic'] = {
    'duration': time.time() - start_time,
    'root_causes_found': root_causes['total_causes_found'],
    'segments': segment_analysis['total_segments'],
    'anomalies': anomalies['total_anomalies']
}

# Save diagnostic results
with open('results/root_causes.json', 'w') as f:
    json.dump(root_causes, f, indent=2, default=str)
with open('results/segment_analysis.json', 'w') as f:
    json.dump(segment_analysis, f, indent=2, default=str)
with open('results/anomalies.json', 'w') as f:
    json.dump(anomalies, f, indent=2, default=str)
print()

# Stage 4: Predictive Analytics
print("STAGE 4: PREDICTIVE ANALYTICS (TRAINING MODELS)")
print("-" * 80)
start_time = time.time()

# Time Series Forecasting
print("Training: Time Series Forecast (30 days ahead)...")
forecast_result = predictive.forecast_time_series(
    cleaned_df, 
    'date', 
    'revenue', 
    periods=30,
    model_type='statistical'
)
if forecast_result['status'] == 'success':
    print(f" Forecast Model Trained")
    print(f"  - Model Type: {forecast_result['model_type']}")
    if 'historical_performance' in forecast_result:
        perf = forecast_result['historical_performance']
        print(f"  - MAE: ${perf['mae']:,.2f}")
        print(f"  - MAPE: {perf['mape']:.2f}%")
    print(f"  - Forecast periods: {len(forecast_result['forecast'])}")

# XGBoost Prediction
print("Training: XGBoost Prediction Model...")
feature_columns = ['quantity', 'price']
xgb_result = predictive.predict_with_xgboost(
    cleaned_df, 
    'revenue', 
    feature_columns
)
if xgb_result['status'] == 'success':
    print(f" XGBoost Model Trained")
    print(f"  - R² Score: {xgb_result['performance']['r2_score']:.4f}")
    print(f"  - MAE: ${xgb_result['performance']['mae']:,.2f}")
    print(f"  - RMSE: ${xgb_result['performance']['rmse']:,.2f}")
    print(f"  - Top Feature: {list(xgb_result['feature_importance'].keys())[0]}")

# Churn Prediction
print("Training: Customer Churn Prediction...")
churn_result = predictive.predict_churn(
    cleaned_df,
    'revenue',
    'customer_id',
    'date',
    threshold_days=15
)
if churn_result['status'] == 'success':
    print(f" Churn Model Completed")
    print(f"  - Total Users: {churn_result['total_users']}")
    print(f"  - Churn Rate: {churn_result['churn_rate']:.1f}%")
    print(f"  - High Risk Users: {len(churn_result['high_risk_users'])}")

results['stages']['predictive'] = {
    'duration': time.time() - start_time,
    'forecast': {
        'model': forecast_result.get('model_type'),
        'mae': forecast_result.get('historical_performance', {}).get('mae'),
        'mape': forecast_result.get('historical_performance', {}).get('mape')
    },
    'xgboost': {
        'r2_score': xgb_result.get('performance', {}).get('r2_score'),
        'mae': xgb_result.get('performance', {}).get('mae'),
        'rmse': xgb_result.get('performance', {}).get('rmse')
    },
    'churn': {
        'total_users': churn_result.get('total_users'),
        'churn_rate': churn_result.get('churn_rate')
    }
}

# Save predictive results
with open('results/forecast.json', 'w') as f:
    json.dump(forecast_result, f, indent=2, default=str)
with open('results/xgboost_prediction.json', 'w') as f:
    json.dump(xgb_result, f, indent=2, default=str)
with open('results/churn_prediction.json', 'w') as f:
    json.dump(churn_result, f, indent=2, default=str)
print()

# Stage 5: Prescriptive Analytics
print("STAGE 5: PRESCRIPTIVE ANALYTICS (RECOMMENDATIONS)")
print("-" * 80)
start_time = time.time()

# Generate recommendations from all analyses
combined_results = {
    'trends': trends.get('trends', {}),
    'root_causes': root_causes['root_causes'][:5],
    'forecast': forecast_result.get('forecast', [])[:5],
    'anomalies': anomalies.get('anomalies', {})
}

recommendations = prescriptive.generate_recommendations(combined_results)
print(f" Generated {recommendations['total_recommendations']} recommendations")
for i, rec in enumerate(recommendations['recommendations'][:5], 1):
    print(f"  {i}. [{rec['priority'].upper()}] {rec['recommendation'][:80]}...")

# Inventory Optimization
inventory_opt = prescriptive.optimize_inventory(
    cleaned_df,
    'product',
    'quantity',
    lead_time_days=7
)
print(f" Inventory Optimization:")
print(f"  - Products analyzed: {inventory_opt['total_products']}")
print(f"  - Reorder recommendations: {inventory_opt['products_needing_reorder']}")

# Pricing Optimization
pricing_opt = prescriptive.optimize_pricing(
    cleaned_df,
    'price',
    'quantity',
    ['region']
)
print(f" Pricing Optimization:")
print(f"  - Optimal Price: ${pricing_opt['optimal_price']:.2f}")
print(f"  - Current Avg: ${pricing_opt['current_avg_price']:.2f}")

results['stages']['prescriptive'] = {
    'duration': time.time() - start_time,
    'recommendations': recommendations['total_recommendations'],
    'inventory_items': inventory_opt['products_needing_reorder'],
    'pricing': {
        'optimal': pricing_opt['optimal_price'],
        'current': pricing_opt['current_avg_price']
    }
}

# Save prescriptive results
with open('results/recommendations.json', 'w') as f:
    json.dump(recommendations, f, indent=2, default=str)
with open('results/inventory_optimization.json', 'w') as f:
    json.dump(inventory_opt, f, indent=2, default=str)
with open('results/pricing_optimization.json', 'w') as f:
    json.dump(pricing_opt, f, indent=2, default=str)
print()

# Stage 6: Generate Visualizations
print("STAGE 6: GENERATING VISUALIZATIONS")
print("-" * 80)
start_time = time.time()

# Time series chart
ts_chart = chart_gen.create_time_series_chart(
    cleaned_df, 'date', ['revenue'], 
    title="Daily Revenue Trend"
)
if ts_chart['status'] == 'success':
    with open('results/chart_timeseries.json', 'w') as f:
        f.write(ts_chart['figure'])
    print(" Time Series Chart created")

# Bar chart
bar_chart = chart_gen.create_bar_chart(
    cleaned_df, 'product', 'revenue',
    title="Revenue by Product"
)
if bar_chart['status'] == 'success':
    with open('results/chart_bar.json', 'w') as f:
        f.write(bar_chart['figure'])
    print(" Bar Chart created")

# Correlation heatmap
if corr_analysis['status'] == 'success':
    corr_df = pd.DataFrame(corr_analysis['correlation_matrix'])
    heatmap = chart_gen.create_correlation_heatmap(
        corr_df,
        title="Feature Correlation Matrix"
    )
    if heatmap['status'] == 'success':
        with open('results/chart_heatmap.json', 'w') as f:
            f.write(heatmap['figure'])
        print(" Correlation Heatmap created")

# Forecast chart
if forecast_result['status'] == 'success':
    forecast_df = pd.DataFrame(forecast_result['forecast'])
    forecast_chart = chart_gen.create_forecast_chart(
        cleaned_df, forecast_df, 'date', 'revenue',
        title="30-Day Revenue Forecast"
    )
    if forecast_chart['status'] == 'success':
        with open('results/chart_forecast.json', 'w') as f:
            f.write(forecast_chart['figure'])
        print(" Forecast Chart created")

print(" All visualizations saved to results/ folder")
print()

# Stage 7: Generate PDF Report
print("STAGE 7: GENERATING COMPREHENSIVE REPORT")
print("-" * 80)
start_time = time.time()

metadata = {
    'filename': 'sales_data.csv',
    'rows': len(cleaned_df),
    'columns': len(cleaned_df.columns),
    'column_names': cleaned_df.columns.tolist()
}

report_path = report_gen.generate_comprehensive_report(
    cleaned_df,
    metadata,
    report_type="comprehensive",
    include_visualizations=True
)

print(f" PDF Report Generated: {report_path}")
print()

# Save master results file
results['total_duration'] = sum(stage['duration'] for stage in results['stages'].values())
with open('results/demo_results_summary.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

# Generate Performance Summary
print("="*80)
print("PERFORMANCE SUMMARY")
print("="*80)
print(f"Total Execution Time: {results['total_duration']:.2f} seconds")
print()
for stage_name, stage_data in results['stages'].items():
    print(f"{stage_name.upper()}: {stage_data['duration']:.2f}s")
print()

print("="*80)
print("MODEL ACCURACY & PERFORMANCE METRICS")
print("="*80)
if 'predictive' in results['stages']:
    pred = results['stages']['predictive']
    
    print("\n1. TIME SERIES FORECAST:")
    if pred['forecast']['mae']:
        print(f"   - Mean Absolute Error: ${pred['forecast']['mae']:,.2f}")
        print(f"   - Mean Absolute Percentage Error: {pred['forecast']['mape']:.2f}%")
        print(f"   - Model: {pred['forecast']['model']}")
    
    print("\n2. XGBOOST REGRESSION:")
    if pred['xgboost']['r2_score']:
        print(f"   - R² Score: {pred['xgboost']['r2_score']:.4f} (variance explained)")
        print(f"   - Mean Absolute Error: ${pred['xgboost']['mae']:,.2f}")
        print(f"   - Root Mean Squared Error: ${pred['xgboost']['rmse']:,.2f}")
        accuracy_pct = pred['xgboost']['r2_score'] * 100
        print(f"   - Accuracy: {accuracy_pct:.2f}%")
    
    print("\n3. CHURN PREDICTION:")
    if pred['churn']['total_users']:
        print(f"   - Users Analyzed: {pred['churn']['total_users']}")
        print(f"   - Predicted Churn Rate: {pred['churn']['churn_rate']:.1f}%")

print("\n" + "="*80)
print("OUTPUTS GENERATED")
print("="*80)
print(" results/")
print("   - cleaned_sales_data.csv")
print("   - descriptive_summary.json")
print("   - kpis.json")
print("   - trends.json")
print("   - correlations.json")
print("   - root_causes.json")
print("   - segment_analysis.json")
print("   - anomalies.json")
print("   - forecast.json")
print("   - xgboost_prediction.json")
print("   - churn_prediction.json")
print("   - recommendations.json")
print("   - inventory_optimization.json")
print("   - pricing_optimization.json")
print("   - chart_*.json (Plotly charts)")
print(f"   - {report_path.name} (PDF Report)")
print("   - demo_results_summary.json")
print()
print("="*80)
print("DEMO COMPLETE! Check results/ folder for all outputs.")
print("="*80)

