import re
from datetime import datetime, timezone
from pathlib import Path


def chunk_markdown(text: str, document_name: str, max_chars: int = 900) -> list[dict]:
    """Split Markdown by heading and bounded paragraph while retaining provenance."""
    sections, title, body = [], "Introduction", []
    for line in text.splitlines():
        if line.startswith("#"):
            if body:
                sections.append((title, "\n".join(body).strip()))
            title, body = line.lstrip("# ").strip(), []
        else:
            body.append(line)
    if body:
        sections.append((title, "\n".join(body).strip()))
    raw = []
    for section, content in sections:
        current = ""
        for paragraph in [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]:
            if current and len(current) + len(paragraph) + 2 > max_chars:
                raw.append((section, current))
                current = paragraph
            else:
                current = f"{current}\n\n{paragraph}".strip()
        if current:
            raw.append((section, current))
    now, stem = datetime.now(timezone.utc).isoformat(), Path(document_name).stem
    return [{"chunk_id": f"{stem}#chunk-{i}", "document_name": document_name,
             "section_title": section, "chunk_text": content, "created_at": now}
            for i, (section, content) in enumerate(raw, 1)]
