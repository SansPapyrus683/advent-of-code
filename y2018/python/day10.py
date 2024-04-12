import re

EMPTY = " "
FILLED = "█"
THRESHOLD = 80  # results may vary

light_fmt = r"position=<(\-?\d+),(\-?\d+)>velocity=<(\-?\d+),(\-?\d+)>"
lights = []
with open("input/day10.txt") as read:
    for light in read.readlines():
        light = "".join(c for c in light if not c.isspace())
        light = [int(i) for i in next(iter(re.findall(light_fmt, light)))]
        lights.append([(light[0], light[1]), (light[2], light[3])])

time = 0
while True:
    for l in lights:
        l[0] = (l[0][0] + l[1][0], l[0][1] + l[1][1])

    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")
    for p, _ in lights:
        min_x = min(min_x, p[0])
        max_x = max(max_x, p[0])
        min_y = min(min_y, p[1])
        max_y = max(max_y, p[1])

    time += 1
    if max_y - min_y < THRESHOLD and max_x - min_x < THRESHOLD:
        # might produce a lot of output, just scroll through until you're done
        grid = [
            [EMPTY for _ in range(max_x - min_x + 1)]
            for _ in range(max_y - min_y + 1)
        ]
        for p, _ in lights:
            grid[p[1] - min_y][p[0] - min_x] = FILLED

        print(f"curr time: {time}")
        for r in grid:
            print("".join(r))

