import sys
from collections.abc import Collection
from collections import deque

WIDTH = 70


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def shortest_path(
    corrupted: Collection[tuple[int, int]],
    start: tuple[int, int] = (0, 0),
    end: tuple[int, int] = (WIDTH, WIDTH),
) -> int | None:
    frontier = deque([start])
    min_dist = {start: 0}
    while frontier:
        curr = frontier.popleft()
        if curr == end:
            return min_dist[end]
        for n in neighbors4(*curr, WIDTH + 1, WIDTH + 1):
            if n not in corrupted and n not in min_dist:
                min_dist[n] = min_dist[curr] + 1
                frontier.append(n)
    return None


points = []
for pt in sys.stdin:
    x, y = [int(i) for i in pt.split(",")]
    points.append((x, y))

first_kb = set(points[:1024])
print(f"lol i've shifted my aim from t100 to just t200: {shortest_path(first_kb)}")

lo = 1
hi = len(points)
valid = -1
while lo <= hi:
    mid = (lo + hi) // 2
    if shortest_path(set(points[:mid])) is None:
        valid = points[mid - 1]
        hi = mid - 1
    else:
        lo = mid + 1

print(f"i mean i'm stressing less this year, which is great imo: {valid[0]},{valid[1]}")
