import sys
from copy import deepcopy

P2_CYCLES = 8


def load(dish: list[list[str]]) -> int:
    ret = 0
    for r in range(len(dish)):
        for c in range(len(dish[r])):
            # "O" is just used in 2 places, i'm too lazy to make it const
            if dish[r][c] == "O":
                ret += len(dish) - r
    return ret


def add_pt(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def tilt(dish: list[list[str]], dir_: int):
    points = [(r, c) for r in range(len(dish)) for c in range(len(dish[0]))]
    if dir_ == 0:  # north
        points.sort(key=lambda p: p[0])
        delta = -1, 0
    elif dir_ == 1:  # west
        points.sort(key=lambda p: p[1])
        delta = 0, -1
    elif dir_ == 2:  # south
        points.sort(key=lambda p: -p[0])
        delta = 1, 0
    elif dir_ == 3:  # east
        points.sort(key=lambda p: -p[1])
        delta = 0, 1
    else:
        raise ValueError(f"invalid direction {dir_}")

    for p in points:
        if dish[p[0]][p[1]] != "O":
            continue
        while True:
            n = add_pt(p, delta)
            in_bounds = 0 <= n[0] < len(dish) and 0 <= n[1] < len(dish[1])
            if not in_bounds or dish[n[0]][n[1]] == "#":
                break
            # just swaps the rock and the empty space
            dish[p[0]][p[1]], dish[n[0]][n[1]] = dish[n[0]][n[1]], dish[p[0]][p[1]]
            p = n


dish = [list(r.strip()) for r in sys.stdin]

p1_dish = deepcopy(dish)
tilt(p1_dish, 0)
p1_load = load(p1_dish)

p2_dish = deepcopy(dish)
cyc_at = 1
visited = {}
while True:
    for d in range(4):
        tilt(p2_dish, d)

    state = tuple("".join(r) for r in p2_dish)
    if state in visited:
        break
    visited[state] = cyc_at
    cyc_at += 1

start = visited[state]
mod = cyc_at - start
if P2_CYCLES <= start:
    offset = P2_CYCLES
else:
    offset = start + (P2_CYCLES - start) % mod

p2_load = -1
for d, i in visited.items():
    if i == offset:
        p2_load = load(d)
        break
assert p2_load != -1

print(f"OMG I READ THE PROBLEM WRONG: {p1_load}")
print(f"I THOUGHT A CYCLE WAS JUST ONE TILT: {p2_load}")
