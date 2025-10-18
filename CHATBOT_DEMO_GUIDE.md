# Chatbot Demo Guide

## New Features Added

### 1. **Chatbot Interface with CSV Upload**
- Upload any CSV file
- Ask natural language questions
- Get instant AI-powered responses

### 2. **Model Accuracy Page**
- Detailed metrics for all 3 models
- Visual performance indicators
- Accuracy scores and error rates

### 3. **Demo CSV Files**
Two ready-to-use demo files:
- `data/sample/retail_demo.csv` - Retail sales data
- `data/sample/ecommerce_demo.csv` - E-commerce orders

---

## How to Use the Chatbot

### Step 1: Access the Dashboard
Open: **http://localhost:8501**

### Step 2: Navigate to Chatbot Page
Click **"Chatbot (Upload & Query)"** in the sidebar

### Step 3: Upload a CSV File
- Click "Browse files" button
- Upload one of the demo files:
  - `data/sample/retail_demo.csv`
  - `data/sample/ecommerce_demo.csv`
  - `data/sample/sales_data.csv`
  - Or your own CSV file

### Step 4: Ask Questions
Try these example questions:

#### Revenue Questions
- "What is the total revenue?"
- "Show me the revenue breakdown"
- "What's the average revenue per transaction?"

#### Product Questions
- "What are the top 5 products?"
- "Which products sell the most?"
- "Show me product performance"

#### Regional Analysis
- "Which region has the highest sales?"
- "Compare sales across regions"
- "Show me regional breakdown"

#### Trends & Forecasting
- "What are the trends in the data?"
- "Can you forecast next month?"
- "Predict future sales"

#### General Questions
- "Give me a summary of the data"
- "What insights can you find?"
- "Analyze this dataset"

---

## Model Accuracy Page

### What's Displayed

1. **Time Series Forecasting Model**
   - MAE (Mean Absolute Error): $1,409.59
   - MAPE (Mean Absolute Percentage Error): 102.18%
   - Accuracy calculation
   - Performance interpretation

2. **XGBoost Regression Model**
   - R² Score
   - MAE (Mean Absolute Error)
   - RMSE (Root Mean Squared Error)
   - Feature importance chart

3. **Churn Prediction Model**
   - Total users analyzed
   - Predicted churn rate
   - High-risk users count
   - Risk distribution pie chart

4. **Model Comparison Matrix**
   - Side-by-side comparison
   - Use cases for each model
   - Performance metrics

---

## Demo CSV Files Details

### retail_demo.csv
- **25 rows** of retail transaction data
- **Columns:** date, product_name, category, quantity_sold, unit_price, total_revenue, customer_id, region, payment_method
- **Use cases:** Revenue analysis, product performance, regional comparison

### ecommerce_demo.csv
- **15 rows** of e-commerce order data
- **Columns:** order_id, customer_name, product, category, quantity, price, shipping_cost, order_date, delivery_date, status, rating
- **Use cases:** Order analysis, delivery tracking, customer satisfaction

### sales_data.csv (Original)
- **50 rows** of sales data
- **Columns:** date, product, category, quantity, price, revenue, customer_id, region
- **Use cases:** Complete analytics pipeline demo

---

## Screenshots to Take

### Chatbot Page
1. **Before upload** - Empty state with upload button
   - Screenshot: `chatbot_empty.png`

2. **After upload** - Data preview shown
   - Screenshot: `chatbot_uploaded.png`

3. **Question asked** - User message visible
   - Screenshot: `chatbot_question.png`

4. **AI response** - Assistant response with insights
   - Screenshot: `chatbot_response.png`

5. **Conversation flow** - Multiple Q&A exchanges
   - Screenshot: `chatbot_conversation.png`

### Model Accuracy Page
1. **Overall metrics** - Top KPI cards
   - Screenshot: `model_accuracy_overview.png`

2. **Time Series Model** - MAE, MAPE, Accuracy
   - Screenshot: `model_timeseries.png`

3. **XGBoost Model** - R², MAE, RMSE, Feature Importance
   - Screenshot: `model_xgboost.png`

4. **Churn Model** - Risk distribution pie chart
   - Screenshot: `model_churn.png`

5. **Comparison Matrix** - All models compared
   - Screenshot: `model_comparison.png`

---

## Tips for Better Screenshots

1. **Upload Demo Files**: Use the provided demo CSVs for consistent results

2. **Ask Varied Questions**: 
   - Start with simple ("What is total revenue?")
   - Move to complex ("Analyze trends and forecast")

3. **Show Interactivity**:
   - Capture data preview expansion
   - Show quick statistics
   - Display multiple chat messages

4. **Highlight Key Metrics**:
   - Zoom in on accuracy scores
   - Capture error metrics clearly
   - Show performance indicators

5. **Full Page Views**: Capture entire page layout for context

---

## Quick Test Script

```python
# Test the chatbot with these questions in sequence:
questions = [
    "What is the total revenue?",
    "Show me the top 5 products",
    "Which region has the highest sales?",
    "What are the trends?",
    "Can you forecast next month's sales?"
]

# Upload: retail_demo.csv
# Ask each question
# Screenshot the responses
```

---

## Troubleshooting

**Chatbot not responding?**
- Check if file is uploaded
- Verify column names in your CSV
- Try simpler questions first

**Model accuracy showing N/A?**
- Run `python demo_run.py` first to generate results
- Check if results/*.json files exist

**Upload failing?**
- Check file size (should be < 50MB)
- Verify it's a valid CSV file
- Check for encoding issues

---

## After Screenshots

Save all screenshots to: `screenshots/chatbot/` and `screenshots/models/`

Then:
1. Update README with chatbot demo images
2. Add model accuracy screenshots
3. Commit to GitHub

---

**Enhanced Dashboard Running at: http://localhost:8501** 🚀

