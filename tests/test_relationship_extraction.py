from graphrag.entity_extraction import extract_entities
from graphrag.relationship_extraction import extract_relationships

def test_extracts_evidenced_relationship():
    text="Prompt Injection Risk is controlled by Citation Requirement."
    rows=extract_relationships(text,extract_entities(text), "notes#chunk-3")
    assert rows[0]["relationship_type"]=="controlled_by"
    assert rows[0]["evidence_chunk_id"]=="notes#chunk-3"
