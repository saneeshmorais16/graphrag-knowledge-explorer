from graphrag.answer_generator import generate_answer
from graphrag.retrieval import hybrid_retrieve

def test_answer_has_citations(knowledge):
    q="Which controls reduce Prompt Injection Risk?"
    answer=generate_answer(q,hybrid_retrieve(q,**knowledge))
    assert answer["citations"]
    assert all(c in answer["answer"] for c in answer["citations"])

def test_unsupported_question_is_rejected(knowledge):
    q="What is the office menu?"
    answer=generate_answer(q,hybrid_retrieve(q,**knowledge))
    assert "insufficient" in answer["answer"].lower()
    assert answer["citations"]==[]
