import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
 chunk_id TEXT PRIMARY KEY, document_name TEXT, section_title TEXT, chunk_text TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS entities (
 name TEXT PRIMARY KEY, entity_type TEXT, evidence_chunk_id TEXT);
CREATE TABLE IF NOT EXISTS relationships (
 id INTEGER PRIMARY KEY AUTOINCREMENT, source_entity TEXT, relationship_type TEXT,
 target_entity TEXT, evidence_chunk_id TEXT, confidence_score REAL);
"""

def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
