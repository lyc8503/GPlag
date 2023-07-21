from pdg_parser import load_all_pdgs
from graph import count_nodes_and_edges, match_pair


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
        matched_node_count += match_pair(*p)
    
    print("Overall matched node count: " + str(matched_node_count))
    print("Total1 : " + str(count_nodes_and_edges(pdgs)))
    print("Total2 : " + str(count_nodes_and_edges(pdgs2)))

