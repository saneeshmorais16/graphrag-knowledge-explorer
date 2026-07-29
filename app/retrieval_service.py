from graphrag.answer_generator import generate_answer
from graphrag.retrieval import hybrid_retrieve

class RetrievalService:
    def __init__(self, data: dict):
        self.data = data

    def retrieve(self, question: str, top_k: int = 5) -> dict:
        return hybrid_retrieve(question, **self.data, top_k=top_k)

    def ask(self, question: str, top_k: int = 5) -> dict:
        return generate_answer(question, self.retrieve(question, top_k))
