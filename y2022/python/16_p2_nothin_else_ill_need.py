import re
import sys
from collections import defaultdict

import networkx as nx

TIME = 26
START = "AA"

valve_fmt = re.compile(
    r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
)
graph = nx.DiGraph()
rates = {}
for v in sys.stdin:
    if valve_fmt.match(v):
        valve, rate, tunnels = valve_fmt.findall(v)[0]
        rates[valve] = int(rate)
        for t in tunnels.split(","):
            graph.add_edge(valve, t.strip())

relevant = set()
for v, r in rates.items():
    if r != 0:
        relevant.add(v)

dist = dict(nx.all_pairs_shortest_path_length(graph))
most_pressure = [defaultdict(int) for _ in range(TIME)]
most_pressure[0][(START, ())] = 0
for t in range(TIME):
    for (at, opened), released in most_pressure[t].items():
        for v in relevant:
            n_time = t + dist[at][v]
            if n_time < TIME:
                next_ = most_pressure[n_time]
                next_[(v, opened)] = max(next_[(v, opened)], released)

        if at not in opened and t < TIME - 1 and at in relevant:
            n_released = released + rates[at] * (TIME - t - 1)
            n_opened = tuple(sorted(opened + (at,)))
            next_ = most_pressure[t + 1]
            next_[(at, n_opened)] = max(next_[(at, n_opened)], n_released)

subset_best = defaultdict(int)
for mp in most_pressure:
    for (_, opened), released in mp.items():
        subset_best[opened] = max(subset_best[opened], released)

best = 0
for opened in list(subset_best.keys()):
    e_opened = relevant.difference(set(opened))
    for other in subset_best.keys():
        if set(other).issubset(e_opened):
            best = max(best, subset_best[opened] + subset_best[other])

print(f"but jesus this problem was hard: {best}")
