# tests/test_urls.py
from fastapi.testclient import TestClient
from main import app
from core.config import settings

client = TestClient(app)

def test_create_shorten_url():
    request_data = {
        "original_url": "http://example.com",
        "visibility": "public"
    }

    response = client.post("/url/create", json=request_data)

    assert response.status_code == 200
    response_data = response.json()
    assert "short_url" in response_data
    assert response_data["short_url"].startswith(f"{settings.service_url}/")
