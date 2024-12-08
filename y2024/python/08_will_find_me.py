import sys

grid = [row.strip() for row in sys.stdin]

antennas = {}
for r in range(len(grid)):
    for c in range(len(grid[0])):
        cell = grid[r][c]
        if cell == ".":
            continue
        if cell not in antennas:
            antennas[cell] = []
        antennas[cell].append((r, c))

p1_anti = set()
p2_anti = set()
for points in antennas.values():
    for i in range(len(points)):
        for j in range(len(points)):
            if i == j:
                continue

            dr = points[j][0] - points[i][0]
            dc = points[j][1] - points[i][1]

            mul = 0
            at = points[j]
            while 0 <= at[0] < len(grid) and 0 <= at[1] < len(grid[0]):
                p2_anti.add(at)
                if mul == 1:
                    p1_anti.add(at)

                mul += 1
                at = points[j][0] + dr * mul, points[j][1] + dc * mul

print(f"ok first ACTUALLY bad day: {len(p1_anti)}")
print(f"strangely enough most of the stress comes from *thinking about aoc*: {len(p2_anti)}")
