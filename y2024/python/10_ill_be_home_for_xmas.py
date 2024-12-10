import sys


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


grid = [[int(i) for i in row.strip()] for row in sys.stdin]

score_sum = 0
rating_sum = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] != 0:
            continue

        trailheads = set()
        num_paths = 0

        def dfs(at: tuple[int, int], visited: set[tuple[int, int]]):
            global num_paths

            curr = grid[at[0]][at[1]]
            if curr == 9:
                trailheads.add(at)
                num_paths += 1
                return

            for nr, nc in neighbors4(*at, len(grid), len(grid[0])):
                if grid[nr][nc] == curr + 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    dfs((nr, nc), visited)
                    visited.remove((nr, nc))


        dfs((r, c), {(r, c)})
        score_sum += len(trailheads)
        rating_sum += num_paths

print(f"ok still no placement today: {score_sum}")
print(f"but i still think i was pretty fast! {rating_sum}")
