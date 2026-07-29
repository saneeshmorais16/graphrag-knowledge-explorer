import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def hybrid_retrieve(question: str, chunks: list[dict], entities: list[dict], relationships: list[dict], top_k: int = 5) -> dict:
    if not chunks:
        return {"top_chunks": [], "related_entities": [], "relationships_used": [], "citation_ids": [],
                "retrieval_explanation": "No documents have been ingested."}
    matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(
        [c["chunk_text"] for c in chunks] + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    top = [{**chunks[i], "relevance_score": round(float(scores[i]), 4)} for i in ranked if scores[i] > 0]
    question_lower = question.lower()
    q_terms = set(re.findall(r"[a-z0-9]+", question_lower))
    matched = {e["name"] for e in entities if e["name"].lower() in question_lower}
    if not matched:
        matched = {e["name"] for e in entities
                   if len(set(re.findall(r"[a-z0-9]+", e["name"].lower())) & q_terms) >= 2}
    used = [r for r in relationships if r["source_entity"] in matched or r["target_entity"] in matched]
    expanded = matched | {r["source_entity"] for r in used} | {r["target_entity"] for r in used}
    evidence_ids = {r["evidence_chunk_id"] for r in used}
    existing = {c["chunk_id"] for c in top}
    top += [{**c, "relevance_score": 0.0, "graph_expanded": True}
            for c in chunks if c["chunk_id"] in evidence_ids and c["chunk_id"] not in existing]
    return {"top_chunks": top, "related_entities": sorted(expanded), "relationships_used": used,
            "citation_ids": [c["chunk_id"] for c in top],
            "retrieval_explanation": "TF-IDF ranked lexical evidence; matched entities expanded graph-linked evidence."}
