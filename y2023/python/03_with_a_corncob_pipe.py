import sys
from collections import defaultdict

EMPTY = "."


def neighbors8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


grid = [l.strip() + EMPTY for l in sys.stdin]

num_tot = 0
gears = defaultdict(list)
for i, row in enumerate(grid):
    j = 0
    while j < len(row):
        if row[j].isdigit():
            next_j = j
            while row[next_j].isdigit():
                next_j += 1

            num = int(row[j:next_j])
            symbol_adj = False
            procced = False
            for thing in range(j, next_j):
                for nr, nc in neighbors8(i, thing, len(grid), len(grid[0])):
                    if grid[nr][nc] != EMPTY and not grid[nr][nc].isdigit():
                        symbol_adj = True
                        if grid[nr][nc] == "*" and not procced:
                            procced = True
                            gears[(nr, nc)].append(num)

            if symbol_adj:
                num_tot += num

            j = next_j

        j += 1

prod = 0
for i in gears.values():
    if len(i) == 2:
        prod += i[0] * i[1]

print(f"WE'RE SO BACK: {num_tot}")
print(f"my template comes in and saves the day! {prod}")
