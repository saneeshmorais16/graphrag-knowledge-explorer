import re

ENTITY_CATALOG = {
    "RAG Support Assistant": "system", "FastAPI Inference API": "system",
    "Human Review Team": "team", "AI Governance Council": "team", "Incident Response Team": "team",
    "Prompt Injection Risk": "risk", "Unsupported Claim Risk": "risk", "Privacy Leakage Risk": "risk",
    "Citation Requirement": "control", "Human Review Required": "control",
    "Restricted Tool Access": "control", "Data Privacy Control": "control", "Rollback Control": "control",
    "AI Governance Policy": "policy", "Customer Data Privacy Policy": "policy",
    "MLflow": "tool", "NetworkX": "tool", "SQLite": "tool", "TF-IDF": "tool",
    "Citation Presence": "metric", "Context Relevance": "metric", "Entity Coverage": "metric",
    "Unsupported Claim Rate": "metric", "Support Triage Workflow": "workflow",
    "Incident Response Process": "workflow", "Synthetic Incident 17": "incident",
}

def extract_entities(text: str, chunk_id: str = "") -> list[dict]:
    return [{"name": name, "entity_type": kind, "evidence_chunk_id": chunk_id}
            for name, kind in ENTITY_CATALOG.items()
            if re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE)]
