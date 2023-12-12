from itertools import permutations

START = 0
EMPTY = "."


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


with open("input/day24.txt") as read:
    grid = []
    nums = {}
    for r, row in enumerate(read.readlines()):
        row = row.strip()
        for c, col in enumerate(row):
            if col.isdigit():
                nums[int(col)] = r, c
        grid.append(row)
    assert START in nums

dist = {n: {} for n in nums}
for num, start in nums.items():
    frontier = [start]
    visited = set(frontier)
    moves = 0
    while frontier:
        next_up = []
        for r, c in frontier:
            if grid[r][c].isdigit():
                dist[num][int(grid[r][c])] = moves

            for nr, nc in neighbors4(r, c, len(grid), len(grid[0])):
                is_open = grid[nr][nc] == EMPTY or grid[nr][nc].isdigit()
                if (nr, nc) not in visited and is_open:
                    visited.add((nr, nc))
                    next_up.append((nr, nc))

        frontier = next_up
        moves += 1

not_start = [n for n in nums if n != START]
p1_dist = float("inf")
p2_dist = float("inf")
for order in permutations(not_start):
    curr_dist = 0
    at = START
    for i in order:  # why the hell does intellij think order is an int
        curr_dist += dist[at][i]
        at = i

    p1_dist = min(p1_dist, curr_dist)
    p2_dist = min(p2_dist, curr_dist + dist[at][START])

print(f"min dist to all #'s: {p1_dist}")
print(f"min dist to all #'s: {p2_dist}")
