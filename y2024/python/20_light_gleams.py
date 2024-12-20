import sys
from collections import deque


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def min_dist(grid: list[str], start: tuple[int, int]):
    frontier = deque([start])
    dists = {start: 0}
    while frontier:
        curr = frontier.popleft()
        for n in neighbors4(*curr, len(grid), len(grid[0])):
            if grid[n[0]][n[1]] != "#" and n not in dists:
                frontier.append(n)
                dists[n] = dists[curr] + 1
    return dists


cpu = [row.strip() for row in sys.stdin]

from_start = None
from_end = None
end = None
for r in range(len(cpu)):
    for c in range(len(cpu[0])):
        if cpu[r][c] == "S":
            from_start = min_dist(cpu, (r, c))
        elif cpu[r][c] == "E":
            end = r, c
            from_end = min_dist(cpu, (r, c))
assert from_start is not None and from_end is not None
raw_cost = from_start[end]

for delta in [2, 20]:
    deltas = []
    # could probably make this a list comp, but i don't care
    for dr in range(-delta, delta + 1):
        for dc in range(-delta + abs(dr), delta + 1 - abs(dr)):
            deltas.append((dr, dc))

    cheats = 0
    for r in range(len(cpu)):
        for c in range(len(cpu[0])):
            if cpu[r][c] == "#":
                continue
            for dr, dc in deltas:
                er, ec = r + dr, c + dc
                in_bounds = 0 <= er < len(cpu) and 0 <= ec < len(cpu[0])
                if not in_bounds or cpu[er][ec] == "#":
                    continue

                cost = from_start[(r, c)] + abs(dr) + abs(dc) + from_end[(er, ec)]
                cheats += raw_cost - cost >= 100

    print(f"best dist given cheats of length {delta}: {cheats}")
