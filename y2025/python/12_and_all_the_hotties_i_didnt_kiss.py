import sys
import numpy as np

DIM = 3  # all presents are 3x3

chunks = [c.strip().split("\n") for c in sys.stdin.read().split("\n\n")]

queries = chunks.pop()

presents = {}
for c in chunks:
    id_ = int(c[0][:-1])
    presents[id_] = np.array([[c == "#" for c in r] for r in c[1:]])

p_area = {id_: p.sum() for id_, p in presents.items()}

valid_regions = 0
for q in queries:
    dims, use = q.split(": ")
    width, height = [int(i) for i in dims.split("x")]

    area = 0
    count = 0
    for v, amt in enumerate(use.split()):
        amt = int(amt)
        count += amt
        area += amt * p_area[v]

    if area <= width * height:
        if count <= (width // DIM) * (height // DIM):
            valid_regions += 1
        else:
            print(f"yeah idk about this region: {q}")

print(f"GENUINE 0/10 PROBLEM WHAT: {valid_regions}")
