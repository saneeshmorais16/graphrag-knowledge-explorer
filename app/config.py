import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///graphrag_knowledge_explorer.db")
    llm_enabled: bool = os.getenv("LLM_ENABLED", "false").lower() == "true"

settings = Settings()
