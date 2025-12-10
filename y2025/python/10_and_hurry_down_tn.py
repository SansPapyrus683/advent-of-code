import sys
from itertools import product

import cvxpy as cp  # HAAAAANK!!!! DON'T ABBREVIATE CVXPY!!!! HAAAAAANK!!!
import numpy as np

p1_presses = 0
p2_presses = 0
for line in sys.stdin:
    line = line.strip().split()

    on = np.array([int(i == "#") for i in line[0][1:-1]], dtype=int)
    jolt = np.array([int(i) for i in line[-1][1:-1].split(",")], dtype=int)

    num_switches = len(line) - 2
    switch_mat = np.zeros((len(jolt), num_switches), dtype=int)
    for v, s in enumerate(line[1:-1]):
        s = s[1:-1].split(",")
        for i in s:
            switch_mat[int(i)][v] = 1

    on_best = float("inf")
    for i in product([0, 1], repeat=num_switches):
        i = np.array(i)
        presses = i.sum()
        if presses >= on_best:
            continue
        if ((switch_mat @ i) % 2 == on).all():
            on_best = min(on_best, presses)
    p1_presses += on_best

    # i learned this framework in my linear programming class!
    var = cp.Variable(num_switches, integer=True)
    objective = cp.Minimize(var.T @ np.ones(num_switches))
    constraints = [switch_mat @ var == jolt, var >= 0]
    problem = cp.Problem(objective, constraints)
    res = problem.solve()
    p2_presses += round(res)

print(f"ok yesterday could still have been a skill issue: {p1_presses}")
print(f"but part 2 being literally just ILP is kinda bs: {p2_presses}")
