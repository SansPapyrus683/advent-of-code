import sys


def neighbors(r: int, c: int, r_max: int, c_max: int) -> [(int, int)]:
    test_neighbors = [
        (r, c + 1),
        (r, c - 1),
        (r + 1, c),
        (r - 1, c)
    ]
    return [n for n in test_neighbors if 0 <= n[0] < r_max and 0 <= n[1] < c_max]


floor = [[int(i) for i in r.strip()] for r in sys.stdin]
assert len(set(len(r) for r in floor)) == 1

row_num = len(floor)
col_num = len(floor[0])

total = 0
for r in range(row_num):
    for c in range(col_num):
        for n in neighbors(r, c, row_num, col_num):
            if floor[n[0]][n[1]] <= floor[r][c]:
                break
        else:
            total += floor[r][c] + 1
print(f"wait why did we have to add 1 that's scuffed as hell: {total}")

visited = [[False for _ in range(col_num)] for _ in range(row_num)]
sizes = []
for r in range(row_num):
    for c in range(col_num):
        if floor[r][c] == 9 or visited[r][c]:
            continue

        frontier = [(r, c)]
        basin = []  # may contain dupes for whatever reason
        while frontier:
            curr = frontier.pop()
            basin.append(curr)
            visited[curr[0]][curr[1]] = True
            for n in neighbors(curr[0], curr[1], row_num, col_num):
                if not visited[n[0]][n[1]] and floor[n[0]][n[1]] != 9:
                    frontier.append(n)
        sizes.append(len(set(basin)))
sizes.sort()

prod_num = 3
basin_prod = 1
for i in range(1, prod_num + 1):
    basin_prod *= sizes[-i]
print(f"wow the seafloor height variation is really small tho fr: {basin_prod}")
