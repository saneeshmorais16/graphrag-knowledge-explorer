import networkx as nx

def neighbours(graph: nx.MultiDiGraph, entity: str) -> list[dict]:
    if entity not in graph: return []
    outgoing = [{"entity": t, "direction": "outgoing", **d} for _, t, d in graph.edges(entity, data=True)]
    incoming = [{"entity": s, "direction": "incoming", **d} for s, _, d in graph.in_edges(entity, data=True)]
    return outgoing + incoming

def find_path(graph: nx.MultiDiGraph, source: str, target: str) -> list[str]:
    if source not in graph or target not in graph: return []
    try: return nx.shortest_path(graph.to_undirected(), source, target)
    except nx.NetworkXNoPath: return []
