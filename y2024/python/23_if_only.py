import sys
from itertools import combinations
import networkx as nx

graph = nx.Graph()
for edge in sys.stdin:
    a, b = edge.strip().split("-")
    graph.add_edge(a, b)

has_t = set()
largest = []
for clique in nx.find_cliques(graph):
    for size3 in combinations(clique, 3):
        if any(c.startswith("t") for c in size3):
            has_t.add(tuple(sorted(size3)))
    if len(clique) > len(largest):
        largest = clique

p2_ans = ",".join(sorted(largest))
print(f"dogwater problem today: {len(has_t)}")
print(f"like there wasn't even any attempt to hide it: {p2_ans}")
