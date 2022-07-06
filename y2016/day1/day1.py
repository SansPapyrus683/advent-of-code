import numpy as np
from directions import Direction

POS_CHANGE = {
    Direction.NORTH: np.array([0, 1]),
    Direction.SOUTH: np.array([0, -1]),
    Direction.EAST: np.array([1, 0]),
    Direction.WEST: np.array([-1, 0])
}

with open("day1.txt") as read:
    directions = [d.strip() for d in read.readline().split(",")]

at = np.array([0, 0])
visited = {tuple(at)}
curr_dir = Direction.NORTH
dupe_pos = False
for d in directions:
    turn = d[0]
    if turn == 'L':
        curr_dir = curr_dir.left()
    elif turn == 'R':
        curr_dir = curr_dir.right()

    for _ in range(int(d[1:])):
        at = at + POS_CHANGE[curr_dir]
        if tuple(at) in visited and not dupe_pos:
            print(f"dist of first dupe pos (p2): {np.abs(at).sum()}")
            dupe_pos = True
        visited.add(tuple(at))

print(f"bunny hq dist (p1): {np.abs(at).sum()}")
