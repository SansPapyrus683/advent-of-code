import sys

directions = [l.strip() for l in sys.stdin]

p1pos = [0, 0]
p2pos = [0, 0]
orientations = [
    lambda p, a: [p[0] + a, p[1]],
    lambda p, a: [p[0], p[1] - a],
    lambda p, a: [p[0] - a, p[1]],
    lambda p, a: [p[0], p[1] + a],
]
orient = 0
waypoint = [10, 1]

for d in directions:
    command = d[0]
    arg = int(d[1:])

    if command == "N":
        p1pos[1] += arg
        waypoint[1] += arg
    elif command == "S":
        p1pos[1] -= arg
        waypoint[1] -= arg
    elif command == "E":
        p1pos[0] += arg
        waypoint[0] += arg
    elif command == "W":
        p1pos[0] -= arg
        waypoint[0] -= arg
    elif command == "R":
        assert (
            arg % 90 == 0
        ), "for the sake of simplicity rotations should be multiple of 90 lol"
        orient = (orient + arg // 90) % 4
        for _ in range(arg // 90):
            waypoint = [waypoint[1], -waypoint[0]]
    elif command == "L":
        assert (
            arg % 90 == 0
        ), "for the sake of simplicity rotations should be multiple of 90 lol"
        orient = (orient - arg // 90) % 4
        for _ in range(arg // 90):
            waypoint = [-waypoint[1], waypoint[0]]
    elif command == "F":
        p1pos = orientations[orient](p1pos, arg)
        for _ in range(arg):
            p2pos[0] += waypoint[0]
            p2pos[1] += waypoint[1]

print(
    f"you'd think i'd get faster with all these coordinate problems: {abs(p1pos[0]) + abs(p1pos[1])}"
)
print(
    f"man these instructions are REALLY disorienting: {abs(p2pos[0]) + abs(p2pos[1])}"
)
