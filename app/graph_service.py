from graphrag.graph_builder import build_graph
from graphrag.graph_search import find_path, neighbours

class GraphService:
    def __init__(self, data: dict):
        self.graph = build_graph(data["entities"], data["relationships"])

    def neighbours(self, entity: str) -> list[dict]:
        return neighbours(self.graph, entity)

    def path(self, source: str, target: str) -> list[str]:
        return find_path(self.graph, source, target)

    def statistics(self) -> dict:
        return {"nodes": self.graph.number_of_nodes(), "edges": self.graph.number_of_edges(),
                "density": round(float(__import__("networkx").density(self.graph)), 4)}
