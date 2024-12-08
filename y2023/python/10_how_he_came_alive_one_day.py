import sys
from collections import deque


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def pipe_next(
        r: int, c: int, r_max: int, c_max: int, char: str
) -> list[tuple[int, int]]:
    # screw it, i'm hardcoding the strings here, there's just too many
    return [p for p in [
        (r + 1, c) if char in "|F7" else None,
        (r - 1, c) if char in "|LJ" else None,
        (r, c + 1) if char in "-LF" else None,
        (r, c - 1) if char in "-7J" else None,
    ] if p is not None and 0 <= p[0] < r_max and 0 <= p[1] < c_max]


grid = [list(r.strip()) for r in sys.stdin]
r_num = len(grid)
c_num = len(grid[0])
assert all(len(r) == c_num for r in grid)

start = None
for r in range(r_num):
    for c in range(c_num):
        if grid[r][c] != "S":
            continue
        conns = {
            n for n in neighbors4(r, c, r_num, c_num)
            if (r, c) in pipe_next(*n, r_num, c_num, grid[n[0]][n[1]])
        }
        start = r, c
        for poss in "|-F7LJ":
            if set(pipe_next(r, c, r_num, c_num, poss)) == conns:
                grid[r][c] = poss
                break
assert start is not None

frontier = deque([start])
loop = {start: 0}
while frontier:
    r, c = frontier.popleft()
    for n in pipe_next(r, c, r_num, c_num, grid[r][c]):
        if n not in loop:
            loop[n] = loop[(r, c)] + 1
            frontier.append(n)

for r in range(r_num):
    for c in range(c_num):
        if (r, c) not in loop:
            grid[r][c] = "."

in_area = 0
for r in range(r_num):
    crosses = 0
    last_junc = None
    for c in grid[r]:
        if c == "|":
            crosses += 1
        elif c in "F7LJ":
            if last_junc is None:
                last_junc = c
            else:
                crosses += {last_junc, c} in [{"F", "J"}, {"L", "7"}]
                last_junc = None
        elif c == ".":
            in_area += crosses % 2 == 1

print(f"wow today's problem was very nontrivial: {max(loop.values())}")
print(f"thank goodness i read a gfg article about this: {in_area}")
