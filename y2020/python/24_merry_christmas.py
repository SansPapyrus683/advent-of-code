r"""
boy do i love stackoverflow
https://stackoverflow.com/questions/11373122
i actually rotated the coordinate system by 90 degrees
  _____       _____      ____      __
  / -2,2\_____/ 0,1 \____/2,0 \____/  \__
  \_____/-1,1 \_____/ 1,0\____/3,-1\__/
  /-2,1 \_____/0,0  \____/2,-1\____/  \__
  \_____/-1,0 \_____/1,-1\____/3,-2\__/
  /-2,0 \_____/ 0,-1\____/2,-2\____/  \__
  \_____/     \_____/    \____/    \__/
because as you can see this isn't oriented the right way for the problem
"""

import sys
from collections import defaultdict


def hex_neighbors(p: (int, int)) -> [(int, int)]:
    return [
        (p[0], p[1] + 1),
        (p[0] + 1, p[1]),
        (p[0] + 1, p[1] - 1),
        (p[0], p[1] - 1),
        (p[0] - 1, p[1]),
        (p[0] - 1, p[1] + 1),
    ]


instructions = []
valid = {"e", "se", "sw", "w", "nw", "ne"}
for line in sys.stdin:
    step_seq = []
    line = line.strip().lower()
    i = 0
    while i < len(line):
        if i < len(line) - 1 and line[i : i + 2] in valid:
            step_seq.append(line[i : i + 2])
            i += 1
        else:
            step_seq.append(line[i])
        i += 1
    instructions.append(step_seq)

tiles = defaultdict(lambda: True)  # all tiles start at True, or white
for i in instructions:
    pos = [0, 0]
    for s in i:
        if s == "e":
            pos[1] += 1
        elif s == "se":
            pos[0] += 1
        elif s == "sw":
            pos[0] += 1
            pos[1] -= 1
        elif s == "w":
            pos[1] -= 1
        elif s == "nw":
            pos[0] -= 1
        elif s == "ne":
            pos[0] -= 1
            pos[1] += 1
    pos = tuple(pos)
    tiles[pos] = not tiles[pos]
print(f"boy is this a crappy hotel: {list(tiles.values()).count(False)}")

# a bit slow, but it gets the job done
for _ in range(100):
    black_counts = defaultdict(int)
    to_process = []
    for t in tiles:
        to_process.append(t)
        to_process += hex_neighbors(t)
    to_process = set(to_process)

    for t in to_process:
        black_counts[t] = sum(not tiles[n] for n in hex_neighbors(t))

    for t, count in black_counts.items():
        if tiles[t] and count == 2:
            tiles[t] = False
        elif not tiles[t] and count == 0 or count > 2:
            tiles[t] = True

print(
    f"and how small are these tiles for {list(tiles.values()).count(False)} to fit on the floor"
)
