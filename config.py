"""
Configuration management for the AI Analytics Intelligence System
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI (optional; omit to use Ollama)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # Ollama (used when OPENAI_API_KEY is not set; works in production if Ollama runs on a server)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    api_debug: bool = True
    
    # Database Configuration
    database_url: str = "sqlite:///./analytics.db"
    
    # Email Configuration (for report distribution)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    
    # Analytics Configuration
    confidence_threshold: float = 0.7
    max_forecast_periods: int = 12
    outlier_detection_threshold: float = 3.0
    
    # File Upload Configuration
    max_upload_size_mb: int = 50
    allowed_file_types: str = "pdf,csv,xlsx"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/analytics.log"
    
    # Report Generation
    report_output_dir: str = "reports/generated"
    report_company_name: str = "Your Company"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


# Create necessary directories
def setup_directories():
    """Create required directories if they don't exist"""
    directories = [
        "data/uploads",
        "data/processed",
        "data/temp",
        "reports/generated",
        "logs",
        "models/trained"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

