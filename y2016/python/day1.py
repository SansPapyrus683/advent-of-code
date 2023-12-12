import enum
import numpy as np


class Direction(enum.Enum):
    NORTH = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()
    WEST = enum.auto()

    def right(self):
        if self == self.NORTH:
            return self.EAST
        elif self == self.SOUTH:
            return self.WEST
        elif self == self.EAST:
            return self.SOUTH
        elif self == self.WEST:
            return self.NORTH

    def left(self):
        if self == self.NORTH:
            return self.WEST
        elif self == self.SOUTH:
            return self.EAST
        elif self == self.EAST:
            return self.NORTH
        elif self == self.WEST:
            return self.SOUTH


POS_CHANGE = {
    Direction.NORTH: np.array([0, 1]),
    Direction.SOUTH: np.array([0, -1]),
    Direction.EAST: np.array([1, 0]),
    Direction.WEST: np.array([-1, 0])
}

with open("input/day1.txt") as read:
    directions = [d.strip() for d in read.readline().split(",")]

at = np.array([0, 0])
visited = {tuple(at)}
curr_dir = Direction.NORTH
dupe_pos = False
for d in directions:
    turn = d[0]
    if turn == "L":
        curr_dir = curr_dir.left()
    elif turn == "R":
        curr_dir = curr_dir.right()

    for _ in range(int(d[1:])):
        at = at + POS_CHANGE[curr_dir]
        if tuple(at) in visited and not dupe_pos:
            print(f"dist of first dupe pos (p2): {np.abs(at).sum()}")
            dupe_pos = True
        visited.add(tuple(at))

print(f"bunny hq dist (p1): {np.abs(at).sum()}")
