import sys
from collections import deque

START = "S"
END = "E"


def neighbors(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


grid = []
for r in sys.stdin:
    grid.append([ord(c) for c in r.strip()])

# just some shorthands
r_num = len(grid)
c_num = len(grid[0])

end = None
start = None
for r in range(r_num):
    for c in range(c_num):
        if grid[r][c] == ord(END):
            assert end is None
            end = (r, c)
            grid[r][c] = ord("z")
        elif grid[r][c] == ord(START):
            assert start is None
            start = (r, c)
            grid[r][c] = ord("a")
assert start is not None and end is not None

min_dist = [[float("inf") for _ in range(c_num)] for _ in range(r_num)]
frontier = deque([end])
min_dist[end[0]][end[1]] = 0
while frontier:
    cr, cc = frontier.popleft()
    new_dist = min_dist[cr][cc] + 1
    for nr, nc in neighbors(cr, cc, r_num, c_num):
        if grid[cr][cc] - grid[nr][nc] <= 1 and new_dist < min_dist[nr][nc]:
            min_dist[nr][nc] = new_dist
            frontier.append((nr, nc))

total_shortest = float("inf")
for r in range(r_num):
    for c in range(c_num):
        if grid[r][c] == ord("a"):
            if (r, c) == start:
                print(f"shortest distance from given start: {min_dist[r][c]}")
            total_shortest = min(total_shortest, min_dist[r][c])

print(f"total shortest distance: {total_shortest}")
