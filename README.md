# GraphRAG Knowledge Explorer

**A local-first GraphRAG workbench that turns synthetic documents into a searchable evidence graph and grounded, cited answers.**

GraphRAG matters because ordinary RAG ranks isolated chunks. Questions about ownership, dependencies, controls, risks, or multi-document chains need structure: entities connect evidence that lexical retrieval alone can miss.

## Problem statement

Knowledge-heavy questions often depend on relationships distributed across documents. This project demonstrates an inspectable pipeline that extracts named concepts and typed edges, expands retrieval across the resulting graph, and refuses to improvise when evidence is weak. It is a portfolio demonstration—not a production or commercial deployment.

## Architecture

```text
Documents
   |
   v
Chunking
   |
   v
Entity extraction -----> Relationship extraction
   |                              |
   v                              v
Knowledge graph <------ Evidence chunks
   |
   v
Hybrid retrieval
   |
   v
Grounded GraphRAG answer + citations
   |
   v
Evaluation scorecard
```

FastAPI provides the API and static dashboard. SQLite persists chunks, entities, edges, and provenance locally. NetworkX serves neighbour, path, and graph-statistic operations.

## Core features

- Six safe, fictional Markdown documents with realistic policies, workflows, systems, risks, controls, tools, metrics, and an invented incident
- Heading-aware chunking with stable `document#chunk-n` citation identifiers
- Offline entity and relationship extraction
- Evidence-backed NetworkX graph with neighbours and shortest paths
- TF-IDF retrieval plus relationship-based graph expansion
- Local extractive answers, inline citations, confidence, and uncertainty
- Explicit insufficient-evidence behavior
- Evaluation across citation presence, relevance, entity coverage, relationship correctness, unsupported claims, and abstention
- FastAPI, SQLite, responsive dashboard, pytest, and GitHub Actions

## How the pipeline works

### Document ingestion

`POST /documents/ingest` reads only `data/sample_docs/*.md`. Headings become section metadata; paragraphs are grouped into bounded chunks and assigned provenance fields: chunk ID, document, section, text, and UTC creation time.

### Entity extraction

A transparent catalogue and case-insensitive boundary matching identify systems, teams, risks, controls, policies, tools, metrics, incidents, and workflows. It needs no model download or paid API.

### Relationship extraction

Auditable sentence patterns recognise `uses`, `has_risk`, `controlled_by`, `owns`, `requires`, `affects`, and `measures`. Every edge retains its evidence chunk and confidence score.

### Hybrid retrieval

TF-IDF ranks chunks against the question. Entity mentions then seed graph expansion; connected edges contribute their evidence chunks. The response explains this process and exposes the chunks, entities, relationships, and citation IDs used.

### GraphRAG answer generation

The default generator selects relevant sentences from retrieved evidence and appends citations. It reports graph evidence separately. If no sufficiently relevant chunk exists, it says the evidence is insufficient. No paid LLM is required, and external LLM use is disabled by default.

### Evaluation strategy

The evaluation suite checks citation presence, context relevance, expected-entity coverage, relationship support, unsupported-claim risk, and correct abstention. Sample questions include both answerable relationship questions and an intentionally unsupported question.

## Example

**Question:** Which controls reduce prompt injection risk for the RAG Support Assistant?

**Representative retrieved chunks:**

- `rag_evaluation_notes#chunk-2`: links the risk to three controls.
- `ai_governance_policy#chunk-2`: supplies policy ownership and control evidence.
- `support_triage_workflow#chunk-2`: supplies workflow and restricted-access evidence.

**Graph evidence:**

```text
Prompt Injection Risk --controlled_by--> Citation Requirement
Prompt Injection Risk --controlled_by--> Human Review Required
Prompt Injection Risk --controlled_by--> Restricted Tool Access
RAG Support Assistant --has_risk--> Prompt Injection Risk
```

**Representative final output:**

```json
{
  "question": "Which controls reduce prompt injection risk for the RAG Support Assistant?",
  "answer": "The cited documents link Prompt Injection Risk to three controls: Citation Requirement, Human Review Required and Restricted Tool Access.",
  "related_entities": [
    "Prompt Injection Risk",
    "Citation Requirement",
    "Human Review Required",
    "Restricted Tool Access",
    "RAG Support Assistant"
  ],
  "graph_evidence": [
    {
      "source": "Prompt Injection Risk",
      "relationship": "controlled_by",
      "target": "Citation Requirement",
      "citation": "rag_evaluation_notes#chunk-2"
    }
  ],
  "confidence": "medium",
  "unsupported_claim_risk": "low"
}
```

Runtime wording is extractive and may differ while preserving cited support.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Runtime and mode status |
| POST | `/documents/ingest` | Rebuild the synthetic document index |
| GET | `/documents` | List documents and chunks |
| GET | `/entities` | List typed entities |
| GET | `/relationships` | List evidence-backed edges |
| GET | `/graph/neighbours/{entity_name}` | Inspect connected entities |
| GET | `/graph/path?source=...&target=...` | Find an undirected shortest path |
| POST | `/retrieve` | Return hybrid retrieval context |
| POST | `/ask` | Return a grounded answer |
| POST | `/evaluate` | Run sample or supplied questions |
| GET | `/summary` | Dashboard and graph metrics |

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Setup and local run

```bash
python -m venv .venv
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Then:

```bash
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:8000`. Alternatively run `uvicorn app.main:app --reload`.

## Tests

```bash
pytest
```

The suite covers chunking, entity and relationship extraction, neighbour lookup, path finding, hybrid retrieval, citations, unsupported claims, evaluation, health, and asking through the API.

## Screenshots and demo

> Add an updated dashboard screenshot or short screen recording here after running the local application. No generated screenshot is committed as factual proof of a deployed service.

## Privacy and safety

- Every bundled document is invented for this demonstration.
- No real company data, customer data, emails, private documents, credentials, logs, or personal records are included.
- `.env`, local databases, logs, uploads, secret directories, and private/real-data paths are ignored.
- External LLM use is disabled by default and the implementation does not require a key.
- The repository makes no claims of production use, clients, enterprise deployment, or commercial operation.

## Limitations

Rule-based extraction is predictable but narrower than learned entity and relation models. TF-IDF is lexical rather than deeply semantic. The answer generator favors auditability over conversational prose. SQLite and an in-process NetworkX graph are appropriate for a local demonstration rather than large-scale concurrent use.

## Future improvements

- Optional local sentence-transformer embeddings with graceful fallback
- Coreference resolution and ontology-driven extraction
- Community detection and graph summaries
- Temporal and weighted path reasoning
- Retrieval ablations and a larger synthetic benchmark
- Local open-weight LLM adapter behind an explicit feature flag
- Interactive force-directed graph visualisation and exportable evaluation reports

## License and use

This educational portfolio project contains synthetic content. Review the safety boundaries in [PROJECT_STATUS.md](PROJECT_STATUS.md) before adapting it to any other dataset.
