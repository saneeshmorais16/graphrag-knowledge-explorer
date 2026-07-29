from graphrag.retrieval import hybrid_retrieve

def test_hybrid_retrieval_includes_graph_context(knowledge):
    result=hybrid_retrieve("controls for Prompt Injection Risk",**knowledge)
    assert result["top_chunks"]
    assert "Citation Requirement" in result["related_entities"]
    assert result["relationships_used"]
