import sys
import heapq
from collections import defaultdict

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def shortest_dists(
        grid: list[list[str]], starts: list[tuple[int, int, int]], rev: bool = False
):
    mul = -1 if rev else 1
    frontier = []
    start_dist = defaultdict(lambda: float("inf"))
    for s in starts:
        heapq.heappush(frontier, (0, s))
        start_dist[s] = 0
    while frontier:
        cost, (cr, cc, cd) = heapq.heappop(frontier)
        if cost != start_dist[(cr, cc, cd)]:
            continue

        next_states = []
        for nd in [(cd - 1) % len(DIRS), (cd + 1) % len(DIRS)]:
            next_states.append((cost + 1000, (cr, cc, nd)))

        adj = cr + mul * DIRS[cd][0], cc + mul * DIRS[cd][1]
        in_bounds = 0 <= adj[0] < len(grid) and 0 <= adj[1] < len(grid)
        if in_bounds and grid[adj[0]][adj[1]] != "#":
            next_states.append((cost + 1, (*adj, cd)))

        for n_cost, n in next_states:
            if n_cost < start_dist[n]:
                start_dist[n] = n_cost
                heapq.heappush(frontier, (n_cost, n))
    return start_dist


maze = [list(row.strip()) for row in sys.stdin]
start, end = None, None
for r in range(len(maze)):
    for c, cell in enumerate(maze[r]):
        if cell == "S":
            start = r, c
        elif cell == "E":
            end = r, c

from_start = shortest_dists(maze, [(start[0], start[1], 0)])

best = min(from_start[(end[0], end[1], d)] for d in range(len(DIRS)))
endings = []
for d in range(len(DIRS)):
    state = end[0], end[1], d
    if from_start[state] == best:
        endings.append(state)
from_end = shortest_dists(maze, endings, True)

good_seats = 0
for r in range(len(maze)):
    for c, cell in enumerate(maze[r]):
        if cell == "#":
            continue

        good_seats += any(
            from_start[(r, c, d)] + from_end[(r, c, d)] == best
            for d in range(len(DIRS))
        )

print(f"ok like no global lb today: {best}")
print(f"but considering i was 30k feet in the air i'll take it: {good_seats}")
