import re
import numpy as np
from water import Tile, TILE_STR  # TILE_STR is for debugging

# like always, positions are in (row, col) format
WATER = (0, 500)

xy_fmt = r'x=(\d+),\s+y=(\d+)\.\.(\d+)'
yx_fmt = r'y=(\d+),\s+x=(\d+)\.\.(\d+)'
clay = set()
with open('day17.txt') as read:
    for c in read.readlines():
        if re.match(xy_fmt, c) is not None:
            x, ys, ye = map(int, next(iter(re.findall(xy_fmt, c))))
            for y in range(ys, ye + 1):
                clay.add((y, x))
        elif re.match(yx_fmt, c) is not None:
            y, xs, xe = map(int, next(iter(re.findall(yx_fmt, c))))
            for x in range(xs, xe + 1):
                clay.add((y, x))

min_r = WATER[0]
max_r = WATER[0]
min_c = WATER[1]
max_c = WATER[1]
for r, c in clay:
    min_r = min(min_r, r)
    max_r = max(max_r, r)
    min_c = min(min_c, c)
    max_c = max(max_c, c)

"""
the extra 1 row is so i don't have to do bounds checking
the extra 2 columns are because water can flow right on the edge of the grid
"""
grid = np.empty((max_r - min_r + 2, max_c - min_c + 3), dtype=Tile)
grid.fill(Tile.SAND)
for r, c in clay:
    grid[r - min_r, c - min_c + 1] = Tile.CLAY

# algorithm sauce: https://www.michaelfogleman.com/aoc18/#17
blocking = [Tile.CLAY, Tile.STILL]
# position, (true = falling water, false = spreading water)
todo = [(WATER[0] - min_r, WATER[1] - min_c + 1, True)]
seen = set()
while todo:
    r, c, type_ = todo.pop()
    if (r, c, type_) in seen:
        continue
    seen.add((r, c, type_))
    if type_:
        while r <= max_r and grid[r + 1, c] not in blocking:
            grid[r, c] = Tile.FLOW
            r += 1
        if r <= max_r:
            grid[r, c] = Tile.FLOW
            todo.append((r, c, False))
    else:
        c_left = c
        while (grid[r + 1, c_left] in blocking
               and grid[r, c_left - 1] != Tile.CLAY):
            c_left -= 1

        c_right = c
        while (grid[r + 1, c_right] in blocking
               and grid[r, c_right + 1] != Tile.CLAY):
            c_right += 1

        left_wall = grid[r, c_left - 1] == Tile.CLAY
        right_wall = grid[r, c_right + 1] == Tile.CLAY
        if left_wall and right_wall:
            for fill_c in range(c_left, c_right + 1):
                grid[r, fill_c] = Tile.STILL
            if r != 0:
                todo.append((r - 1, c, False))
        else:
            for fill_c in range(c_left, c_right + 1):
                grid[r, fill_c] = Tile.FLOW
            if not left_wall:
                todo.append((r, c_left, True))
            if not right_wall:
                todo.append((r, c_right, True))

highest_clay = np.where(grid == Tile.CLAY)[0][0]
flowing = (grid == Tile.FLOW).sum() - highest_clay
still = (grid == Tile.STILL).sum()
print(f"total water (while flowing): {flowing + still}")
print(f"total water (after flowing stops): {still}")
