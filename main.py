"""
Main entry point for the AI Analytics Intelligence System
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.api.main import app
import uvicorn
from config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print("=" * 70)
    print("🤖 AI Analytics Intelligence System")
    print("=" * 70)
    print(f"Starting server on http://{settings.api_host}:{settings.api_port}")
    print(f"API Documentation: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"Alternative Docs: http://{settings.api_host}:{settings.api_port}/redoc")
    print("=" * 70)
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )

