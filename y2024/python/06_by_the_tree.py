import sys

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def traverse(
    grid: list[list[str]], start: tuple[int, int], dir_: int = 0
) -> tuple[bool, set[tuple[tuple[int, int], int]]]:
    visited = set()
    at = start
    d_at = dir_
    while (at, d_at) not in visited:
        visited.add((at, d_at))
        next_at = at[0] + DIRS[d_at][0], at[1] + DIRS[d_at][1]
        if not (0 <= next_at[0] < len(grid) and 0 <= next_at[1] < len(grid[0])):
            return False, visited

        if grid[next_at[0]][next_at[1]] == "#":
            d_at = (d_at + 1) % len(DIRS)
        else:
            at = next_at

    return True, visited


grid = [list(row.strip()) for row in sys.stdin]

start = None
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == "^":
            start = r, c
assert start is not None

p1_visited = traverse(grid, start)[1]
distinct = {i[0] for i in p1_visited}

print(f"ok i barely scraped into top 100 today: {len(distinct)}")

looping_obstacles = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if (r, c) not in distinct:
            continue
        grid[r][c] = "#"
        looping_obstacles += traverse(grid, start)[0]
        grid[r][c] = "."

print(f"but thank god i'm not the only one mad about ppl gpt-ing: {looping_obstacles}")
