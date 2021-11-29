"""
this is part 2
the two parts of this puzzle follow pretty much exactly
the same logic, so i don't think i have to comment this
"""
from itertools import product
from copy import deepcopy
import numpy as np

SIM_AMT = 6


def neighbors(x: int, y: int, z: int, w: int) -> [(int, int, int, int)]:
    ret = []
    for triplet in product(*([[1, -1, 0]] * 4)):
        ret.append((x + triplet[0], y + triplet[1], z + triplet[2], w + triplet[3]))
    ret.remove((x, y, z, w))
    return ret


# NOTE: indices are referred to in w, z, y, x, not x, y, z, w because of array stuff
with open('many_ways.txt') as read:
    plane = [[int(i == '#') for i in line.rstrip()] for line in read.readlines()]
    assert len(plane) == len(plane[0]), 'can you just give a square as input?'
    arr = np.zeros((1, 1, len(plane), len(plane)))
    arr[0][0] = plane

for _ in range(SIM_AMT):
    w_and_z = len(arr) + 2
    x_and_y = len(arr[0][0]) + 2
    expanded = np.zeros((w_and_z, w_and_z, x_and_y, x_and_y))
    expanded[1:w_and_z - 1, 1:w_and_z - 1, 1:x_and_y - 1, 1:x_and_y - 1] = arr
    arr = expanded

    new_arr = deepcopy(arr)
    for x in range(x_and_y):
        for y in range(x_and_y):
            for z in range(w_and_z):
                for w in range(w_and_z):
                    filled_count = 0
                    for nX, nY, nZ, nW in neighbors(x, y, z, w):
                        if 0 <= nX < x_and_y and 0 <= nY < x_and_y and 0 <= nZ < w_and_z and 0 <= nW < w_and_z:
                            filled_count += arr[nW, nZ, nY, nX]
                    if arr[w, z, y, x] == 1 and filled_count not in [2, 3]:
                        new_arr[w, z, y, x] = 0
                    elif arr[w, z, y, x] == 0 and filled_count == 3:
                        new_arr[w, z, y, x] = 1
    arr = new_arr

print(f"the protag has goddamn ascended to a new level of existence: {int(np.sum(arr))}")
