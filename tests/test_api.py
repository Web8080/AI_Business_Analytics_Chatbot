"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_datasets():
    """Test listing datasets"""
    response = client.get("/datasets")
    assert response.status_code == 200
    assert "datasets" in response.json()
    assert "total" in response.json()


# Add more tests as needed

