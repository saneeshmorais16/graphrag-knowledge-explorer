from graphrag.entity_extraction import extract_entities

def test_extracts_typed_entities():
    rows=extract_entities("RAG Support Assistant has Prompt Injection Risk.", "x#chunk-1")
    assert {(r["name"],r["entity_type"]) for r in rows} >= {
        ("RAG Support Assistant","system"),("Prompt Injection Risk","risk")}
