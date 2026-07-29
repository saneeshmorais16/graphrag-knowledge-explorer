from pydantic import BaseModel, Field

class RetrieveRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)

class AskRequest(RetrieveRequest):
    pass

class EvaluationRequest(BaseModel):
    questions: list[str] | None = None
