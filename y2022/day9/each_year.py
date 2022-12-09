DIRECTIONS = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}
P1_LEN = 2
P2_LEN = 10


def sign(n: int) -> int:
    if n == 0:
        return 0
    return -1 if n < 0 else 1


def move_rope(rope: list[tuple[int, int]], delta: tuple[int, int]):
    def valid_neighbors(x: int, y: int) -> list[tuple[int, int]]:
        """returns all the valid places a succeeding knot can be"""
        return [
            (x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1), (x - 1, y - 1)
        ]

    head = rope[0]
    rope[0] = (head[0] + delta[0], head[1] + delta[1])
    prev = head
    for v, knot in enumerate(rope):
        neigh = list(valid_neighbors(*prev))
        if tuple(knot) not in neigh:
            dx = prev[0] - knot[0]
            dy = prev[1] - knot[1]
            new_knot = (knot[0] + sign(dx), knot[1] + sign(dy))
        else:
            new_knot = knot
        knot = new_knot
        rope[v] = knot
        prev = knot


moves = []
with open("i_ask_for_alot.txt") as read:
    for i in read.readlines():
        dir_, mag = i.split()
        moves.append((dir_, int(mag)))

start = (0, 0)
p1_visited = {start}
p2_visited = {start}
p1_rope = [start for _ in range(P1_LEN)]
p2_rope = [start for _ in range(P2_LEN)]
for dir_, mag in moves:
    change = DIRECTIONS[dir_]
    for _ in range(mag):
        move_rope(p1_rope, change)
        p1_visited.add(p1_rope[-1])
        move_rope(p2_rope, change)
        p2_visited.add(p2_rope[-1])


print(f"god, today was abysmal: {len(p1_visited)}")
print(f"didn't even manage top 500 for p1 or p2: {len(p2_visited)}")
