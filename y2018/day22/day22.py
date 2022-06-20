import heapq
import numpy as np
from cave import Region, Tool

MOD = 20183

THRESHOLD = 1000
DEPTH = 8112
# (x, y), not (r, c) this time
TARGET = (13, 743)


def neighbors(x: int, y: int, x_max: int, y_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
    ] if 0 <= p[0] < y_max and 0 <= p[1] < x_max]


erosion = np.empty(
    (TARGET[0] + 1 + THRESHOLD, TARGET[1] + 1 + THRESHOLD),
    dtype=np.int64
)
erosion[0] = (np.arange(len(erosion[0])) * 48271 + DEPTH) % MOD
for x in range(1, len(erosion)):
    for y in range(len(erosion[x])):
        if y == 0:
            erosion[x, y] = (x * 16807 + DEPTH) % MOD
        else:
            erosion[x, y] = (
                erosion[x - 1, y] * erosion[x, y - 1] + DEPTH
            ) % MOD

risk = erosion % 3
risk[TARGET] = 0
print(f"total risk: {risk[:TARGET[0] + 1, :TARGET[1] + 1].sum()}")

cave = np.empty_like(risk, dtype=Region)
for x in range(len(risk)):
    for y in range(len(risk[x])):
        cave[x, y] = Region(risk[x, y])

costs = np.empty(erosion.shape + (len(Tool),), dtype=np.int64)
costs.fill(np.iinfo(costs.dtype).max)
start = 0, 0, Tool.TORCH.value
costs[start] = 0
frontier = [(costs[start], *start)]
while frontier:
    curr_cost, x, y, tool = heapq.heappop(frontier)
    tool = Tool(tool)
    if curr_cost != costs[x, y, tool.value]:
        continue
    if (x, y, tool.value) == (TARGET[0], TARGET[1], Tool.TORCH.value):
        break

    good_region = tool.compatible()
    # try moving to another tile
    for n in neighbors(x, y, *cave.shape):
        if (cave[n] in good_region
                and curr_cost + 1 < costs[n[0], n[1], tool.value]):
            costs[n[0], n[1], tool.value] = curr_cost + 1
            heapq.heappush(frontier, (
                costs[n[0], n[1], tool.value], *n, tool.value
            ))

    for t in cave[x, y].compatible():
        if t != tool and curr_cost + 7 < costs[x, y, t.value]:
            costs[x, y, t.value] = curr_cost + 7
            heapq.heappush(frontier, (
                costs[x, y, t.value], x, y, t.value
            ))

min_time = costs[TARGET[0], TARGET[1], Tool.TORCH.value]
print(f"min time to reach target: {min_time}")
