from pathlib import Path
from .chunking import chunk_markdown
from .entity_extraction import extract_entities
from .relationship_extraction import extract_relationships

def ingest_directory(path: str | Path) -> dict:
    chunks, entities, relationships = [], [], []
    for file in sorted(Path(path).glob("*.md")):
        for chunk in chunk_markdown(file.read_text(encoding="utf-8"), file.name):
            chunks.append(chunk)
            found = extract_entities(chunk["chunk_text"], chunk["chunk_id"])
            entities.extend(found)
            relationships.extend(extract_relationships(chunk["chunk_text"], found, chunk["chunk_id"]))
    unique = {e["name"]: e for e in entities}
    return {"chunks": chunks, "entities": list(unique.values()), "relationships": relationships}
