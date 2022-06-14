# DISCLAIMER: really slow, probably a better way but idk

P2_MAX_DIST = 10 ** 4

points = []
min_x = float('inf')
max_x = 0
min_y = float('inf')
max_y = 0
with open('day6.txt') as read:
    for p in read.readlines():
        x, y = [int(i) for i in p.split(',')]
        assert x >= 0 and y >= 0

        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        points.append((x, y))

area = [[-1 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
occ_amt = [0 for _ in range(len(points))]
for x in range(max_x + 1):
    for y in range(max_y + 1):
        min_dist = float('inf')

        distances = []
        for p in points:
            distances.append(abs(p[0] - x) + abs(p[1] - y))

        closest = min(distances)
        if distances.count(closest) == 1:
            area[x][y] = distances.index(closest)

        if area[x][y] != -1:
            occ_amt[area[x][y]] += 1

# -1 might be in this set but it doesn't matter
inf_area = set()
for x in range(min_x, max_x + 1):
    inf_area.add(area[x][min_y])
    inf_area.add(area[x][max_y])
for y in range(min_y, max_y + 1):
    inf_area.add(area[min_x][y])
    inf_area.add(area[max_x][y])

max_area = 0
for v, p in enumerate(points):
    if v not in inf_area:
        max_area = max(max_area, occ_amt[area[p[0]][p[1]]])

print(f"largest area: {max_area}")

close_enough_amt = 0
check_dist = P2_MAX_DIST // len(points) + 1
for x in range(min_x - check_dist, max_x + check_dist):
    for y in range(min_y - check_dist, max_y + check_dist):
        total_dist = sum(
            abs(p[0] - x) + abs(p[1] - y) for p in points
        )
        close_enough_amt += total_dist < P2_MAX_DIST

print(f"area of \"close enough\" region: {close_enough_amt}")
