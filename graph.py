import networkx as nx

from types import MethodType

def count_nodes_and_edges(gs):
    nodes = 0
    edges = 0

    for g in gs:
        nodes += len(g.nodes)
        edges += len(g.edges)
    
    return nodes, edges

def match_pair(g1, g2):
    # Method 1: Edit distance
    # print(nx.graph_edit_distance(g1, g2))

    # Method 2: Maximum common subgraph
    # ismags = nx.isomorphism.ISMAGS(g1, g2)
    # ismags.largest_common_graph()

    # Method 3: Partial isomorphism
    gm = nx.isomorphism.GraphMatcher(g1, g2)
    max_iters = 0

    def partial_match(self):
        """
        Patch the original match function, to find a 'almost' isomorphism
        """
        self.max_core = max(self.max_core, len(self.core_1))
        self.current_iter += 1

        if len(self.core_1) >= len(self.G2) or self.current_iter >= self.max_iters:  # <= Good enough here
            self.mapping = self.core_1.copy()
            yield self.mapping
        else:
            for G1_node, G2_node in self.candidate_pairs_iter():
                if self.syntactic_feasibility(G1_node, G2_node):
                    if self.semantic_feasibility(G1_node, G2_node):
                        newstate = self.state.__class__(self, G1_node, G2_node)
                        yield from self.match()
                        newstate.restore()

    gm.match = MethodType(partial_match, gm)
    gm.max_iters = 10_0000
    gm.current_iter = 0
    gm.max_core = 0
    
    print(gm.subgraph_is_isomorphic())
    print(gm.max_core)
    return gm.max_core
