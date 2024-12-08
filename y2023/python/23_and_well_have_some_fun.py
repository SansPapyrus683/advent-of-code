import sys
import typing as t
from collections.abc import Collection, Callable

T = t.TypeVar("T")  # what is it with me and type annotations seriously
WALL = "#"
DIRS = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1)
}


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def next_p1(grid: list[str], r: int, c: int) -> list[tuple[int, int]]:
    curr = grid[r][c]
    if curr in DIRS:
        dir_ = DIRS[curr]
        next_ = [(r + dir_[0], c + dir_[1])]
    else:
        next_ = neighbors4(r, c, len(grid), len(grid[0]))
    return [(a, b) for a, b in next_ if grid[a][b] != WALL]


def next_p2(grid: list[str], r: int, c: int) -> list[tuple[int, int]]:
    return [
        (a, b) for a, b in neighbors4(r, c, len(grid), len(grid[0]))
        if grid[a][b] != WALL
    ]


# mfw type annotations take up 90% of the line :skull:
def pt_dists(
        grid: list[str], pts: Collection[tuple[int, int]],
        next_func: Callable[[list[str], int, int], list[tuple[int, int]]]
) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    dists = {p: {} for p in pts}
    for p in pts:
        frontier = [p]
        visited2 = set(frontier)
        steps = 0
        while frontier or frontier:
            next_up = []
            for curr in frontier:
                if curr != p and curr in pts:
                    dists[p][curr] = steps
                    continue

                for nr, nc in next_func(grid, *curr):
                    if (nr, nc) not in visited2:
                        visited2.add((nr, nc))
                        next_up.append((nr, nc))
            steps += 1
            frontier = next_up
    return dists


def longest_path(start: T, end: T, neighbors: dict[T, dict[T, int]]) -> int:
    longest = 0
    curr_dist = 0
    prev = {start}

    def dfs(at: T):
        nonlocal longest, curr_dist
        if at == end:
            longest = max(longest, curr_dist)
            return
        for n, nd in neighbors[at].items():
            if n not in prev:
                prev.add(n)
                curr_dist += nd
                dfs(n)
                prev.remove(n)
                curr_dist -= nd

    dfs(start)
    return longest


grid = [r.strip() for r in sys.stdin]

start = 1, 0
end = len(grid) - 1, len(grid[0]) - 2
juncs = {start, end}
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == WALL:
            continue
        n_amt = sum(
            grid[nr][nc] != WALL
            for nr, nc in neighbors4(r, c, len(grid), len(grid[0]))
        )
        if n_amt > 2:
            juncs.add((r, c))

p1_dist = pt_dists(grid, juncs, next_p1)
p2_dist = pt_dists(grid, juncs, next_p2)
print(f"bro eric wth: {longest_path(start, end, p1_dist)}")
print(f"p2 is literally np complete: {longest_path(start, end, p2_dist)}")
