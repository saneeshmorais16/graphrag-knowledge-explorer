def evaluate_answer(result: dict, expected_entities: list[str] | None = None) -> dict:
    expected, answer = set(expected_entities or []), result.get("answer", "")
    citations, related = result.get("citations", []), set(result.get("related_entities", []))
    insufficient = "insufficient" in answer.lower()
    scores = {
        "citation_presence": 1.0 if citations or insufficient else 0.0,
        "context_relevance": 0.9 if citations else (1.0 if insufficient else 0.0),
        "entity_coverage": round(len(related & expected) / max(len(expected), 1), 2),
        "relationship_correctness": 1.0 if result.get("graph_evidence") else (0.8 if insufficient else 0.0),
        "unsupported_claim_risk": 1.0 if result.get("unsupported_claim_risk") == "low" or insufficient else 0.0,
        "insufficient_evidence_handling": 1.0 if (not insufficient or not citations) else 0.0,
    }
    return {"scores": scores, "overall_score": round(sum(scores.values()) / len(scores), 2)}
