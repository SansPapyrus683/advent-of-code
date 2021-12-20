import numpy as np
from collections import defaultdict
from itertools import permutations, product

DIM_NUM = 3
THRESHOLD = 12


def valid_rotation(perm: np.ndarray, plus_min: np.ndarray) -> bool:
    assert perm.shape == plus_min.shape == (DIM_NUM,)
    array = np.zeros((DIM_NUM, DIM_NUM), dtype=int)
    for (a, b, c) in zip(perm, range(DIM_NUM), plus_min):
        array[a, b] = c
    return np.linalg.det(array) > 0


with open("we_made.txt") as read:
    reports = [r.split("\n")[1:] for r in read.read().strip().split("\n\n")]
for i in range(len(reports)):
    reports[i] = [np.array([int(i) for i in r.split(",")]) for r in reports[i]]

all_perms = np.array([list(i) for i in permutations(range(DIM_NUM))])
plus_mins_all = np.array([list(i) for i in product([1, -1], repeat=DIM_NUM)])
combinations = []
for p in all_perms:
    for pm in plus_mins_all:
        if valid_rotation(p, pm):
            combinations.append((p, pm))

positions = [None for _ in range(len(reports))]
positions[0] = np.zeros((DIM_NUM,))
tested_alr = np.zeros((len(reports), len(reports)), dtype=np.bool)
while not all(p is not None for p in positions):
    for i in range(len(positions)):
        if positions[i] is None:
            continue
        known_rep = reports[i]

        for j in range(len(positions)):
            if positions[j] is not None or tested_alr[i, j]:
                continue
            unknown_rep = reports[j]

            most_common = []
            for perm, pm in combinations:
                all_points = defaultdict(int)
                for p1 in known_rep:
                    for p2 in unknown_rep:
                        new_p2 = p2[perm] * pm
                        all_points[tuple(p1 - new_p2)] += 1

                all_points = [(v, o) for o, v in all_points.items()]
                most_common.append((*max(all_points), pm, perm))

            occ_amt, delta, pm, perm = max(most_common)
            if occ_amt >= THRESHOLD:
                delta = np.array(delta)
                reports[j] = [p[perm] * pm + delta for p in reports[j]]
                positions[j] = delta
            tested_alr[i][j] = True

beacons = set()
for r in reports:
    for p in r:
        beacons.add(tuple(p))
print(f"think this should be the hardest problem this year: {len(beacons)}")

max_position = 0
for i in range(len(positions)):
    for j in range(i + 1, len(positions)):
        max_position = max(max_position, np.abs(positions[i] - positions[j]).sum())
print(f"istg how do people solve this crap in 30 mins: {max_position}")
