# 🔧 Developer Guide - AI Analytics Intelligence System

**Technical documentation for developers, contributors, and system administrators.**

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Core Components](#core-components)
6. [AI Engine](#ai-engine)
7. [API Reference](#api-reference)
8. [Database Schema](#database-schema)
9. [Configuration](#configuration)
10. [Testing](#testing)
11. [Deployment](#deployment)
12. [Contributing](#contributing)
13. [Troubleshooting](#troubleshooting)

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│              (Streamlit Dashboard)                   │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Conversational AI Layer                 │
│  ┌──────────────────┬──────────────────────────┐   │
│  │  OpenAIAgent     │  SmartAnalyticsAgent     │   │
│  │  (GPT-4)         │  (Rule-based fallback)   │   │
│  └──────────────────┴──────────────────────────┘   │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Analytics Engine                        │
│  ┌─────────────┬──────────────┬──────────────┐     │
│  │ Descriptive │  Diagnostic  │  Predictive  │     │
│  │  Analytics  │   Analytics  │  Analytics   │     │
│  └─────────────┴──────────────┴──────────────┘     │
│  ┌──────────────────────────────────────────┐       │
│  │        Prescriptive Analytics            │       │
│  └──────────────────────────────────────────┘       │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Data Processing Layer                   │
│  ┌──────────────┬──────────────┬─────────────┐     │
│  │  Ingestion   │   Cleaning   │ Validation  │     │
│  │  (PDF/CSV)   │   Pipeline   │   Engine    │     │
│  └──────────────┴──────────────┴─────────────┘     │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│               Visualization Layer                    │
│         (Plotly Charts + ReportLab)                 │
└─────────────────────────────────────────────────────┘
```

### Data Flow

```
User Upload → Data Ingestion → Data Cleaning → Data Storage
                                                      ↓
User Question → Intent Analysis → Analytics Execution
                                         ↓
                    Chart Generation ← Response Generation
                                         ↓
                              Display to User
```

### Key Design Principles

1. **Modular Architecture** - Each component is independent and replaceable
2. **Fail-Safe Design** - Fallback systems for all critical components
3. **Stateless Processing** - Each request is independent
4. **Session Management** - Streamlit session state for UI persistence
5. **Error Resilience** - Comprehensive error handling at every layer

---

## 💻 Technology Stack

### Core Technologies

#### Backend
- **Python 3.12** - Primary language
- **FastAPI** - REST API framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Pydantic** - Data validation

#### AI/ML
- **OpenAI GPT-4** - Natural language understanding
- **LangChain** - AI agent framework
- **Prophet** - Time series forecasting
- **XGBoost** - Machine learning models
- **scikit-learn** - Statistical analysis
- **FuzzyWuzzy** - Fuzzy string matching

#### Frontend
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive visualizations
- **HTML/CSS** - Custom styling

#### Data Processing
- **pdfplumber** - PDF parsing
- **chardet** - Encoding detection
- **openpyxl** - Excel handling
- **ReportLab** - PDF generation

#### Testing & DevOps
- **pytest** - Testing framework
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Git/GitHub** - Version control

---

## 📂 Project Structure

```
AI_Business_Analytics_Chatbot/
├── src/                          # Source code
│   ├── __init__.py
│   ├── data_ingestion/           # Data import modules
│   │   ├── __init__.py
│   │   ├── pdf_parser.py         # PDF parsing logic
│   │   └── csv_parser.py         # CSV parsing logic
│   ├── data_cleaning/            # Data cleaning pipeline
│   │   ├── __init__.py
│   │   └── cleaner.py            # 6-step cleaning process
│   ├── analytics/                # Analytics engines
│   │   ├── __init__.py
│   │   ├── descriptive.py        # KPIs, trends, correlations
│   │   ├── diagnostic.py         # Root cause, segments
│   │   ├── predictive.py         # Forecasting, ML models
│   │   └── prescriptive.py       # Recommendations
│   ├── conversational/           # AI agents
│   │   ├── __init__.py
│   │   ├── smart_agent.py        # Rule-based agent
│   │   ├── openai_agent.py       # GPT-4 integration
│   │   ├── intent_matcher.py     # 100K+ patterns
│   │   └── agent.py              # LangChain agent (legacy)
│   ├── visualization/            # Chart generation
│   │   ├── __init__.py
│   │   └── charts.py             # Plotly charts
│   ├── reports/                  # Report generation
│   │   ├── __init__.py
│   │   └── generator.py          # PDF reports
│   └── api/                      # REST API
│       ├── __init__.py
│       └── main.py               # FastAPI endpoints
├── tests/                        # Test suites
│   ├── __init__.py
│   ├── test_api.py               # API tests
│   └── test_chatbot_comprehensive.py  # Chatbot tests
├── data/                         # Data directory
│   ├── uploads/                  # User uploads
│   ├── processed/                # Processed data
│   ├── temp/                     # Temporary files
│   └── sample/                   # Sample datasets
│       ├── retail_demo.csv
│       ├── ecommerce_demo.csv
│       ├── sales_data.csv
│       └── customer_records.csv
├── models/                       # ML models
│   └── trained/                  # Trained model files
├── reports/                      # Generated reports
│   └── generated/                # PDF reports
├── results/                      # Analysis results
│   ├── analytics/                # JSON results
│   └── images/                   # Dashboard screenshots
├── scripts/                      # Utility scripts
│   ├── quick_start.sh            # Quick setup
│   └── run_tests.sh              # Test runner
├── dashboard_openai.py           # Main dashboard (OpenAI)
├── dashboard_robust.py           # Alternative dashboard
├── main.py                       # Application entry point
├── demo_run.py                   # Demo script
├── test_openai_integration.py    # Integration test
├── config.py                     # Configuration
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker composition
├── .gitignore                    # Git ignore rules
├── .dockerignore                 # Docker ignore rules
├── env.example                   # Environment template
├── README.md                     # Project documentation
├── USER_MANUAL.md                # User guide
├── DEVELOPER_GUIDE.md            # This file
└── LICENSE                       # MIT License
```

---

## 🚀 Setup and Installation

### Prerequisites

- **Python 3.12+**
- **pip** (Python package manager)
- **Git**
- **Docker** (optional, for containerized deployment)
- **OpenAI API Key** (optional, for GPT-4 integration)

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Web8080/AI_Business_Analytics_Chatbot.git
cd AI_Business_Analytics_Chatbot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (optional)
cp env.example .env
# Edit .env and add your OPENAI_API_KEY if you have one

# 5. Run the dashboard
./run_openai_dashboard.sh
# Or: streamlit run dashboard_openai.py

# 6. Access the dashboard
# Open browser to http://localhost:8501
```

### Docker Setup

```bash
# Build the image
docker-compose build

# Run the container
docker-compose up

# Access at http://localhost:8501
```

### Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run in development mode with auto-reload
streamlit run dashboard_openai.py --server.runOnSave true
```

---

## 🧩 Core Components

### 1. Data Ingestion Module

**Location:** `src/data_ingestion/`

#### CSV Parser (`csv_parser.py`)

```python
from src.data_ingestion.csv_parser import CSVParser

# Initialize
parser = CSVParser()

# Parse CSV file
df = parser.parse('path/to/file.csv')

# With validation
df = parser.parse('path/to/file.csv', validate=True)
```

**Features:**
- Automatic encoding detection (UTF-8, Latin-1, etc.)
- Schema validation
- Error handling for malformed files
- Large file support

#### PDF Parser (`pdf_parser.py`)

```python
from src.data_ingestion.pdf_parser import PDFParser

# Initialize
parser = PDFParser()

# Extract tables from PDF
tables = parser.extract_tables('path/to/file.pdf')

# Get specific page
table = parser.extract_table('path/to/file.pdf', page=1)
```

**Features:**
- Table extraction from multi-page PDFs
- Text extraction
- Header detection
- Layout preservation

### 2. Data Cleaning Pipeline

**Location:** `src/data_cleaning/cleaner.py`

```python
from src.data_cleaning.cleaner import DataCleaner

# Initialize
cleaner = DataCleaner()

# Run full pipeline
cleaned_df = cleaner.clean(raw_df)

# Individual steps
cleaned_df = cleaner.remove_duplicates(df)
cleaned_df = cleaner.handle_missing_values(df)
cleaned_df = cleaner.remove_outliers(df)
cleaned_df = cleaner.infer_types(df)
```

**6-Step Pipeline:**
1. **Duplicate Removal** - Remove exact duplicates
2. **Null Handling** - Fill or remove missing values
3. **Outlier Detection** - Z-score based outlier removal
4. **Type Inference** - Automatic dtype detection
5. **Format Standardization** - Date, currency formatting
6. **Validation** - Data quality checks

### 3. Analytics Engine

**Location:** `src/analytics/`

#### Descriptive Analytics

```python
from src.analytics.descriptive import DescriptiveAnalytics

# Initialize
analytics = DescriptiveAnalytics()

# Get KPIs
kpis = analytics.calculate_kpis(df)
# Returns: {'total_revenue': 16936.23, 'avg_revenue': 677.45, ...}

# Analyze trends
trends = analytics.analyze_trends(df, column='revenue', time_column='date')
# Returns: {'direction': 'increasing', 'change_percent': 15.3, ...}

# Calculate correlations
corr = analytics.calculate_correlations(df)
# Returns: DataFrame with correlation matrix
```

#### Diagnostic Analytics

```python
from src.analytics.diagnostic import DiagnosticAnalytics

# Initialize
analytics = DiagnosticAnalytics()

# Root cause analysis
root_causes = analytics.identify_root_causes(df, target='revenue')

# Segment analysis
segments = analytics.segment_analysis(df, segment_by='category')

# Anomaly detection
anomalies = analytics.detect_anomalies(df, column='revenue')
```

#### Predictive Analytics

```python
from src.analytics.predictive import PredictiveAnalytics

# Initialize
analytics = PredictiveAnalytics()

# Forecast with Prophet
forecast = analytics.forecast_timeseries(
    df, 
    time_column='date',
    value_column='revenue',
    periods=30
)

# Churn prediction with XGBoost
churn_pred = analytics.predict_churn(df, target='churned')
```

#### Prescriptive Analytics

```python
from src.analytics.prescriptive import PrescriptiveAnalytics

# Initialize
analytics = PrescriptiveAnalytics()

# Generate recommendations
recommendations = analytics.generate_recommendations(
    df,
    kpis=kpis,
    trends=trends,
    anomalies=anomalies
)
```

### 4. Conversational AI

**Location:** `src/conversational/`

#### SmartAnalyticsAgent (Fallback)

```python
from src.conversational.smart_agent import SmartAnalyticsAgent

# Initialize
agent = SmartAnalyticsAgent()

# Load data
agent.load_data(df)

# Ask question
response = agent.ask("What is the total revenue?")
# Returns: {
#     'answer': 'Total Revenue: $16,936.23...',
#     'confidence': 0.96,
#     'chart_data': {...},
#     'source': 'fallback'
# }
```

**Features:**
- 100,000+ intent patterns
- Fuzzy matching
- Context awareness
- Vague question handling
- Confidence scoring

#### OpenAIAnalyticsAgent

```python
from src.conversational.openai_agent import OpenAIAnalyticsAgent

# Initialize (requires OPENAI_API_KEY in environment)
agent = OpenAIAnalyticsAgent()

# Load data
agent.load_data(df)

# Ask question
response = agent.ask("Show me trends in product sales")
# Returns: {
#     'answer': 'Based on your data, product sales...',
#     'confidence': 0.95,
#     'chart_data': {...},
#     'source': 'openai'
# }

# Automatically falls back to SmartAnalyticsAgent if:
# - No API key found
# - API error occurs
# - Rate limit exceeded
```

**Features:**
- GPT-4 powered responses
- Dynamic prompt engineering
- Chart type determination
- Automatic fallback
- Context passing

#### Intent Matcher

```python
from src.conversational.intent_matcher import RobustIntentMatcher

# Initialize
matcher = RobustIntentMatcher()

# Match intent
intent = matcher.match_intent("show me the top 5 products")
# Returns: {
#     'intent': 'show_top',
#     'entity': 'product',
#     'n': 5,
#     'confidence': 0.92
# }
```

**Pattern Database:**
- 100,000+ utterance patterns
- Multiple domains (sales, finance, operations, etc.)
- Fuzzy matching (handles typos)
- Multi-language support (planned)

### 5. Visualization Engine

**Location:** `src/visualization/charts.py`

```python
from src.visualization.charts import ChartGenerator

# Initialize
chart_gen = ChartGenerator()

# Generate bar chart
fig = chart_gen.create_bar_chart(
    x=['Product A', 'Product B', 'Product C'],
    y=[100, 150, 120],
    title='Product Sales'
)

# Generate line chart
fig = chart_gen.create_line_chart(
    x=dates,
    y=revenues,
    title='Revenue Trends'
)

# Generate pie chart
fig = chart_gen.create_pie_chart(
    labels=['Category A', 'Category B'],
    values=[60, 40],
    title='Market Share'
)

# Customize
fig.update_layout(template='plotly_dark', height=400)
```

**Chart Types:**
- Bar charts
- Line charts
- Pie charts
- Scatter plots (planned)
- Heatmaps (planned)

---

## 🤖 AI Engine

### Architecture

The AI engine uses a dual-mode approach:

```
User Question
     ↓
OpenAIAnalyticsAgent
     ↓
Has API Key? ──NO──→ SmartAnalyticsAgent (Fallback)
     ↓ YES
     ↓
Call OpenAI GPT-4
     ↓
Success? ──NO──→ SmartAnalyticsAgent (Fallback)
     ↓ YES
     ↓
Return Response
```

### OpenAI Integration

**Prompt Engineering:**

```python
def _create_openai_prompt(self, question: str) -> str:
    """Create optimized prompt for OpenAI"""
    
    # Data context
    data_context = self._get_data_context()
    
    # Build prompt
    prompt = f"""
    You are an expert data analyst. Analyze the following data and answer the question.
    
    DATA CONTEXT:
    {data_context}
    
    QUESTION: {question}
    
    Provide a clear, concise answer with:
    1. Direct answer to the question
    2. Key statistics/numbers
    3. Any relevant insights
    4. Suggest a chart type if visualization would help
    
    Be specific and data-driven.
    """
    
    return prompt
```

**Response Processing:**

```python
def _process_openai_response(self, response: str) -> dict:
    """Extract answer and chart recommendation"""
    
    # Parse response
    answer = self._extract_answer(response)
    chart_type = self._extract_chart_type(response)
    
    # Generate chart if recommended
    chart_data = None
    if chart_type:
        chart_data = self._generate_chart_data(chart_type)
    
    return {
        'answer': answer,
        'chart_data': chart_data,
        'source': 'openai'
    }
```

### Intent Matching Algorithm

**Fuzzy Matching:**

```python
from fuzzywuzzy import fuzz

def match_intent(self, question: str) -> dict:
    """Match question to intent using fuzzy matching"""
    
    best_match = None
    best_score = 0
    
    # Normalize question
    q_norm = question.lower().strip()
    
    # Match against patterns
    for intent, patterns in self.intent_patterns.items():
        for pattern in patterns:
            score = fuzz.ratio(q_norm, pattern)
            if score > best_score:
                best_score = score
                best_match = intent
    
    # Return if confidence sufficient
    if best_score > 70:  # Threshold
        return {
            'intent': best_match,
            'confidence': best_score / 100
        }
    
    return {'intent': 'unknown', 'confidence': 0}
```

**Pattern Categories:**

1. **Aggregation** - sum, total, average, count
2. **Ranking** - top, bottom, best, worst
3. **Comparison** - compare, versus, difference
4. **Trends** - trend, over time, growth
5. **Visualization** - show, display, chart, graph
6. **Recommendations** - suggest, recommend, advise

---

## 🔌 API Reference

### FastAPI Endpoints

**Location:** `src/api/main.py`

#### Upload Data

```http
POST /api/upload
Content-Type: multipart/form-data

Parameters:
  - file: CSV or PDF file

Response:
{
  "success": true,
  "rows": 1000,
  "columns": 15,
  "message": "Data uploaded successfully"
}
```

#### Analyze Data

```http
POST /api/analyze
Content-Type: application/json

Body:
{
  "data_id": "abc123",
  "analysis_type": "descriptive"
}

Response:
{
  "success": true,
  "results": {
    "kpis": {...},
    "trends": {...},
    "correlations": {...}
  }
}
```

#### Ask Question

```http
POST /api/ask
Content-Type: application/json

Body:
{
  "question": "What is the total revenue?",
  "data_id": "abc123"
}

Response:
{
  "answer": "Total Revenue: $16,936.23...",
  "confidence": 0.96,
  "chart_data": {...},
  "source": "openai"
}
```

#### Generate Report

```http
POST /api/generate-report
Content-Type: application/json

Body:
{
  "data_id": "abc123",
  "format": "pdf"
}

Response:
{
  "success": true,
  "report_url": "/reports/abc123.pdf"
}
```

---

## 🗄️ Database Schema

Currently, the system uses **in-memory storage** (Streamlit session state) for simplicity. For production, consider:

### Recommended Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Datasets table
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    filename VARCHAR(255),
    rows INTEGER,
    columns INTEGER,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Analyses table
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    analysis_type VARCHAR(50),
    results JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    question TEXT,
    answer TEXT,
    confidence FLOAT,
    chart_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## ⚙️ Configuration

### Environment Variables

**File:** `.env`

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Application Configuration
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database Configuration (if using)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Analytics Thresholds
CONFIDENCE_THRESHOLD=0.7
OUTLIER_THRESHOLD=3.0
```

### Config Module

**File:** `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
    
    # Analytics
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.7))
    OUTLIER_THRESHOLD = float(os.getenv('OUTLIER_THRESHOLD', 3.0))
    
    # Paths
    UPLOAD_DIR = 'data/uploads'
    PROCESSED_DIR = 'data/processed'
    REPORTS_DIR = 'reports/generated'
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_chatbot_comprehensive.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_chatbot_comprehensive.py::TestChatbotFunctionality::test_basic_questions -v
```

### Test Structure

```python
# tests/test_example.py
import pytest
from src.module import Component

class TestComponent:
    """Test suite for Component"""
    
    @pytest.fixture
    def component(self):
        """Create component instance"""
        return Component()
    
    def test_feature(self, component):
        """Test specific feature"""
        result = component.do_something()
        assert result == expected
```

### Current Test Coverage

- **16 tests** in `test_chatbot_comprehensive.py`
- **100% pass rate**
- Coverage: Functionality, chart types, data types, performance
- Run time: ~5 seconds

### Adding New Tests

1. Create test file in `tests/`
2. Import component to test
3. Write test class with `Test` prefix
4. Write test methods with `test_` prefix
5. Use pytest fixtures for setup
6. Run tests to verify

---

## 🚢 Deployment

### Local Deployment

Already covered in [Setup and Installation](#setup-and-installation)

### Docker Deployment

```bash
# Build image
docker build -t ai-analytics-system .

# Run container
docker run -p 8501:8501 -p 8000:8000 ai-analytics-system

# With environment variables
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... ai-analytics-system
```

### Cloud Deployment

#### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)
# 2. SSH into instance
ssh -i key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# 3. Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# 4. Clone repository
git clone https://github.com/Web8080/AI_Business_Analytics_Chatbot.git
cd AI_Business_Analytics_Chatbot

# 5. Build and run
docker-compose up -d

# 6. Configure security group to allow ports 8501 and 8000
```

#### Heroku

```bash
# 1. Create Heroku app
heroku create ai-analytics-system

# 2. Add buildpacks
heroku buildpacks:set heroku/python

# 3. Deploy
git push heroku main

# 4. Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
```

#### Azure App Service

```bash
# 1. Create resource group
az group create --name ai-analytics --location eastus

# 2. Create app service plan
az appservice plan create --name analytics-plan --resource-group ai-analytics

# 3. Create web app
az webapp create --name ai-analytics-system --resource-group ai-analytics --plan analytics-plan

# 4. Deploy from GitHub
az webapp deployment source config --name ai-analytics-system --resource-group ai-analytics --repo-url https://github.com/Web8080/AI_Business_Analytics_Chatbot --branch main
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Write tests**
5. **Run tests locally**
   ```bash
   pytest tests/ -v
   ```
6. **Commit with clear messages**
   ```bash
   git commit -m "Add: Feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create Pull Request**

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings
- Max line length: 100

```python
def function_name(param1: str, param2: int) -> dict:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    pass
```

**Formatting:**
```bash
# Auto-format with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/
```

### Commit Message Format

```
Type: Brief description

Longer description if needed

- Change 1
- Change 2
```

**Types:**
- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Update existing feature
- `Refactor:` Code refactoring
- `Docs:` Documentation
- `Test:` Add/update tests
- `Style:` Code style changes

---

## 🔧 Troubleshooting

### Common Development Issues

#### Issue: Import errors

```bash
# Solution: Add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
```

#### Issue: OpenAI API errors

```python
# Solution: Check API key and handle errors
try:
    response = openai.ChatCompletion.create(...)
except openai.error.AuthenticationError:
    print("Invalid API key")
except openai.error.RateLimitError:
    print("Rate limit exceeded")
```

#### Issue: Streamlit not reloading

```bash
# Solution: Clear cache and restart
streamlit cache clear
streamlit run dashboard_openai.py
```

#### Issue: Docker build fails

```bash
# Solution: Clear Docker cache
docker system prune -a
docker build --no-cache -t ai-analytics-system .
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Streamlit debug
import streamlit as st
st.write("Debug info:", st.session_state)
```

### Performance Profiling

```python
# Profile code
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)
```

---

## 📚 Additional Resources

### Documentation
- [README.md](README.md) - Project overview
- [USER_MANUAL.md](USER_MANUAL.md) - User guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [NEXT_PHASES.md](NEXT_PHASES.md) - Development roadmap

### External Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Plotly Documentation](https://plotly.com/python/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)

---

## 📝 Version History

- **v1.0** (Phase 5.1) - OpenAI integration, comprehensive testing
- **v0.9** (Phase 4) - UI/UX enhancements, robust chatbot
- **v0.8** (Phase 3) - Advanced features implementation
- **v0.7** (Phase 2) - Conversational AI development
- **v0.6** (Phase 1) - Core system development
- **v0.5** - Initial analytics engine
- **v0.1** - Project inception

---

## 🙏 Acknowledgments

**Technologies:**
- OpenAI for GPT-4
- Streamlit for amazing dashboard framework
- Plotly for beautiful visualizations
- FastAPI for modern API framework
- All open-source contributors

---

## 📞 Support

**For technical issues:**
1. Check this guide
2. Review [README.md](README.md)
3. Search GitHub issues
4. Create new issue with details

**For feature requests:**
- Open GitHub issue with `[Feature Request]` tag

---

**Developer Guide Version:** 1.0  
**Last Updated:** October 18, 2025  
**System Version:** Phase 5.1

---

**Happy Coding!** 💻🚀

