from collections import deque as dq
from heapq import *

# bfs
start = None
frontier = dq([start])
min_dist = {start: 0}
while frontier:
    curr = frontier.popleft()
    n_states = []
    # add stuff to n_states here
    for n in n_states:
        if n not in min_dist:
            min_dist[n] = min_dist[curr] + 1
            frontier.append(n)

# dijkstra's
frontier = [(0, start)]
min_dist = {start: 0}
while frontier:
    cost, curr = heappop(frontier)
    if cost != min_dist[curr]:
        continue

    n_states = []  # (new_cost, new_state)
    for n_cost, n in n_states:
        if n not in min_dist or n_cost < min_dist[n]:
            min_dist[n] = n_cost
            heappush(frontier, (n_cost, n))
