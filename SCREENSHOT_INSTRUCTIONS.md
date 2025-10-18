# 📸 Screenshot Instructions for README

## How to Add Dashboard Screenshots to GitHub

### Step 1: Take Screenshots
1. Open your dashboard: `streamlit run dashboard_ai.py`
2. Navigate to: http://localhost:8501

### Step 2: Capture These 4 Key Screenshots

#### 1. Dashboard Overview (`dashboard_overview.png`)
- Take a full-screen screenshot showing:
  - Left sidebar with "Upload Data" section
  - File uploaded (retail_demo.csv)
  - Data preview showing rows/columns
  - Main dashboard interface

#### 2. Chatbot Interface (`chatbot_interface.png`)
- Upload a CSV file
- Ask a valid question like "show me top 5 products"
- Capture the AI response with:
  - Question in chat bubble
  - AI answer with metrics
  - Confidence score
  - Auto-generated chart

#### 3. Analytics Results (`analytics_results.png`)
- Ask "what is the total revenue?"
- Capture:
  - AI response with total revenue
  - Key metrics cards (Total, Average, Count)
  - Strategic recommendations section
  - Query details with SQL

#### 4. Vague Question Handling (`vague_question_handling.png`)
- Ask a vague question like "hi" or "weather"
- Capture:
  - AI's polite redirect response
  - Confidence: 30%
  - 6 suggested questions with icons
  - "Try asking:" section

### Step 3: Save Screenshots
1. Save screenshots as PNG files
2. Name them exactly as shown above
3. Place them in: `screenshots/dashboard/`

### Step 4: Replace Placeholder Files
Replace these placeholder files with your actual screenshots:
- `screenshots/dashboard/dashboard_overview.png`
- `screenshots/dashboard/chatbot_interface.png` 
- `screenshots/dashboard/analytics_results.png`
- `screenshots/dashboard/vague_question_handling.png`

### Step 5: Commit and Push
```bash
git add screenshots/
git commit -m "Add dashboard screenshots to README"
git push origin main
```

### Step 6: Verify on GitHub
Visit: https://github.com/Web8080/AI_Business_Analytics_Chatbot
Check that images display properly in the README

## Tips for Good Screenshots
- Use high resolution (1920x1080 or higher)
- Ensure text is readable
- Capture the full interface
- Show the most impressive features
- Use PNG format for best quality
