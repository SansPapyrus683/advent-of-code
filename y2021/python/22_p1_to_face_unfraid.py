import sys

import numpy as np

RANGE = 50

operations = []
for l in sys.stdin:
    a, b = l.strip().split()
    on = a == "on"
    b = b.split(",")
    b = [x.split("=") for x in b]
    for i in range(len(b)):
        b[i][1] = [int(y) for y in b[i][1].split("..")]
    operations.append([on, np.array([x[1] for x in b])])

min_val = -RANGE
for _, o in operations:
    min_val = min(min_val, RANGE)
for _, o in operations:
    o -= min_val

relevant = np.zeros((RANGE * 2, RANGE * 2, RANGE * 2)).astype(bool)
for val, o in operations:
    x, y, z = o
    # don"t worry if it goes out of range, python handles it just fine (idk how)
    relevant[x[0]:x[1] + 1, y[0]:y[1] + 1, z[0]:z[1] + 1] = val
print(f"lmao another \"oh p1 isn't so bad\" problem: {relevant.sum()}")
