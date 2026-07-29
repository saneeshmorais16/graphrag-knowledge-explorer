import re

PATTERNS = [
    (r"(?P<s>[^.]+?) uses (?P<t>[^.]+?)(?:\.|$)", "uses"),
    (r"(?P<s>[^.]+?) has (?:the )?(?P<t>[^.]+?)(?:\.|$)", "has_risk"),
    (r"(?P<s>[^.]+?) is controlled by (?P<t>[^.]+?)(?:\.|$)", "controlled_by"),
    (r"(?P<s>[^.]+?) owns (?P<t>[^.]+?)(?:\.|$)", "owns"),
    (r"(?P<s>[^.]+?) requires (?P<t>[^.]+?)(?:\.|$)", "requires"),
    (r"(?P<s>[^.]+?) affects (?P<t>[^.]+?)(?:\.|$)", "affects"),
    (r"(?P<s>[^.]+?) measures (?P<t>[^.]+?)(?:\.|$)", "measures"),
]

def extract_relationships(text: str, entities: list[dict], chunk_id: str = "") -> list[dict]:
    names, relationships, seen = [e["name"] for e in entities], [], set()
    for pattern, rel_type in PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            source = next((n for n in names if n.lower() in match.group("s").lower()), None)
            target = next((n for n in names if n.lower() in match.group("t").lower()), None)
            key = (source, rel_type, target)
            if source and target and source != target and key not in seen:
                seen.add(key)
                relationships.append({"source_entity": source, "relationship_type": rel_type,
                    "target_entity": target, "evidence_chunk_id": chunk_id, "confidence_score": 0.9})
    return relationships
