from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_query_validation():
    # Prompt too short (< 3 chars)
    res = client.post("/api/v1/query", json={"prompt": "hi"})
    assert res.status_code == 422

def test_query_success():
    res = client.post("/api/v1/query", json={"prompt": "What is DocuMind?"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert len(data["citations"]) > 0
    assert data["latency_ms"] > 0