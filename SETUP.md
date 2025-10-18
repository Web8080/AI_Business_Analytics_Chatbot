# Setup Instructions

## Environment Configuration

The system uses OpenAI's GPT-4 and LangChain for conversational AI. You need to configure your API keys:

### 1. Create Environment File

Copy the `env.example` to create your `.env` file:

```bash
cp env.example .env
```

### 2. Add Your OpenAI API Key

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

Get your API key from: https://platform.openai.com/api-keys

### 3. OpenAI Integration

The system integrates OpenAI and LangChain in these modules:

- **`config.py`** - Loads OpenAI API key from environment
- **`src/conversational/agent.py`** - LangChain agent with OpenAI GPT-4
- **`src/api/main.py`** - Initializes conversational agent with API key

### 4. How It Works

```python
# In config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str  # Required
    openai_model: str = "gpt-4-turbo-preview"
    
    class Config:
        env_file = ".env"

# In src/conversational/agent.py
from langchain_openai import ChatOpenAI

class ConversationalAgent:
    def __init__(self, api_key: str, model: str):
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.1
        )

# In src/api/main.py
from config import get_settings

settings = get_settings()
conversational_agent = ConversationalAgent(
    api_key=settings.openai_api_key,
    model=settings.openai_model
)
```

### 5. Models Folder

The `models/trained/` folder is intentionally empty. It's where trained ML models will be saved when you:

- Train XGBoost models for prediction
- Train Prophet models for forecasting
- Save custom trained models

Models are generated at runtime and can be persisted here for reuse.

### 6. Security Note

**IMPORTANT:** Never commit your `.env` file to Git! It contains sensitive API keys.

The `.env` file is in `.gitignore` for security. Only `env.example` (without real keys) is tracked in Git.

### 7. Quick Start

```bash
# 1. Create .env file
cp env.example .env

# 2. Edit .env and add your OpenAI API key
nano .env  # or use any text editor

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the system
python main.py
```

### 8. Verify Configuration

You can test if your configuration is working:

```python
from config import get_settings

settings = get_settings()
print(f"OpenAI Key configured: {settings.openai_api_key[:8]}...")
print(f"Model: {settings.openai_model}")
```

## Additional Configuration

### Email Notifications (Optional)

To enable automated report email distribution:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Analytics Parameters

Fine-tune analytics behavior:

```env
CONFIDENCE_THRESHOLD=0.7          # Minimum confidence for predictions
MAX_FORECAST_PERIODS=12           # Maximum forecast horizon
OUTLIER_DETECTION_THRESHOLD=3.0   # Z-score threshold for outliers
```

## Troubleshooting

**"OpenAI API key not found"**
- Make sure you created `.env` file from `env.example`
- Verify your API key is correctly set in `.env`
- Check that `.env` is in the project root directory

**"Module 'langchain_openai' not found"**
- Run `pip install -r requirements.txt`
- Make sure virtual environment is activated

**"Rate limit exceeded"**
- You've hit OpenAI API rate limits
- Wait a few moments or upgrade your OpenAI plan
- Check your usage at https://platform.openai.com/usage

