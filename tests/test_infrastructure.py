import pytest
import os
import requests
from dotenv import load_dotenv

# Load env
load_dotenv()

# Gemini Server URL
GEMINI_URL = "http://127.0.0.1:8000/v1/models"


def test_gemini_server_health():
    """Check if local Gemini-FastAPI server is running and responding."""
    try:
        response = requests.get(GEMINI_URL, timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        # Check if expected models are present
        model_ids = [m["id"] for m in data["data"]]
        assert "gemini-3.0-flash" in model_ids
    except requests.exceptions.ConnectionError:
        pytest.fail("Gemini Server is DOWN! (Connection refused)")
