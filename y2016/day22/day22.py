import re
from dataclasses import dataclass


@dataclass
class Node:
    sz: int
    used: int
    avail: int
    use: int


def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


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
    grid[n[1]][n[0]] = Node(*n[2:])

all_nodes = []
for r in grid:
    all_nodes.extend(r)

total = 0
for i in range(len(all_nodes)):
    ni = all_nodes[i]
    if ni.used == 0:
        continue
    for j in range(len(all_nodes)):
        nj = all_nodes[j]
        total += i != j and ni.used <= nj.avail

print(f"number of viable pairs: {total}")
