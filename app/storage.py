from pathlib import Path
from .database import connect

class Storage:
    def __init__(self, path: str | Path):
        self.path = path

    def replace_all(self, data: dict) -> None:
        with connect(self.path) as conn:
            conn.execute("DELETE FROM relationships"); conn.execute("DELETE FROM entities"); conn.execute("DELETE FROM chunks")
            conn.executemany("INSERT INTO chunks VALUES (:chunk_id,:document_name,:section_title,:chunk_text,:created_at)", data["chunks"])
            conn.executemany("INSERT INTO entities VALUES (:name,:entity_type,:evidence_chunk_id)", data["entities"])
            conn.executemany("""INSERT INTO relationships
                (source_entity,relationship_type,target_entity,evidence_chunk_id,confidence_score)
                VALUES (:source_entity,:relationship_type,:target_entity,:evidence_chunk_id,:confidence_score)""",
                data["relationships"])

    def all(self) -> dict:
        with connect(self.path) as conn:
            chunks = [dict(r) for r in conn.execute("SELECT * FROM chunks ORDER BY document_name, chunk_id")]
            entities = [dict(r) for r in conn.execute("SELECT * FROM entities ORDER BY name")]
            relationships = [dict(r) for r in conn.execute("""SELECT source_entity,relationship_type,target_entity,
                evidence_chunk_id,confidence_score FROM relationships ORDER BY source_entity,target_entity""")]
        return {"chunks": chunks, "entities": entities, "relationships": relationships}
