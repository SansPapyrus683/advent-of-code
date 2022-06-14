"""
so this is part 1
i first used python lists
then after i discovered the wonders of numpy within about 5 minutes
i cleaned this up with said numpy
"""
from itertools import product
from copy import deepcopy
import numpy as np

SIM_AMT = 6


def neighbors(x: int, y: int, z: int) -> [(int, int, int)]:
    ret = []
    for triplet in product(*([[1, -1, 0]] * 3)):
        ret.append((x + triplet[0], y + triplet[1], z + triplet[2]))
    ret.remove((x, y, z))
    return ret


# NOTE: indices are referred to in z, y, x, not x, y, z because of array stuff
with open('many_ways.txt') as read:
    plane = [[int(i == '#') for i in line.rstrip()] for line in read.readlines()]
    assert len(plane) == len(plane[0]), 'can you just give a square as day1.txt?'
    arr = np.zeros((1, len(plane), len(plane)))
    arr[0] = plane

for _ in range(SIM_AMT):
    new_z = len(arr) + 2
    x_and_y = len(arr[0]) + 2
    expanded = np.zeros((new_z, x_and_y, x_and_y))
    expanded[1:new_z - 1, 1:x_and_y - 1, 1:x_and_y - 1] = arr  # copy the array into the middle of the new one
    arr = expanded

    new_arr = deepcopy(arr)
    for x in range(x_and_y):
        for y in range(x_and_y):
            for z in range(new_z):
                filled_count = 0
                for nX, nY, nZ in neighbors(x, y, z):
                    if 0 <= nX < x_and_y and 0 <= nY < x_and_y and 0 <= nZ < new_z:
                        filled_count += arr[nZ, nY, nX]
                if arr[z, y, x] == 1 and filled_count not in [2, 3]:
                    new_arr[z, y, x] = 0
                elif arr[z, y, x] == 0 and filled_count == 3:
                    new_arr[z, y, x] = 1
    arr = new_arr

print(f"the heck? i thought christmas would go on without me lol: {int(np.sum(arr))}")
