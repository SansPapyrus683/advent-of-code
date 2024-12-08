import sys

UP = -1, 0
DOWN = 1, 0
LEFT = 0, -1
RIGHT = 0, 1

SLASH_MIRROR = {
    RIGHT: UP,
    LEFT: DOWN,
    DOWN: LEFT,
    UP: RIGHT
}
# short for backslash lol
BS_MIRROR = {
    RIGHT: DOWN,
    LEFT: UP,
    DOWN: RIGHT,
    UP: LEFT
}


def num_energized(
        mirrors: list[str], s_at: tuple[int, int], s_d: tuple[int, int]
) -> int:
    if mirrors[s_at[0]][s_at[1]] == "/":
        s_d = SLASH_MIRROR[s_d]
    elif mirrors[s_at[0]][s_at[1]] == "\\":
        s_d = BS_MIRROR[s_d]

    frontier = [(s_at, s_d)]
    visited = [[set() for _ in range(len(mirrors[0]))] for _ in range(len(mirrors))]
    while frontier:
        next_up = []
        for at, d in frontier:
            visited[at[0]][at[1]].add(d)
            nr, nc = at[0] + d[0], at[1] + d[1]
            if not (0 <= nr < len(mirrors) and 0 <= nc < len(mirrors[0])):
                continue

            if mirrors[nr][nc] == "/":
                next_up.append(((nr, nc), SLASH_MIRROR[d]))

            elif mirrors[nr][nc] == "\\":
                next_up.append(((nr, nc), BS_MIRROR[d]))

            elif mirrors[nr][nc] == "|" and d in [RIGHT, LEFT]:
                next_up.append(((nr, nc), DOWN))
                next_up.append(((nr, nc), UP))

            elif mirrors[nr][nc] == "-" and d in [UP, DOWN]:
                next_up.append(((nr, nc), LEFT))
                next_up.append(((nr, nc), RIGHT))

            else:
                next_up.append(((nr, nc), d))

        next_up = [(at, d) for at, d in next_up if d not in visited[at[0]][at[1]]]
        frontier = next_up

    return sum(sum(bool(c) for c in r) for r in visited)


mirrors = [r.strip() for r in sys.stdin]

max_energy = 0
for r in range(len(mirrors)):
    max_energy = max([
        max_energy,
        num_energized(mirrors, (r, 0), RIGHT),
        num_energized(mirrors, (r, len(mirrors[0]) - 1), LEFT)
    ])
for c in range(len(mirrors[0])):
    max_energy = max([
        max_energy,
        num_energized(mirrors, (0, c), DOWN),
        num_energized(mirrors, (len(mirrors) - 1, c), UP)
    ])

print(f"well, no t100 today: {num_energized(mirrors, (0, 0), RIGHT)}")
print(f"but i tried my best and didn't silly anything! {max_energy}")
