from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health_endpoint():
    r=client.get("/health")
    assert r.status_code==200 and r.json()["llm_enabled"] is False

def test_ask_endpoint():
    assert client.post("/documents/ingest").status_code==200
    r=client.post("/ask",json={"question":"Which controls reduce Prompt Injection Risk?"})
    assert r.status_code==200
    assert r.json()["citations"]
