# Screenshot Guide for Results

## What to Capture

### 1. Streamlit Dashboard (Main UI)
**URL:** http://localhost:8501

#### Pages to Screenshot:
1. **Overview Page** (Home)
   - Shows: KPIs, Performance metrics, Top recommendations
   - Key metrics: Total Revenue, Customers, Churn Rate
   - Screenshot name: `dashboard_overview.png`

2. **Descriptive Analytics Page**
   - Shows: KPIs, Revenue metrics, Trend analysis
   - Screenshot name: `dashboard_descriptive.png`

3. **Predictive Models Page**
   - Shows: Forecast chart, Model performance (MAE, MAPE)
   - Churn prediction with risk distribution pie chart
   - Screenshot name: `dashboard_predictive.png`

4. **Recommendations Page**
   - Shows: 8 actionable recommendations with priorities
   - Screenshot name: `dashboard_recommendations.png`

5. **Visualizations Page**
   - Select each chart from dropdown:
     - Revenue Trend
     - Product Performance  
     - Correlation Matrix
     - Forecast
   - Screenshot name: `dashboard_viz_[chartname].png`

6. **Raw Data Page**
   - Shows: Data table with filters
   - Screenshot name: `dashboard_data.png`

---

### 2. HTML Visualizations (Interactive Charts)
**Location:** `results/images/`

Open each HTML file in browser and screenshot:

1. **revenue_trend.html**
   - Interactive time series chart
   - Screenshot name: `chart_revenue_trend.png`

2. **product_performance.html**
   - Bar chart showing product comparison
   - Screenshot name: `chart_product_performance.png`

3. **correlation_matrix.html**
   - Heatmap showing variable correlations
   - Screenshot name: `chart_correlation_matrix.png`

4. **forecast_30days.html**
   - Forecast with confidence intervals
   - Screenshot name: `chart_forecast.png`

---

### 3. PDF Report
**Location:** `reports/generated/analytics_report_*.pdf`

Open the PDF and screenshot:
- Page 1: Title page
- Page 2: Executive summary
- Page 3: Data overview and statistics
- Screenshot names: `report_page1.png`, `report_page2.png`, etc.

---

### 4. Terminal/Console Output
**Show the demo execution:**
```bash
python demo_run.py
```
Screenshot the output showing:
- All 7 stages completing
- Performance metrics
- Model accuracy
- Screenshot name: `terminal_demo_execution.png`

---

### 5. Results Folder Structure
**Show the generated files:**
```bash
ls -lh results/
ls -lh results/images/
```
Screenshot name: `results_folder.png`

---

## Quick Commands to Open Everything

```bash
# Dashboard (Main UI)
open http://localhost:8501

# HTML Visualizations
open results/images/revenue_trend.html
open results/images/product_performance.html
open results/images/correlation_matrix.html
open results/images/forecast_30days.html

# PDF Report
open reports/generated/analytics_report_*.pdf

# Results folder
open results/
```

---

## Screenshot Tips

1. **Full Window**: Capture the entire browser window
2. **High Resolution**: Use at least 1920x1080 resolution
3. **Clean Background**: Close unnecessary tabs/windows
4. **Annotations**: You can add arrows/highlights after if needed
5. **Naming**: Use descriptive names as suggested above

---

## Where to Save Screenshots

Save all screenshots to: `screenshots/` folder

Suggested structure:
```
screenshots/
├── dashboard_overview.png
├── dashboard_descriptive.png
├── dashboard_predictive.png
├── dashboard_recommendations.png
├── dashboard_viz_revenue.png
├── dashboard_viz_product.png
├── dashboard_viz_correlation.png
├── dashboard_viz_forecast.png
├── dashboard_data.png
├── chart_revenue_trend.png
├── chart_product_performance.png
├── chart_correlation_matrix.png
├── chart_forecast.png
├── report_page1.png
├── report_page2.png
├── terminal_demo_execution.png
└── results_folder.png
```

---

## After Screenshots

1. Move all screenshots to `screenshots/` folder
2. Update README.md with screenshot embeds
3. Commit and push to GitHub

---

## Troubleshooting

**Dashboard not loading?**
```bash
# Check if it's running
lsof -i :8501

# Restart if needed
pkill -f streamlit
streamlit run dashboard.py --server.port 8501
```

**HTML files not opening?**
```bash
# Open manually in browser
# Copy full path and paste in browser address bar
pwd  # Get current directory
# Then navigate to results/images/ in browser
```

**Port already in use?**
```bash
# Use different port
streamlit run dashboard.py --server.port 8502
```

---

## Quick Screenshot Checklist

- [ ] Dashboard Overview page
- [ ] Dashboard Descriptive Analytics page
- [ ] Dashboard Predictive Models page
- [ ] Dashboard Recommendations page
- [ ] Dashboard Visualizations (all 4 charts)
- [ ] Dashboard Raw Data page
- [ ] HTML: Revenue Trend chart
- [ ] HTML: Product Performance chart
- [ ] HTML: Correlation Matrix
- [ ] HTML: 30-Day Forecast
- [ ] PDF Report (2-3 pages)
- [ ] Terminal execution output
- [ ] Results folder structure

**Total Screenshots Needed: ~15-20 images**

---

**Ready to screenshot! Dashboard is running at http://localhost:8501** 🎉

