import sys
from dataclasses import dataclass


@dataclass
class Fold:
    axis_y: bool  # True if along the y axis, False if x
    num: int


points = set()
instructions = []
reading_points = True
for l in sys.stdin:
    if l == "\n":
        reading_points = False
        continue

    if reading_points:
        points.add(tuple(int(i) for i in l.split(",")))
    else:
        l = l.replace("fold along ", "").split("=")
        axis_y = l[0] == "y"
        num = int(l[1])
        instructions.append(Fold(axis_y, num))

first = True
for i in instructions:
    new_points = set()
    for p in points:
        if i.axis_y:
            new_points.add((p[0], p[1] if p[1] < i.num else i.num - (p[1] - i.num)))
        else:
            new_points.add((p[0] if p[0] < i.num else i.num - (p[0] - i.num), p[1]))

    points = new_points
    if first:
        print(f"this is the worst manual ever written jesus: {len(points)}")
        first = False

max_x = max(p[0] for p in points)
max_y = max(p[1] for p in points)
final = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
for p in points:
    final[p[1]][p[0]] = "█"

print("but anyways here's the code, i hope you're happy")
for r in final:
    print("".join(r))
