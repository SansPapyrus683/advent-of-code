import numpy as np

DIST = 3

pts = []
with open('input/day25.txt') as read:
    for c in read.readlines():
        pts.append(np.array([int(i) for i in c.split(',')]))
pts = np.array(pts)

visited = [False for _ in range(len(pts))]
constellation_num = 0
for i in range(len(pts)):
    if visited[i]:
        continue

    visited[i] = True
    frontier = [i]
    while frontier:
        curr = frontier.pop()
        for v, p in enumerate(pts):
            if not visited[v] and np.abs(p - pts[curr]).sum() <= DIST:
                visited[v] = True
                frontier.append(v)

    constellation_num += 1

print(f"total number of constellations: {constellation_num}")
