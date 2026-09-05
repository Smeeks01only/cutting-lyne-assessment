import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_chat_validation_empty_message():
    # Pydantic should catch the empty string since min_length=1
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422

def test_chat_validation_missing_field():
    response = client.post("/api/chat", json={"text": "Hello"})
    assert response.status_code == 422

def test_chat_valid_tracking_request():
    response = client.post("/api/chat", json={"message": "Where is my cargo?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "SHIPMENT_TRACKING"
    assert "tracking number" in data["answer"].lower()

def test_chat_valid_knowledge_request():
    response = client.post("/api/chat", json={"message": "What duties do I pay?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "CUSTOMS_DUTIES"
    assert "duties" in data["answer"].lower()
