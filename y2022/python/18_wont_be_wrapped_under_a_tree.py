import sys
from collections import deque


def sides(x: int, y: int, z: int) -> list[tuple[int, int, int]]:
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


lava = []
for i in sys.stdin:
    lava.append(tuple(int(j) for j in i.split(',')))

lava = set(tuple(c) for c in lava)
bound = max(max(c) for c in lava) + 1

io_area = 0
o_area = 0
outside = set()
inside = set()
for c in lava:
    for s in sides(*c):
        io_area += s not in lava
        if s in lava or s in inside:
            continue

        frontier = deque([s])
        visited = set()
        while frontier:
            curr = frontier.popleft()
            if any(i == bound for i in curr) or curr in outside:
                outside.update(visited)
                o_area += 1
                break
            for n in sides(*curr):
                if n not in visited and n not in lava:
                    visited.add(n)
                    frontier.append(n)
        else:
            inside.update(visited)

print(f"area including outside & inside: {io_area}")
print(f"area but it's just the outside: {o_area}")
