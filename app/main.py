from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .graph_service import GraphService
from .schemas import AskRequest, EvaluationRequest, RetrieveRequest
from .storage import Storage
from .retrieval_service import RetrievalService
from graphrag.evaluation import evaluate_answer
from graphrag.ingestion import ingest_directory
from graphrag.report import summary

ROOT = Path(__file__).resolve().parents[1]
storage = Storage(ROOT / "graphrag_knowledge_explorer.db")
app = FastAPI(title="GraphRAG Knowledge Explorer", version="1.0.0",
              description="Local-first GraphRAG over safe synthetic documents.")
app.mount("/static", StaticFiles(directory=ROOT / "app" / "static"), name="static")

def current() -> dict:
    return storage.all()

@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(ROOT / "app" / "static" / "index.html")

@app.get("/health")
def health():
    return {"status": "healthy", "mode": "local-extractive", "llm_enabled": False}

@app.post("/documents/ingest")
def ingest_documents():
    data = ingest_directory(ROOT / "data" / "sample_docs")
    storage.replace_all(data)
    return {"status": "ingested", **summary(data)}

@app.get("/documents")
def documents():
    data = current()
    return {"documents": sorted({c["document_name"] for c in data["chunks"]}), "chunks": data["chunks"]}

@app.get("/entities")
def entities():
    return {"entities": current()["entities"]}

@app.get("/relationships")
def relationships():
    return {"relationships": current()["relationships"]}

@app.get("/graph/neighbours/{entity_name}")
def graph_neighbours(entity_name: str):
    rows = GraphService(current()).neighbours(entity_name)
    if not rows: raise HTTPException(404, "Entity not found or has no relationships")
    return {"entity": entity_name, "neighbours": rows}

@app.get("/graph/path")
def graph_path(source: str = Query(...), target: str = Query(...)):
    path = GraphService(current()).path(source, target)
    if not path: raise HTTPException(404, "No path found")
    return {"source": source, "target": target, "path": path}

@app.post("/retrieve")
def retrieve(payload: RetrieveRequest):
    return RetrievalService(current()).retrieve(payload.question, payload.top_k)

@app.post("/ask")
def ask(payload: AskRequest):
    return RetrievalService(current()).ask(payload.question, payload.top_k)

@app.post("/evaluate")
def evaluate(payload: EvaluationRequest):
    questions = payload.questions or [
        "Which controls reduce Prompt Injection Risk for the RAG Support Assistant?",
        "Who owns the RAG Support Assistant?", "What is the office menu?"
    ]
    service = RetrievalService(current())
    results = [{"question": q, **evaluate_answer(service.ask(q))} for q in questions]
    return {"evaluations": results, "average": round(sum(r["overall_score"] for r in results) / len(results), 2)}

@app.get("/summary")
def get_summary():
    data = current()
    return {**summary(data), "graph": GraphService(data).statistics(), "runtime_mode": "local-extractive"}
