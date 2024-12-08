import re
import sys
from collections import defaultdict

import networkx as nx

START = "AA"
TIME = 30

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

relevant = []
for v, r in rates.items():
    if r != 0:
        relevant.append(v)

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

best = 0
for mp in most_pressure:
    if mp:
        best = max(best, max(mp.values()))

print(f"damn, first time this year i had to sleep through: {best}")
