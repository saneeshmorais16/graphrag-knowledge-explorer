from graphrag.graph_builder import build_graph
from graphrag.graph_search import find_path, neighbours

def test_neighbours_and_path(knowledge):
    graph=build_graph(knowledge["entities"],knowledge["relationships"])
    connected=neighbours(graph,"Prompt Injection Risk")
    assert any(x["entity"]=="Citation Requirement" for x in connected)
    assert find_path(graph,"Prompt Injection Risk","RAG Support Assistant")
