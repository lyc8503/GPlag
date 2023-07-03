from pdg_parser import load_all_pdgs
from graph import count_nodes_and_edges
import networkx as nx

from types import MethodType

import itertools

from tqdm import tqdm


if __name__ == '__main__':
    filter_pdg = lambda gs: [g for g in gs if len(g.edges) > 10 or len(g.nodes) > 10]
    pdgs = filter_pdg(load_all_pdgs("src1"))
    pdgs2 = filter_pdg(load_all_pdgs("src3"))

    matched_node_count = 0

    pairs = []

    for g1 in pdgs:
        for g2 in pdgs:
            pairs.append((g1, g2))
    

    for p in tqdm(pairs):

        # print(nx.graph_edit_distance(*p))
        gm = nx.isomorphism.GraphMatcher(*p)

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
        
        # print(len(p[0].nodes), len(p[1].edges))
        print(gm.subgraph_is_isomorphic())
        print(gm.max_core)
        matched_node_count += gm.max_core
        # print(mcs)
        # print(len(mcs.nodes), len(mcs.edges))

        # matched_node_count += len(getMCS(*p).nodes)
        # matched_edge_count += len(getMCS(*p).edges)
    
    print("Overall matched node count: " + str(matched_node_count))
    print("Total1 : " + str(count_nodes_and_edges(pdgs)))
    print("Total2 : " + str(count_nodes_and_edges(pdgs2)))

