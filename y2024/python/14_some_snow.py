import sys
import re
from itertools import count

P1_TIME = 100
ROWS, COLS = 101, 103


def neighbors8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


robots = []
robot_fmt = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
for r in sys.stdin:
    if res := robot_fmt.match(r):
        robots.append([int(res.group(i)) for i in range(1, 4 + 1)])

quads = [[0, 0], [0, 0]]
for r, c, dr, dc in robots:
    new_r = (r + P1_TIME * dr) % ROWS
    new_c = (c + P1_TIME * dc) % COLS
    if new_r == ROWS // 2 or new_c == COLS // 2:
        continue

    quads[new_r < ROWS // 2][new_c < COLS // 2] += 1

safety = quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1]
print(f"bruh i'm on a plane what am i even supposed to do: {safety}")

rob_pos = [(r[0], r[1]) for r in robots]
for t in count(1):
    for i, (r, c) in enumerate(rob_pos):
        rob_pos[i] = (r + robots[i][2]) % ROWS, (c + robots[i][3]) % COLS
    
    occupied = set(rob_pos)
    if len(occupied) < len(rob_pos):
        continue

    runs = 0
    for r in range(ROWS):
        for c in range(COLS):
            # a stupid heuristic, i'm not even sure if this works for all input
            runs += all((r, c + i) in occupied for i in range(20))
    
    if runs >= 2:
        print(f"robots after {t} steps")
        for r in range(ROWS):
            for c in range(COLS):
                print("█" if (r, c) in occupied else " ", end="")
            print()
        break
