import sys
from collections import deque


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def neighbors4raw(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


grid = [line.strip() for line in sys.stdin]

row_num = len(grid)
col_num = len(grid[0])

visited = [[False for _ in range(col_num)] for _ in range(row_num)]
price_p1 = price_p2 = 0
for r in range(row_num):
    for c in range(row_num):
        if visited[r][c]:
            continue

        visited[r][c] = True
        frontier = deque([(r, c)])
        covered = {(r, c)}
        while frontier:
            curr = frontier.popleft()
            for n in neighbors4(*curr, row_num, col_num):
                if grid[n[0]][n[1]] == grid[r][c] and n not in covered:
                    visited[n[0]][n[1]] = True
                    covered.add(n)
                    frontier.append(n)

        edges = []
        for p in covered:
            for n in neighbors4raw(*p):
                if n not in covered:
                    edges.append((p, n))
        price_p1 += len(covered) * len(edges)

        vert = []
        horz = []
        for i, o in edges:  # in & out
            (vert if i[1] != o[1] else horz).append((min(i, o), i < o))
        vert.sort(key=lambda k: (k[0][1], k[0][0]))
        horz.sort()

        sides = 2
        for i in range(1, len(vert)):
            curr, prev = vert[i], vert[i - 1]  # more shorthands
            pos_diff = curr[0][1] != prev[0][1] or curr[0][0] > prev[0][0] + 1
            sides += pos_diff or curr[1] != prev[1]
        for i in range(1, len(horz)):
            curr, prev = horz[i], horz[i - 1]  # more shorthands
            pos_diff = curr[0][0] != prev[0][0] or curr[0][1] > prev[0][1] + 1
            sides += pos_diff or curr[1] != prev[1]

        price_p2 += len(covered) * sides

print(f"ok this day was pretty bad but... {price_p1}")
print(f"the horrors persist but so do i! {price_p2}")
