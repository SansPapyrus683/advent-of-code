import sys

WALL = "#"


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def blizz_move(blizzard: list[list[list[str]]]) -> list[list[list[str]]]:
    ret = [[[] for _ in range(len(blizzard[0]))] for _ in range(len(blizzard))]
    for r in range(len(blizzard)):
        for c in range(len(blizzard[r])):
            for b in blizzard[r][c]:
                match b:
                    case "^":
                        ret[len(blizzard) - 2 if r == 1 else r - 1][c].append(b)
                    case "v":
                        ret[1 if r == len(blizzard) - 2 else r + 1][c].append(b)
                    case "<":
                        ret[r][len(blizzard[0]) - 2 if c == 1 else c - 1].append(b)
                    case ">":
                        ret[r][1 if c == len(blizzard[0]) - 2 else c + 1].append(b)
                    case _:
                        raise ValueError(f"unknown blizzard type: {b}")
    return ret


valley = [i.strip() for i in sys.stdin]
assert len({len(r) for r in valley}) == 1

# shorthands
r_num = len(valley)
c_num = len(valley[0])

blizz = [[[] for _ in range(c_num)] for _ in range(r_num)]
walls = set()
for r in range(r_num):
    for c in range(c_num):
        if valley[r][c] == WALL:
            walls.add((r, c))
        elif valley[r][c] in "^v<>":
            blizz[r][c].append(valley[r][c])

start = 0, 1
end = r_num - 1, c_num - 2
frontier = {start}
minutes = 0
# yes, this bfs is copied 3 times.
while end not in frontier:
    blizz = blizz_move(blizz)
    next_up = set()

    for r, c in frontier:
        for n in neighbors4(r, c, r_num, c_num) + [(r, c)]:
            if n not in walls and not blizz[n[0]][n[1]]:
                next_up.add(n)

    frontier = next_up
    minutes += 1

print(f"amt of time to get to end: {minutes}")

frontier = {end}
while start not in frontier:
    blizz = blizz_move(blizz)
    next_up = set()

    for r, c in frontier:
        for n in neighbors4(r, c, r_num, c_num) + [(r, c)]:
            if n not in walls and not blizz[n[0]][n[1]]:
                next_up.add(n)

    frontier = next_up
    minutes += 1

frontier = {start}
while end not in frontier:
    blizz = blizz_move(blizz)
    next_up = set()

    for r, c in frontier:
        for n in neighbors4(r, c, r_num, c_num) + [(r, c)]:
            if n not in walls and not blizz[n[0]][n[1]]:
                next_up.add(n)

    frontier = next_up
    minutes += 1

print(f"amt of time to get to end, start, & end again: {minutes}")
