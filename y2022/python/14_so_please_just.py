import sys

START = (500, 0)

walls = []
for rock in sys.stdin:
    rock = [pt.split(",") for pt in rock.split("->")]
    for i in range(len(rock)):
        rock[i] = int(rock[i][0]), int(rock[i][1])
    for i in range(len(rock) - 1):
        walls.append(((rock[i]), rock[i + 1]))

occupied = set()
for p1, p2 in walls:
    if p1[0] == p2[0]:
        for x in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
            occupied.add((p1[0], x))
    else:
        for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
            occupied.add((x, p1[1]))

lowest = max(p[1] for p in occupied)

no_floor_occ = occupied.copy()
particles = 0
while True:
    sand = list(START)
    while sand[1] < lowest:
        if (sand[0], sand[1] + 1) not in no_floor_occ:
            sand[1] += 1
        elif (sand[0] - 1, sand[1] + 1) not in no_floor_occ:
            sand[1] += 1
            sand[0] -= 1
        elif (sand[0] + 1, sand[1] + 1) not in no_floor_occ:
            sand[1] += 1
            sand[0] += 1
        else:
            break

    if sand[1] == lowest:
        break

    particles += 1
    no_floor_occ.add(tuple(sand))

print(f"damn, didn't get top 100: {particles}")

floor = lowest + 2
floor_occ = occupied.copy()
particles = 0
while True:
    sand = list(START)
    while sand[1] != floor - 1:
        if (sand[0], sand[1] + 1) not in floor_occ:
            sand[1] += 1
        elif (sand[0] - 1, sand[1] + 1) not in floor_occ:
            sand[1] += 1
            sand[0] -= 1
        elif (sand[0] + 1, sand[1] + 1) not in floor_occ:
            sand[1] += 1
            sand[0] += 1
        else:
            break

    particles += 1

    if tuple(sand) == START:
        break

    floor_occ.add(tuple(sand))

print(f"but at least simulation wasn't too painful: {particles}")
