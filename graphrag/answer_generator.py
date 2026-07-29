import re

def generate_answer(question: str, context: dict) -> dict:
    chunks = context["top_chunks"]
    if not chunks or max((c.get("relevance_score", 0) for c in chunks), default=0) < 0.02:
        return {"question": question, "answer": "The available evidence is insufficient to answer this question.",
                "citations": [], "related_entities": context["related_entities"], "graph_evidence": [],
                "confidence": "low", "unsupported_claim_risk": "high",
                "uncertainty_note": "No sufficiently relevant cited chunk was found."}
    terms, candidates = set(re.findall(r"[a-z0-9]+", question.lower())), []
    controlled = []
    if "control" in question.lower():
        for relationship in context["relationships_used"]:
            if relationship["relationship_type"] == "controlled_by" and relationship["source_entity"].lower() in question.lower():
                controlled.append(relationship)
    if controlled:
        targets = list(dict.fromkeys(r["target_entity"] for r in controlled))
        risk = controlled[0]["source_entity"]
        citations = list(dict.fromkeys(r["evidence_chunk_id"] for r in controlled))
        joined = ", ".join(targets[:-1]) + (" and " if len(targets) > 1 else "") + targets[-1]
        graph = [{"source": r["source_entity"], "relationship": r["relationship_type"],
                  "target": r["target_entity"], "citation": r["evidence_chunk_id"]} for r in controlled]
        return {"question": question, "answer": f"The cited documents link {risk} to these controls: {joined}. " +
                " ".join(f"[{citation}]" for citation in citations), "citations": citations,
                "related_entities": context["related_entities"], "graph_evidence": graph,
                "confidence": "high" if len(targets) > 1 else "medium", "unsupported_claim_risk": "low",
                "uncertainty_note": "Limited to controls explicitly connected in the cited synthetic knowledge graph."}
    for chunk in chunks[:5]:
        for sentence in re.split(r"(?<=[.!?])\s+", chunk["chunk_text"]):
            overlap = len(terms & set(re.findall(r"[a-z0-9]+", sentence.lower())))
            if overlap: candidates.append((overlap, sentence.strip(), chunk["chunk_id"]))
    candidates.sort(reverse=True)
    selected = []
    for _, sentence, citation in candidates:
        if sentence not in [s for s, _ in selected]: selected.append((sentence, citation))
        if len(selected) == 3: break
    citations = [citation for _, citation in selected]
    graph = [{"source": r["source_entity"], "relationship": r["relationship_type"],
              "target": r["target_entity"], "citation": r["evidence_chunk_id"]}
             for r in context["relationships_used"][:8]]
    return {"question": question, "answer": " ".join(f"{s} [{c}]" for s, c in selected),
            "citations": citations, "related_entities": context["related_entities"], "graph_evidence": graph,
            "confidence": "high" if len(citations) >= 2 and graph else "medium",
            "unsupported_claim_risk": "low", "uncertainty_note": "Limited to the cited synthetic knowledge base."}
