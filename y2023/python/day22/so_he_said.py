from itertools import product

Cube = list[tuple[int, int, int]]


def sim_bricks(bricks: list[Cube]) -> tuple[list[Cube], int]:
    for i in range(len(bricks)):
        bricks[i] = [list(c) for c in bricks[i]]

    fallen = set()
    process = True
    while process:
        process = False
        occupied = set()
        for b in bricks:
            occupied.update(tuple(c) for c in b)

        for bi, b in enumerate(bricks):
            can_fall = True
            for c in b:
                down = [c[0], c[1], c[2] - 1]
                if c[2] == 1 or (down not in b and tuple(down) in occupied):
                    can_fall = False
                    break

            if can_fall:
                process = True
                fallen.add(bi)
                for c in b:
                    c[2] -= 1

    for b in bricks:
        for i in range(len(b)):
            b[i] = tuple(b[i])

    return bricks, len(fallen)


bricks = []
with open("lets_run.txt") as read:
    for br in read.readlines():
        s, e = [[int(x) for x in r.split(",")] for r in br.split("~")]
        bricks.append(list(product(*[range(s[i], e[i] + 1) for i in range(3)])))

bricks, _ = sim_bricks(bricks)

print("this is gonna take a while, so check ur email or smth")
can_zap = 0
unstable_sum = 0
for i in range(len(bricks)):
    removed, fall_num = sim_bricks(bricks[:i] + bricks[i + 1:])
    if fall_num == 0:
        can_zap += 1
    else:
        unstable_sum += fall_num

print(f"thanks for your patience: {can_zap}")
print(f"i'll get around to optimizing this sol sometime never: {unstable_sum}")
