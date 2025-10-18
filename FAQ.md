# ❓ Frequently Asked Questions (FAQ)

**Quick answers to common questions about the AI Analytics Intelligence System**

---

## 📋 Table of Contents

1. [General Questions](#general-questions)
2. [Getting Started](#getting-started)
3. [Data Upload](#data-upload)
4. [Using the System](#using-the-system)
5. [Charts and Visualizations](#charts-and-visualizations)
6. [OpenAI vs Fallback Mode](#openai-vs-fallback-mode)
7. [Technical Questions](#technical-questions)
8. [Troubleshooting](#troubleshooting)
9. [Performance and Limits](#performance-and-limits)
10. [Privacy and Security](#privacy-and-security)

---

## 🌟 General Questions

### What is the AI Analytics Intelligence System?

It's an AI-powered analytics platform that automatically analyzes your data and answers questions in plain English. Think of it as your personal data analyst - available 24/7, no technical skills required!

### Who is this for?

- **Business owners** who want to understand their data without hiring analysts
- **Managers** who need quick insights for decision-making
- **Analysts** who want to speed up routine analysis
- **Anyone** with CSV data who wants instant insights

### Do I need to know programming or statistics?

No! The system is designed for everyone. Just ask questions in plain English like you would ask a colleague.

### How much does it cost?

The system is free to use. If you want to enable OpenAI GPT-4 mode, you'll need your own OpenAI API key (which costs ~$0.01-0.02 per question). The free Fallback mode works great for most use cases!

### What makes this different from Excel or Google Sheets?

Instead of writing formulas or creating pivot tables, you just ask questions like "What is my total revenue?" or "Show me top products." The AI handles all the technical work and creates visualizations automatically.

---

## 🚀 Getting Started

### How do I install it?

```bash
# 1. Clone from GitHub
git clone https://github.com/Web8080/AI_Business_Analytics_Chatbot.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
./run_openai_dashboard.sh

# 4. Open browser to localhost:8501
```

Detailed instructions are in the README.md file.

### Do I need an OpenAI API key?

No! The system works perfectly without one in "Fallback Mode." If you have an API key, the system will use OpenAI GPT-4 for slightly more advanced natural language understanding.

### How do I get an OpenAI API key?

1. Go to https://platform.openai.com/
2. Create an account
3. Go to API keys section
4. Create a new API key
5. Add it to your `.env` file: `OPENAI_API_KEY=your-key-here`

### Can I use this on Windows/Mac/Linux?

Yes! The system works on all operating systems. You just need Python 3.12+ and a web browser.

### Is there a cloud/hosted version?

Currently, you run it locally on your computer. Cloud deployment is planned for future releases. See NEXT_PHASES.md for the roadmap.

---

## 📁 Data Upload

### What file formats are supported?

Currently, **CSV files only**. PDF support is in development.

To convert other formats:
- **Excel (.xlsx):** File > Save As > CSV
- **Google Sheets:** File > Download > CSV
- **Database:** Use export to CSV function

### How large can my file be?

Up to **200MB per file**. For reference:
- Small dataset: 1-5MB (thousands of rows)
- Medium dataset: 10-50MB (tens of thousands of rows)
- Large dataset: 50-200MB (hundreds of thousands of rows)

Most business datasets are under 10MB.

### What if my file is too large?

Options:
1. **Filter your data** - Export only what you need to analyze
2. **Split into smaller files** - Analyze by time period or category
3. **Compress** - Remove unnecessary columns
4. **Sample** - Take a random sample of rows

### My CSV file has special characters - will it work?

Yes! The system automatically detects encoding (UTF-8, Latin-1, etc.) and handles special characters, currency symbols, and international text.

### Can I upload multiple files?

Currently, you can analyze one file at a time. To switch datasets, simply upload a new file. Multi-file support is planned for future releases.

### Does my CSV need headers?

Yes, the first row should contain column names. For example:
```
date,product,revenue,quantity
2024-01-01,Widget A,100,5
2024-01-02,Widget B,150,3
```

### What if my data has errors?

The system automatically cleans your data:
- Removes duplicate rows
- Handles missing values
- Detects and removes outliers
- Infers correct data types
- Standardizes formats

You'll get a clean dataset ready for analysis!

---

## 💬 Using the System

### How do I ask a question?

1. Make sure you've uploaded a file
2. Go to the "AI Chatbot" tab
3. Type your question in the text box
4. Click "Send" or press Enter
5. Wait 1-2 seconds for the response

### What questions can I ask?

**Basic Statistics:**
- "What is the total revenue?"
- "How many customers?"
- "What is the average sale?"

**Rankings:**
- "Show me top 5 products"
- "What are the best sellers?"
- "Bottom 10 by revenue"

**Trends:**
- "Show me trends over time"
- "Is revenue growing?"
- "How are sales performing?"

**Comparisons:**
- "Compare categories"
- "This month vs last month"
- "Best performing region"

**Recommendations:**
- "What should I focus on?"
- "What are my opportunities?"
- "What's working well?"

See USER_MANUAL.md for 100+ example questions!

### The AI didn't understand my question - what do I do?

Try these steps:
1. **Rephrase** - Be more specific
2. **Simplify** - Ask one thing at a time
3. **Use different words** - "total" instead of "sum"
4. **Click Quick Actions** - Pre-configured questions
5. **Check confidence score** - Low score means uncertain answer

### What are Quick Actions?

Quick Action buttons for common questions:
- **Show Summary** - Overview of your data
- **Top 5 Items** - Highest values with chart
- **Trends** - Time-based analysis with line chart
- **Recommendations** - AI-generated insights

Just click - no typing needed!

### How do I get a chart?

Use words like:
- "Show me..."
- "Visualize..."
- "Create a chart of..."
- "Display..."

Example: "Show me top 5 products" will give you both an answer AND a bar chart.

### Can I export my analysis?

Yes! Two ways:
1. **Export Chat** - Save your entire conversation (CSV or TXT format)
2. **Download Charts** - Hover over any chart, click the camera icon

### How do I clear my chat history?

Click the "Clear Chat" button in the sidebar. Your data stays loaded - only the conversation resets.

---

## 📊 Charts and Visualizations

### What types of charts can the AI create?

Three types:
1. **Bar Charts** - Comparing values (top products, sales by category)
2. **Line Charts** - Trends over time (revenue trends, growth)
3. **Pie Charts** - Proportions/percentages (market share, distribution)

The AI automatically chooses the right type based on your question!

### How do I interact with charts?

Charts are fully interactive:
- **Hover** - See exact values
- **Zoom** - Click and drag to zoom in
- **Pan** - Click and drag to move around
- **Reset** - Click "Reset axes" to return to original view
- **Download** - Click camera icon to save as PNG

### Can I customize chart colors or style?

Currently, all charts use a professional dark theme. Custom styling is planned for future releases.

### Why isn't a chart appearing?

Common reasons:
1. **Question doesn't request visualization** - Add "show me" or "visualize"
2. **Data doesn't support that chart type** - Need appropriate columns
3. **Still loading** - Wait 1-2 seconds
4. **Data issue** - Check if your data has the right format

### Can I use charts in presentations?

Absolutely! Download any chart as a PNG image and insert into:
- PowerPoint
- Google Slides
- Keynote
- Word/Google Docs
- Emails
- Reports

Charts maintain professional quality at any size!

---

## 🤖 OpenAI vs Fallback Mode

### What's the difference between the two modes?

**OpenAI Mode** (requires API key):
- Uses GPT-4 for natural language understanding
- Better at complex or unusual questions
- Slightly slower (~2-3 seconds)
- Costs ~$0.01-0.02 per question
- Requires internet

**Fallback Mode** (no API key needed):
- Uses rule-based system with 100,000+ patterns
- Fast responses (~0.5 seconds)
- Completely free
- Works offline
- Great for standard business questions

### Which mode should I use?

**Use Fallback Mode if:**
- You don't have an OpenAI API key
- You want faster responses
- You're asking standard business questions
- You want to keep costs at zero
- You need offline capability

**Use OpenAI Mode if:**
- You have an API key
- You ask complex or unusual questions
- You want more conversational responses
- Cost isn't a concern

**Honest answer:** Both modes work great! Most users won't notice a difference for typical business questions.

### How do I know which mode I'm in?

Look at the top of the dashboard. You'll see either:
- "🟢 OpenAI GPT-4 Powered Mode" - Using OpenAI
- "🟡 Fallback Mode (Advanced Rules)" - Using rule-based system

### Can I switch between modes?

Yes! Just add or remove your `OPENAI_API_KEY` from the `.env` file and restart the dashboard.

### What happens if OpenAI fails?

The system automatically falls back to rule-based mode! You'll still get an answer - the system never crashes or hangs.

---

## 🔧 Technical Questions

### What technology is this built with?

**Core Stack:**
- Python 3.12
- Streamlit (dashboard)
- OpenAI GPT-4 (optional)
- Plotly (charts)
- Pandas (data processing)
- FastAPI (REST API)

See DEVELOPER_GUIDE.md for complete tech stack.

### Can I self-host this?

Yes! It's designed to run on your own computer or server. See README.md for deployment options.

### Is there an API I can use?

Yes! FastAPI endpoints are available:
- `POST /api/upload` - Upload data
- `POST /api/analyze` - Run analysis
- `POST /api/ask` - Ask question
- `POST /api/generate-report` - Create report

See API_DOCUMENTATION.md for full API reference (coming soon).

### Can I integrate this into my application?

Yes! You can:
1. Use the REST API endpoints
2. Import Python modules directly
3. Embed the Streamlit dashboard in an iframe
4. Use Docker for containerized deployment

See DEVELOPER_GUIDE.md for integration examples.

### How do I contribute to development?

We welcome contributions!
1. Fork the GitHub repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

See DEVELOPER_GUIDE.md for contribution guidelines.

---

## 🔍 Troubleshooting

### Dashboard won't load

**Solutions:**
1. Check if the system is running (`http://localhost:8501`)
2. Refresh browser (F5 or Cmd+R)
3. Clear browser cache
4. Try a different browser
5. Check terminal for error messages
6. Restart the system: `./run_openai_dashboard.sh`

### File upload fails

**Solutions:**
1. **Check file format** - Must be .csv
2. **Check file size** - Must be under 200MB
3. **Close file in other programs** - Close Excel/Numbers
4. **Check file permissions** - Ensure you can read the file
5. **Try a different file** - Test with sample data
6. **Refresh and retry** - F5 then try again

### "No data loaded" error

**Solution:**
You need to upload a file first!
1. Look for "Upload Data" in the left sidebar
2. Click "Browse files" and select your CSV
3. Wait for "Data loaded successfully" message
4. Then ask your question

### Charts aren't displaying

**Solutions:**
1. **Ask for visualization** - Use "show me" or "visualize"
2. **Wait** - Charts take 1-2 seconds to generate
3. **Check data** - Need appropriate columns for that chart type
4. **Refresh** - Reload the page
5. **Clear session** - Click "Clear All Data" and re-upload

### Slow performance

**Causes & Solutions:**

**Large file:**
- First analysis takes longer
- Subsequent questions are faster
- Consider filtering your data

**Complex question:**
- Break into simpler questions
- Ask one thing at a time

**Internet (OpenAI mode):**
- Check connection
- Switch to Fallback mode

### OpenAI errors

**Common errors:**

**"Invalid API key":**
- Check your `.env` file
- Verify key is correct
- Make sure it starts with `sk-`

**"Rate limit exceeded":**
- You've hit OpenAI's rate limit
- Wait a few minutes
- Or switch to Fallback mode

**"API timeout":**
- Check internet connection
- Try again
- Or switch to Fallback mode

The system automatically falls back to rule-based mode on any OpenAI error!

---

## ⚡ Performance and Limits

### How fast is the system?

**Response times:**
- Simple questions: 0.5-1 second
- With chart: 1-2 seconds
- Complex analysis: 2-3 seconds
- First upload: 2-5 seconds

**Tested performance:**
- 16 tests, 100% pass rate
- All responses under 2 seconds
- Chart generation under 3 seconds

### How many questions can I ask?

**Unlimited!** Ask as many questions as you need. No daily/monthly limits.

(OpenAI mode has OpenAI's rate limits, but those are very generous for typical use.)

### How many rows/columns can I analyze?

**Tested up to:**
- 1,000,000 rows
- 100 columns
- 200MB file size

**Recommended:**
- Under 100,000 rows for best performance
- Under 50 columns
- Under 50MB

### Does performance degrade with large files?

First analysis takes longer, but subsequent questions remain fast. The system caches results intelligently.

### Can multiple people use this at once?

Each person needs their own instance (their own browser session). For team collaboration, consider:
1. Each person runs their own instance
2. Share exported chat/charts via email/Slack
3. Cloud deployment (planned for future)

---

## 🔒 Privacy and Security

### Is my data safe?

**Yes!** Your data:
- Stays on your computer
- Is never uploaded to external servers (except OpenAI if you use that mode)
- Is not stored permanently
- Is not shared with anyone
- Is deleted when you close the browser or clear data

### Does anyone see my data?

**No!** 

**In Fallback Mode:**
- 100% local processing
- Zero external connections
- Your data never leaves your computer

**In OpenAI Mode:**
- Only your question and relevant data context is sent to OpenAI
- OpenAI's API doesn't train on your data
- Data is encrypted in transit
- See OpenAI's privacy policy for details

### Can I use this with sensitive data?

**Yes**, with precautions:

**Highly Sensitive:**
- Use Fallback Mode only (no external connections)
- Run on isolated network
- Don't share exported files without redacting

**Moderately Sensitive:**
- Fallback Mode recommended
- Be careful with OpenAI Mode
- Review OpenAI's data policies

**Public Data:**
- Either mode is fine

### Where is data stored?

**Temporary storage only:**
- In browser memory (RAM)
- Cleared when you close browser
- Or click "Clear All Data"

**Not stored permanently:**
- No database
- No persistent files
- No data retention

**Exports:**
- Only if you manually export chat/charts
- Saved to your Downloads folder
- You control those files

### Is the system GDPR/HIPAA compliant?

**GDPR:**
- Yes, for Fallback Mode (all local processing)
- Check OpenAI's GDPR compliance for OpenAI Mode

**HIPAA:**
- Local processing is fine
- Do NOT use OpenAI Mode with PHI (Protected Health Information)
- Consider additional security measures for healthcare data

### What data does OpenAI see (if I use OpenAI Mode)?

OpenAI receives:
- Your question
- Sample of your data (5-10 rows typically)
- Column names and types
- Basic statistics

OpenAI does NOT receive:
- Your entire dataset
- Your raw files
- Your personal information (unless it's in the data you uploaded)

According to OpenAI's policy, API data is not used for training.

---

## 🆘 Getting More Help

### Where can I find more documentation?

- **USER_MANUAL.md** - Comprehensive user guide
- **DEVELOPER_GUIDE.md** - Technical documentation
- **VIDEO_TUTORIALS.md** - Step-by-step video scripts
- **README.md** - Project overview
- **NEXT_PHASES.md** - Roadmap and future features

### How do I report a bug?

1. Check if it's in this FAQ
2. Search GitHub Issues
3. If new, create an issue with:
   - What you were trying to do
   - What happened instead
   - Error messages (if any)
   - Steps to reproduce

### How do I request a feature?

1. Check NEXT_PHASES.md to see if it's planned
2. Search GitHub Issues for existing requests
3. Create new issue with `[Feature Request]` tag
4. Describe the feature and why it's useful

### Can I get one-on-one help?

Check the GitHub repository for:
- Discussions board
- Community forum
- Support contact

### Is there a community?

Join our community:
- GitHub Discussions
- Follow for updates
- Contribute to development

---

## 📊 Quick Reference

### Most Common Questions

1. **"How do I start?"**
   - Upload a CSV file, ask a question!

2. **"Why isn't it working?"**
   - Did you upload a file first?

3. **"How do I get a chart?"**
   - Use "show me" or "visualize" in your question

4. **"Do I need OpenAI?"**
   - No! Fallback mode works great

5. **"Where is my data?"**
   - In browser memory, deleted when you close

6. **"Can I save my analysis?"**
   - Yes! Export chat and download charts

7. **"How much does it cost?"**
   - Free! (OpenAI mode costs ~$0.01/question if you use it)

8. **"Is it secure?"**
   - Yes! Data stays local (Fallback mode) or encrypted (OpenAI mode)

9. **"What formats?"**
   - CSV files only

10. **"How do I update?"**
    - `git pull origin main` from project directory

---

## 📞 Contact

- **GitHub:** https://github.com/Web8080/AI_Business_Analytics_Chatbot
- **Issues:** https://github.com/Web8080/AI_Business_Analytics_Chatbot/issues
- **Documentation:** See all .md files in the repository

---

**FAQ Version:** 1.0  
**Last Updated:** October 18, 2025  
**System Version:** Phase 5.1

**Still have questions? Check USER_MANUAL.md or DEVELOPER_GUIDE.md!** 📚

