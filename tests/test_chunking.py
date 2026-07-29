from graphrag.chunking import chunk_markdown

def test_chunking_preserves_provenance():
    chunks=chunk_markdown("# One\n\nAlpha.\n\n# Two\n\nBeta.", "demo.md")
    assert len(chunks)==2
    assert chunks[0]["chunk_id"]=="demo#chunk-1"
    assert chunks[1]["section_title"]=="Two"
