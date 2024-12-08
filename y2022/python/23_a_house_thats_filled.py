import sys
from collections import defaultdict

ELF = "#"
P1_STEP_AMT = 10
PADDING = 50


def neighbors8(r: int, c: int) -> list[tuple[int, int]]:
    return [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ]


def move(elves: set[tuple[int, int]], pos: tuple[int, int], step: int) -> tuple[int, int]:
    for n in neighbors8(pos[0], pos[1]):
        if n in elves:
            break
    else:
        return pos

    # north, south, west, east ig
    delta_reqs = [
        (lambda r, c: [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)], lambda r, c: (r - 1, c)),
        (lambda r, c: [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)], lambda r, c: (r + 1, c)),
        (lambda r, c: [(r - 1, c - 1), (r, c - 1), (r + 1, c - 1)], lambda r, c: (r, c - 1)),
        (lambda r, c: [(r - 1, c + 1), (r, c + 1), (r + 1, c + 1)], lambda r, c: (r, c + 1)),
    ]
    for i in range(len(delta_reqs)):
        check, move_to = delta_reqs[(step + i) % len(delta_reqs)]
        for n in check(*pos):
            if n in elves:
                break
        else:
            return move_to(*pos)
    return pos


grid = [row.strip() for row in sys.stdin]

elves = set()
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == ELF:
            elves.add((r, c))

steps = 0
moved = True
p1_state = None
p2_steps = -1
while steps < P1_STEP_AMT or moved:
    moved = False
    proposed = defaultdict(list)
    for e in elves:
        prop = move(elves, e, steps)
        if prop != e:
            moved = True
        proposed[prop].append(e)

    new = set()
    for p, e in proposed.items():
        if len(e) == 1:
            new.add(p)
        else:
            for i in e:
                new.add(i)

    elves = new

    steps += 1
    if steps == P1_STEP_AMT:
        p1_state = elves
    if not moved and p2_steps == -1:
        p2_steps = steps

assert p1_state is not None and p2_steps != -1

min_r = float("inf")
max_r = -float("inf")
min_c = float("inf")
max_c = -float("inf")
for r, c in p1_state:
    min_r = min(min_r, r)
    max_r = max(max_r, r)
    min_c = min(min_c, c)
    max_c = max(max_c, c)

unfilled = 0
for r in range(min_r, max_r + 1):
    for c in range(min_c, max_c + 1):
        unfilled += (r, c) not in p1_state

print(f"empty ground tiles of elf bounding box: {unfilled}")
print(f"number of steps to reach a stable state: {p2_steps}")
