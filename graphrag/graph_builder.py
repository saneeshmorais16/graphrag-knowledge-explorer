import networkx as nx

def build_graph(entities: list[dict], relationships: list[dict]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for entity in entities:
        graph.add_node(entity["name"], entity_type=entity["entity_type"])
    for rel in relationships:
        graph.add_edge(rel["source_entity"], rel["target_entity"], **rel)
    return graph
