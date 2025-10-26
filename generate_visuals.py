"""
Generate Visual Outputs from Analytics Results
Converts Plotly JSON to HTML and PNG files
"""
import json
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

print("="*80)
print("GENERATING VISUAL OUTPUTS")
print("="*80)

results_dir = Path('results')
images_dir = Path('results/images')
images_dir.mkdir(exist_ok=True)

charts = {
    'chart_timeseries.json': 'revenue_trend.html',
    'chart_bar.json': 'product_performance.html',
    'chart_heatmap.json': 'correlation_matrix.html',
    'chart_forecast.json': 'forecast_30days.html'
}

print("\nConverting Plotly charts to HTML...")
for json_file, html_file in charts.items():
    json_path = results_dir / json_file
    html_path = images_dir / html_file
    
    if json_path.exists():
        with open(json_path, 'r') as f:
            fig_dict = json.load(f)
        
        fig = go.Figure(fig_dict)
        
        # Save as HTML (interactive)
        fig.write_html(str(html_path))
        print(f" {html_file}")
        
        # Try to save as PNG if kaleido is available
        try:
            png_file = html_file.replace('.html', '.png')
            png_path = images_dir / png_file
            fig.write_image(str(png_path), width=1200, height=600)
            print(f" {png_file}")
        except Exception as e:
            print(f"  (PNG skipped - install kaleido: pip install kaleido)")

print("\n" + "="*80)
print("HTML VISUALIZATIONS CREATED")
print("="*80)
print(f"Location: {images_dir}/")
print("\nGenerated files:")
for html_file in charts.values():
    print(f"  - {html_file}")

print("\nTo view:")
print(f"  open {images_dir}/revenue_trend.html")
print(f"  open {images_dir}/product_performance.html")
print(f"  open {images_dir}/correlation_matrix.html")
print(f"  open {images_dir}/forecast_30days.html")
print("="*80)

