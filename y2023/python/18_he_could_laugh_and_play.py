import sys

import numpy as np

DIRS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
DIG_TO_DIR = ["R", "D", "L", "U"]


def shoelace(x_y: list[tuple[int, int]]) -> float:
    """https://stackoverflow.com/a/58515054/12128483"""
    x_y = np.array(x_y)
    x_y = x_y.reshape(-1, 2)
    x = x_y[:, 0]
    y = x_y[:, 1]
    s1 = np.sum(x * np.roll(y, -1))
    s2 = np.sum(y * np.roll(x, -1))
    area = 0.5 * np.absolute(s1 - s2)
    return area


def lagoon_area(digs: list[tuple[str, int]]) -> int:
    at = 0, 0
    dist = 0
    points = [at]
    for d, mag in digs:
        d = DIRS[d]
        at = at[0] + d[0] * mag, at[1] + d[1] * mag
        points.append(at)
        dist += mag / 2
    assert at == (0, 0), "we should end up back where we start"
    return int(shoelace(points) + dist + 1)


dig = []
for i in sys.stdin:
    i = i.split()
    dig.append((i[0], int(i[1]), i[2][2:-1]))

p1_dig = []
p2_dig = []
for p1_dir, p1_mag, p2_info in dig:
    p1_dig.append((p1_dir, p1_mag))
    p2_mag, p2_dir = p2_info[:-1], int(p2_info[-1])
    p2_dig.append((DIG_TO_DIR[p2_dir], int(p2_mag, 16)))

print(f"lmao i inted so hard for p1: {lagoon_area(p1_dig)}")
print(f'tried some "clever" methods before giving up: {lagoon_area(p2_dig)}')
