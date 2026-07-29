from pathlib import Path
import pytest
from graphrag.ingestion import ingest_directory

@pytest.fixture
def knowledge():
    return ingest_directory(Path(__file__).parents[1] / "data" / "sample_docs")
