from enum import Enum

DIM = 50
WALL = "#"
WRAP = " "


class Dir(Enum):
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

    def right(self) -> "Dir":
        return Dir((self.value + 1) % len(Dir))

    def left(self) -> "Dir":
        return Dir((self.value - 1) % len(Dir))

    def back(self) -> "Dir":
        return self.right().right()


def neighbors(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def password(pos: tuple[int, int], face: Dir) -> int:
    return pos[0] * 1000 + pos[1] * 4 + face.value


with open("xmas_lights.txt") as read:
    grid, directions = read.read().split("\n\n")
    grid = [WRAP + r for r in grid.split("\n")]
    directions = directions.strip()

max_len = max(len(r) for r in grid)
for i in range(len(grid)):
    if len(grid[i]) < max_len + 1:
        grid[i] += WRAP * (max_len - len(grid[i]) + 1)
grid.insert(0, WRAP * (max_len + 1))
grid.append(WRAP * (max_len + 1))

p1_wrap = {}
for r in range(len(grid)):
    for c in range(len(grid[r])):
        if grid[r][c].isspace():
            continue

        for n in neighbors(r, c):
            if not grid[n[0]][n[1]].isspace():
                continue

            dr, dc = n[0] - r, n[1] - c
            p1_pos = (r, c)
            while not grid[p1_pos[0]][p1_pos[1]].isspace():
                p1_pos = (p1_pos[0] - dr, p1_pos[1] - dc)
            p1_pos = (p1_pos[0] + dr, p1_pos[1] + dc)
            p1_wrap[((r, c), n)] = p1_pos

parsed_dirs = []
p1_pos = ""
for c in directions:
    if c.isdigit():
        p1_pos += c
    else:
        parsed_dirs.append(int(p1_pos))
        parsed_dirs.append(c)
        p1_pos = ""
if p1_pos:
    parsed_dirs.append(int(p1_pos))

start = None
for r in range(len(grid[1])):
    if grid[1][r] != WRAP:
        start = (1, r)
        break
assert start is not None

dir_ = Dir.RIGHT
p1_pos = start
for d in parsed_dirs:
    if type(d) == int:
        delta = dir_.delta()
        for _ in range(d):
            n = (p1_pos[0] + delta[0], p1_pos[1] + delta[1])
            if grid[n[0]][n[1]] == WRAP:
                poss = p1_wrap[(p1_pos, n)]
                if grid[poss[0]][poss[1]] == WALL:
                    break
                p1_pos = poss
            elif grid[n[0]][n[1]] == WALL:
                break
            else:
                p1_pos = n
    else:
        dir_ = dir_.right() if d == "R" else dir_.left()

print(f"p1 pw: {password(p1_pos, dir_)}")

# yeah.
p2_wrap = {}
for i in range(DIM):
    p2_wrap[(1 + 2 * DIM, 1 + i, Dir.UP)] = (1 + DIM + i, 1 + DIM, Dir.RIGHT)
    p2_wrap[(1 + 2 * DIM + i, 1, Dir.LEFT)] = (DIM - i, 1 + DIM, Dir.RIGHT)
    p2_wrap[(1 + 3 * DIM + i, 1, Dir.LEFT)] = (1, 1 + DIM + i, Dir.DOWN)
    p2_wrap[(4 * DIM, 1 + i, Dir.DOWN)] = (1, 1 + 2 * DIM + i, Dir.DOWN)
    p2_wrap[(3 * DIM, 1 + DIM + i, Dir.DOWN)] = (1 + 3 * DIM + i, DIM, Dir.LEFT)
    p2_wrap[(1 + 2 * DIM + i, 2 * DIM, Dir.RIGHT)] = (DIM - i, 3 * DIM, Dir.LEFT)
    p2_wrap[(1 + DIM + i, 2 * DIM, Dir.RIGHT)] = (DIM, 1 + 2 * DIM + i, Dir.UP)

for a, b in list(p2_wrap.items()):
    p2_wrap[b[:-1] + (b[-1].back(),)] = a[:-1] + (a[-1].back(),)

dir_ = Dir.RIGHT
p2_pos = start
for d in parsed_dirs:
    if type(d) == int:
        for _ in range(d):
            delta = dir_.delta()
            assert grid[p2_pos[0]][p2_pos[1]] != WRAP
            n = (p2_pos[0] + delta[0], p2_pos[1] + delta[1])
            if grid[n[0]][n[1]] == WRAP:
                n_r, n_c, n_dir = p2_wrap[(*p2_pos, dir_)]
                if grid[n_r][n_c] == WALL:
                    break
                p2_pos = n_r, n_c
                dir_ = n_dir
            elif grid[n[0]][n[1]] == WALL:
                break
            else:
                p2_pos = n
        # print(p2_pos[1] - 1, p2_pos[0] - 1, dir_)
    else:
        dir_ = dir_.right() if d == "R" else dir_.left()

print(f"p2 pw: {password(p2_pos, dir_)}")
