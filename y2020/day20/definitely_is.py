"""
Tiles at the edge of the image also have this border, but the outermost edges won't line up with any other tiles.
^ without this, i'd probably die lol
"""
import re
from math import sqrt
import numpy as np


def line_up(edge1: list[list[str]], edge2: list[list[str]]) -> int:
    """
    returns 0 if they can't line up at all
    returns 1 if the first edge pair of edge1 is valid
    and 2 if the second edge pair is valid
    """
    other_edges = edge2[0] + edge2[1]
    for e in edge1[0]:
        for other_e in other_edges:
            if e == other_e or e == other_e[::-1]:
                return 1
    for e in edge1[1]:
        for other_e in other_edges:
            if e == other_e or e == other_e[::-1]:
                return 2
    return 0


def vertical_neighbors(side: int, r: int, c: int) -> list[list[int]]:
    return [p for p in [[r + 1, c], [r - 1, c]] if 0 <= p[0] < side]


def horizontal_neighbors(side: int, r: int, c: int) -> list[list[int]]:
    return [p for p in [[r, c + 1], [r, c - 1]] if 0 <= p[1] < side]


def neighbors(side: int, r: int, c: int) -> list[list[int]]:
    return vertical_neighbors(side, r, c) + horizontal_neighbors(side, r, c)


def orientations(grid: list[str]) -> list[list[str]]:
    """
    gives all possible ways a tile can be in
    copied from https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
    """
    possible = []
    rotated = grid.copy()
    for _ in range(4):
        possible.append(rotated)
        rotated = list(''.join(r) for r in zip(*rotated[::-1]))

    rotated = [r for r in reversed(grid)]
    for _ in range(4):
        possible.append(rotated)
        rotated = list(''.join(r) for r in zip(*rotated[::-1]))

    rotated = [r[::-1] for r in grid]
    for _ in range(4):
        possible.append(rotated)
        rotated = list(''.join(r) for r in zip(*rotated[::-1]))
    return possible


tiles = {}
with open('staying_up.txt') as read:
    for raw_tile in read.read().split('\n\n'):
        raw_tile = raw_tile.strip().split('\n')
        tile = []
        tiles[int(''.join(c for c in raw_tile[0] if c.isdigit()))] = raw_tile[1:]
    side_len = int(sqrt(len(tiles)))
    assert side_len == sqrt(len(tiles)), 'just please give me a square'

edges = {}
for t_id, tile in tiles.items():
    edges[t_id] = [[tile[0], tile[-1]], [''.join(r[0] for r in tile), ''.join(r[-1] for r in tile)]]

adj_ids = {}
prod = 1
start = -1
for id1, tile1 in edges.items():
    adj_ids[id1] = [[], []]
    matches = []
    for id2, tile2 in edges.items():
        if id1 == id2:
            continue
        result = line_up(tile1, tile2)
        if result != 0:
            matches.append(result)
            adj_ids[id1][result - 1].append(id2)
    # only matches 2, so it must be a corner piece
    if sorted(matches) == [1, 2]:
        start = id1  # idk, just assign a random corner for our start
        prod *= id1
assert start != -1, "there's gotta be a corner bro"
print(f"this is the worst camera design ever made in the history of mankind: {prod}")

pic_ids = np.full((side_len, side_len), -1)
pic_ids[0][0] = start
frontier = [[[0, 0], start]]
while frontier:  # first build the picture out of pure IDs
    curr = frontier.pop(0)
    up_down, left_right = [set(i) for i in adj_ids[curr[-1]]]
    row, col = curr[0]
    v_neighbors = vertical_neighbors(side_len, row, col)
    h_neighbors = horizontal_neighbors(side_len, row, col)
    for vn in v_neighbors:
        val = pic_ids[vn[0]][vn[1]]
        if val != -1 and val not in up_down:
            up_down, left_right = left_right, up_down
            break

    # clear out the ones that've alr been processed, then fill in the undone ones
    for vr, vc in v_neighbors:
        if pic_ids[vr, vc] != -1:
            up_down.remove(pic_ids[vr, vc])
    for vr, vc in v_neighbors:
        if pic_ids[vr, vc] == -1:
            pic_ids[vr, vc] = up_down.pop()
            frontier.append([[vr, vc], pic_ids[vr, vc]])

    for hr, hc in h_neighbors:
        if pic_ids[hr, hc] != -1:
            left_right.remove(pic_ids[hr, hc])
    for hr, hc in h_neighbors:
        if pic_ids[hr, hc] == -1:
            pic_ids[hr, hc] = left_right.pop()
            frontier.append([[hr, hc], pic_ids[hr, hc]])

# try all the starting orientations because we don't really know which one it is
for start_o in orientations(tiles[pic_ids[0, 0]]):
    try:
        actual_pic = [[None for _ in range(side_len)] for _ in range(side_len)]
        actual_pic[0][0] = start_o
        for r in range(side_len):
            for c in range(side_len):
                if actual_pic[r][c] is not None:  # just to handle (0, 0)
                    continue
                this_tile = tiles[pic_ids[r][c]]
                filled_alr = [p for p in neighbors(side_len, r, c) if actual_pic[p[0]][p[1]] is not None].pop()
                tile = actual_pic[filled_alr[0]][filled_alr[1]]
                if filled_alr[0] != r:  # it's upwards
                    match_up = tile[-1]
                    for o in orientations(this_tile):
                        if o[0] == match_up:
                            actual_pic[r][c] = o
                            break

                else:  # it's to the left of the thing
                    match_up = ''.join(r[-1] for r in tile)
                    for o in orientations(this_tile):
                        if ''.join(r[0] for r in o) == match_up:
                            actual_pic[r][c] = o
                            break
        break  # wow, everything matched up!
    except IndexError:  # well, that starting orientation wasn't valid, let's try another
        pass

final = []
for big_r in actual_pic:
    for i in range(1, len(big_r[0]) - 1):  # exclude the top & bottom borders
        final.append(''.join(r[i][1:-1] for r in big_r))

nessie = [
    "..................#.",  # the ending dots are so the bodyLen is consistent
    "#....##....##....###",
    ".#..#..#..#..#..#..."
]
body_len = len(nessie[0])
for o in orientations(final):
    part_of_nessie = np.zeros((len(final), len(final[0])))
    nessie_count = 0
    for i in range(len(final) - len(nessie) + 1):
        for s in range(len(o[0]) - body_len + 1):
            for v, r in enumerate(o[i:i + len(nessie)]):
                r = r[s: s + body_len]
                if re.match(nessie[v], r) is None:
                    break
            else:
                for v1 in range(len(nessie)):
                    for v2 in range(body_len):
                        part_of_nessie[i + v1][s + v2] = nessie[v1][v2] == '#'
                nessie_count += 1
    if nessie_count:  # let's assume there's only ONE valid orientation
        final = o
        break

rough = 0
for r in range(len(final)):
    for c in range(len(final[0])):
        rough += not part_of_nessie[r][c] and final[r][c] == '#'
print(f"i can't believe this took 200 lines of code: {rough}")
