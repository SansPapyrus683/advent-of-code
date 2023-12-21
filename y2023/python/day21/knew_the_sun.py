WALL = "#"
P1_STEPS = 64
P2_STEPS = 26501365


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


with open("was_hot_that_day.txt") as read:
    grid = [r.strip() for r in read.readlines()]

side = len(grid)
mid = len(grid) // 2
start = mid, mid

assert {len(grid)} == {len(grid[r]) for r in range(len(grid))}, "grid must be square"
assert grid[start[0]][start[1]] == "S", "elf has to start in the middle"
assert side % 2 == 1, "side length has to be odd"

p1_frontier = {start}

steps = 0
for _ in range(P1_STEPS):
    next_up = set()
    for r, c in p1_frontier:
        for nr, nc in neighbors4(r, c, side, side):
            if grid[nr][nc] != WALL:
                next_up.add((nr, nc))
    p1_frontier = next_up
    steps += 1

p2_frontier = [start]
visited = {start}
while p2_frontier:
    r, c = p2_frontier.pop()
    for nr, nc in neighbors4(r, c, side, side):
        if grid[nr][nc] != WALL and (nr, nc) not in visited:
            visited.add((nr, nc))
            p2_frontier.append((nr, nc))

dots = [0, 0]
corners = [0, 0]
for r in range(side):
    for c in range(side):
        if (r, c) not in visited:
            continue
        parity = (r + c) % 2
        dots[parity] += 1
        if abs(r - start[0]) + abs(c - start[1]) > mid:
            corners[parity] += 1

assert (P2_STEPS - mid) % side == 0, "i think something's wrong w/ your input"
extend = (P2_STEPS - mid) // side

start_parity = P2_STEPS % 2
bound_parity = (start_parity + extend) % 2
p2_reachable = (
        sum(dots) * extend**2
        + dots[bound_parity] * (2 * extend + 1)
        - corners[bound_parity] * (extend + 1)
        + corners[1 - bound_parity] * extend
)

print(f"next day again...turns out i sillied my p2: {len(p1_frontier)}")
print(f"turns out not every dot is reachable :sob: {p2_reachable}")
