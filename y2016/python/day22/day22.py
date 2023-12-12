import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Node:
    sz: int
    used: int
    avail: int


@lru_cache
def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


node_fmt = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
with open("day22.txt") as read:
    # we don't need the initial two lines
    read.readline()
    read.readline()

    nodes = []
    for n in read.readlines():
        res = re.findall(node_fmt, n)
        if res:
            res = [int(i) for i in res[0]]
            nodes.append(res)

max_x = max(n[0] for n in nodes)
max_y = max(n[1] for n in nodes)
# type annotations so intellij stops bugging me
grid: list[list[Node | None]] = [[None for _ in range(max_x + 1)] for _ in range(max_y + 1)]
for n in nodes:
    grid[n[1]][n[0]] = Node(*n[2:5])
assert all(all(c is not None for c in r) for r in grid)

all_nodes = []
for r in grid:
    all_nodes.extend(r)

viable_pairs = 0
for i in range(len(all_nodes)):
    ni = all_nodes[i]
    if ni.used == 0:
        continue
    for j in range(len(all_nodes)):
        nj = all_nodes[j]
        viable_pairs += i != j and ni.used <= nj.avail

print(f"number of viable pairs: {viable_pairs}")

"""
NOTE: P2 relies on some observation of the input, which is really dumb imo
if you look at the sizes,  most nodes can fit exactly one other node in them
this is except for a couple of nodes that have like 10x more space & data
these nodes are basically frozen
there is also one (1) node that has 0% usage
"""
threshold = 200  # arbitrary, may vary based on your input

blocks = set()
goal = 0, 0
init_pos = 0, max_x
init_empty = None
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if grid[y][x].used == 0:
            assert init_empty is None  # should be only one(?)
            init_empty = y, x
        if grid[y][x].used > threshold:
            blocks.add((y, x))
assert init_empty is not None

frontier = [(init_pos, init_empty)]
visited = set(frontier)
moves = 0
while frontier:
    next_up = []
    found = False
    for curr, empty in frontier:
        if curr == goal:
            found = True
            break

        next_states = []
        if curr in neighbors4(*empty, max_y + 1, max_x + 1):
            next_states.append((empty, curr))
        for n in neighbors4(*empty, max_y + 1, max_x + 1):
            if n not in blocks and n != curr:
                next_states.append((curr, n))

        for s in next_states:
            if s not in visited:
                visited.add(s)
                next_up.append(s)
    if found:
        break
    frontier = next_up
    moves += 1

print(f"min # of moves to get to the target: {moves}")
