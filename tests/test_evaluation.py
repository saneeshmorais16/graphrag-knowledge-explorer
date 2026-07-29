from graphrag.evaluation import evaluate_answer

def test_insufficient_evidence_handling_scores():
    result={"answer":"Evidence is insufficient.","citations":[],"related_entities":[],
            "graph_evidence":[],"unsupported_claim_risk":"high"}
    score=evaluate_answer(result)
    assert score["scores"]["insufficient_evidence_handling"]==1.0
    assert score["scores"]["citation_presence"]==1.0
