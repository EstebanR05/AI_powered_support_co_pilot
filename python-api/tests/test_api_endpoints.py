import pytest
from fastapi.testclient import TestClient
import os

# Set test environment before importing app
os.environ["ENVIRONMENT"] = "test"

from main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"
    assert "endpoints" in data

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "timestamp" in data

def test_get_tickets_endpoint(client):
    """Test get tickets endpoint"""
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Should return a list of tickets