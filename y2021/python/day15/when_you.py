import numpy as np
from heapq import heappush, heappop

DUP_AMT = 5


def neighbors(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    test_neighbors = [
        (r, c + 1),
        (r, c - 1),
        (r + 1, c),
        (r - 1, c)
    ]
    return [n for n in test_neighbors if 0 <= n[0] < r_max and 0 <= n[1] < c_max]


def min_risk(risks: np.ndarray) -> int:
    costs = np.zeros_like(risks).astype(np.int64)
    costs.fill(np.iinfo(np.int64).max)

    frontier = [(0, 0, 0)]
    costs[0, 0] = 0
    while frontier:
        curr = heappop(frontier)
        if costs[curr[1:]] != curr[0]:
            continue
        curr_cost = curr[0]
        curr = curr[1:]
        for n in neighbors(curr[0], curr[1], len(risks), len(risks[0])):
            n_cost = curr_cost + risks[n]
            if n_cost < costs[n]:
                costs[n] = n_cost
                heappush(frontier, (n_cost, ) + n)
    return costs[-1, -1]


with open("in_town.txt") as read:
    cavern = np.array([[int(i) for i in l.strip()] for l in read.readlines()])
cavern = np.array(cavern)

print(f"BRUH I THOUGHT YOU COULD ONLY GO RIGHT OR DOWN: {min_risk(cavern)}")

r_num = len(cavern)
c_num = len(cavern[0])
new_cavern = np.zeros((r_num * DUP_AMT, c_num * DUP_AMT)).astype(np.int64)
for r in range(r_num):
    for c in range(c_num):
        for r_add in range(DUP_AMT):
            for c_add in range(DUP_AMT):
                to_add = r_add + c_add
                nr = r + r_add * r_num
                nc = c + c_add * c_num
                new_cavern[nr, nc] = cavern[r, c] + to_add
                if new_cavern[nr, nc] >= 10:
                    new_cavern[nr, nc] -= 9
print(f"the array manip in this problem was hell omg: {min_risk(new_cavern)}")
