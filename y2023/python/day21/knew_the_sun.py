WALL = "#"
P1_STEPS = 64
P2_STEPS = 26501365


def neighbors4raw(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def reachable(grid: list[str], start: tuple[int, int], steps: int) -> int:
    frontier = {start}
    for _ in range(steps):
        next_up = set()
        for r, c in frontier:
            for nr, nc in neighbors4raw(r, c):
                if grid[nr % len(grid)][nc % len(grid[0])] != WALL:
                    next_up.add((nr, nc))
        frontier = next_up
    return len(frontier)


with open("was_hot_that_day.txt") as read:
    grid = [r.strip() for r in read.readlines()]
assert {len(grid)} == {len(grid[r]) for r in range(len(grid))}, "grid must be square"

side = len(grid)
mid = len(grid) // 2
start = mid, mid
assert grid[start[0]][start[1]] == "S", "elf has to start in the middle"
assert side % 2 == 1, "side length has to be odd"

p1_reachable = reachable(grid, start, P1_STEPS)

# doing math in programming really sucks huh
x, y, z = [reachable(grid, start, mid + d * side) for d in range(3)]
c = x
a = (z - x) // 2 - (y - x)
b = y - x - a

assert (P2_STEPS - mid) % side == 0, "i think something's wrong w/ your input"
extend = (P2_STEPS - mid) // side

p2_reachable = a * extend ** 2 + b * extend + c

print(f"aoc might be bad for my mental health {p1_reachable}")
print(f"but i require the dopamine of leaderboards {p2_reachable}")
