from enum import Enum


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def delta(self) -> tuple[int, int]:
        if self == self.RIGHT:
            return 0, 1
        elif self == self.DOWN:
            return 1, 0
        elif self == self.LEFT:
            return 0, -1
        elif self == self.UP:
            return -1, 0

    def right(self) -> "Direction":
        return Direction((self.value + 1) % len(Direction))

    def left(self) -> "Direction":
        return Direction((self.value - 1) % len(Direction))


def neighbors(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def password(position: tuple[int, int], dir: Direction):
    return position[0] * 1000 + position[1] * 4 + dir.value


with open("input.txt") as read:
    grid, directions = read.read().split("\n\n")
    grid = [" " + r for r in grid.split("\n")]
    directions = directions.strip()

max_len = max(len(r) for r in grid)
for i in range(len(grid)):
    if len(grid[i]) < max_len + 1:
        grid[i] += " " * (max_len - len(grid[i]) + 1)

grid.insert(0, " " * (max_len + 1))
grid.append(" " * (max_len + 1))

start = None
for r in range(len(grid[1])):
    if grid[1][r] != " ":
        start = (1, r)

parsed_dirs = []
curr = ""
for c in directions:
    if c.isdigit():
        curr += c
    else:
        parsed_dirs.append(int(curr))
        parsed_dirs.append(c)
        curr = ""
if curr:
    parsed_dirs.append(int(curr))

b_space_next = {}
for r in range(len(grid)):
    for c in range(len(grid[r])):
        if grid[r][c].isspace():
            continue
        
        for n in neighbors(r, c):
            if not grid[n[0]][n[1]].isspace():
                continue

            dr, dc = n[0] - r, n[1] - c
            curr = (r, c)
            while not grid[curr[0]][curr[1]].isspace():
                curr = (curr[0] - dr, curr[1] - dc)
            curr = (curr[0] + dr, curr[1] + dc)
            b_space_next[((r, c), n)] = curr

direction = Direction.RIGHT
curr = start
for d in parsed_dirs:
    if type(d) == int:
        delta = direction.delta()
        for _ in range(d):
            n = (curr[0] + delta[0], curr[1] + delta[1])
            if grid[n[0]][n[1]] == " ":
                poss = b_space_next[(curr, n)]
                if grid[poss[0]][poss[1]] == "#":
                    break
                curr = poss
            elif grid[n[0]][n[1]] == "#":
                break
            else:
                curr = n
    else:
        if d == "L":
            direction = direction.left()
        elif d == "R":
            direction = direction.right()

print(password(curr, direction))
