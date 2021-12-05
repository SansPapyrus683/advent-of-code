from copy import deepcopy


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Point"):
        if self.x != other.x:
            return self.x < other.x
        return self.y < other.y


def two_cross_num(cross_num: [[int]]) -> int:
    total = 0
    for r in range(len(cross_num)):
        for c in range(len(cross_num[r])):
            total += cross_num[r][c] >= 2
    return total


with open("winter_wonderland.txt") as read:
    wires = []
    for l in read.readlines():
        l = l.strip().split(' -> ')
        wires.append([
            Point(*[int(i) for i in l[0].split(',')]),
            Point(*[int(i) for i in l[1].split(',')])
        ])

# not sure if there's negatives, not gonna take any changes
min_x = min(min(w[0].x, w[1].x) for w in wires)
min_y = min(min(w[0].y, w[1].y) for w in wires)
for w in wires:
    w[0].x -= min_x
    w[1].x -= min_x
    w[0].y -= min_y
    w[1].y -= min_y
max_x = max(max(w[0].x, w[1].x) for w in wires)
max_y = max(max(w[0].y, w[1].y) for w in wires)

straight_crosses = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
for w in wires:
    w.sort()
    if w[0].x == w[1].x:
        for y in range(w[0].y, w[1].y + 1):
            straight_crosses[w[0].x][y] += 1
    elif w[0].y == w[1].y:
        for x in range(w[0].x, w[1].x + 1):
            straight_crosses[x][w[0].y] += 1
print(f"god input for this problem was hell: {two_cross_num(straight_crosses)}")

all_crosses = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
for w in wires:
    x_add = w[1].x - w[0].x
    y_add = w[1].y - w[0].y
    if x_add < 0:
        x_add = -1
    elif x_add > 0:
        x_add = 1

    if y_add < 0:
        y_add = -1
    elif y_add > 0:
        y_add = 1

    curr = deepcopy(w[0])
    while curr != w[1]:
        all_crosses[curr.x][curr.y] += 1
        curr.x += x_add
        curr.y += y_add
    all_crosses[curr.x][curr.y] += 1
print(f"diagonal lines can suck my right finger: {two_cross_num(all_crosses)}")
