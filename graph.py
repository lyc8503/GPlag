import networkx as nx


def count_nodes_and_edges(gs):
    nodes = 0
    edges = 0

    for g in gs:
        nodes += len(g.nodes)
        edges += len(g.edges)
    
    return nodes, edges

