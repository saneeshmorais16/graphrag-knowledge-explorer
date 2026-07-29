# Project Status

## Build status

Feature-complete portfolio demonstration. The default runtime is fully local and deterministic.

## Completed features

- Synthetic Markdown ingestion, heading-aware chunking, and SQLite persistence
- Typed rule-based entity and relationship extraction
- NetworkX graph construction, neighbour lookup, shortest paths, and statistics
- TF-IDF chunk ranking with entity-driven graph expansion
- Extractive grounded answers with chunk citations and uncertainty notes
- Evaluation scorecard, FastAPI API, and responsive dark dashboard
- Automated pytest suite and GitHub Actions workflow

## Testing status

The local test result and exact count are recorded in the initial repository commit report. CI runs the same suite on Python 3.12.

## Known limitations

- Rules and a fixed entity catalogue are intentionally simpler than learned NER or relation models.
- TF-IDF captures lexical similarity, not deep semantic equivalence.
- Extractive answers prioritise traceability over fluency.
- SQLite and the in-process graph suit a local demonstration, not a distributed workload.
- Optional embedding and LLM adapters are future work; paid APIs are not enabled.

## Safety boundaries

Only the six invented Markdown files under `data/sample_docs` are in scope. The project makes no production, client, deployment, or commercial-usage claim. It must not ingest real company, customer, email, credential, or personal data.

## Files excluded from Git

Environment files, SQLite databases, logs, PDFs, caches, virtual environments, build artifacts, uploads, secrets, credentials, generated outputs, application packets, private documents, and real company/customer/knowledge-base directories.

## Checks required before making public

- Confirm all tests pass.
- Inspect every tracked file and synthetic document.
- Scan tracked content for credentials, tokens, private data, and production/client claims.
- Verify ignored sensitive paths with `git check-ignore`.
- Confirm the optional LLM mode is disabled and no key is required.
- Review repository visibility only after all checks pass.
