from collections import defaultdict

Cube = tuple[tuple[int, int, int], tuple[int, int, int]]


def inter(
        a_start: int, a_end: int, b_start: int, b_end: int
) -> tuple[int, int] | None:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return None if start > end else (start, end)


def is_supporting(bot: Cube, top: Cube):
    if bot[1][2] + 1 != top[0][2]:
        return False
    x_inter = inter(bot[0][0], bot[1][0], top[0][0], top[1][0])
    y_inter = inter(bot[0][1], bot[1][1], top[0][1], top[1][1])
    return x_inter is not None and y_inter is not None


with open("lets_run.txt") as read:
    bricks = []
    for br in read.readlines():
        s, e = [tuple(int(x) for x in r.split(",")) for r in br.split("~")]
        bricks.append((s, e))

new_bricks = []
by_height = defaultdict(list)
for curr in sorted(bricks, key=lambda b: b[0][2]):
    curr = list(curr[0]), list(curr[1])
    while curr[0][2] > 1:
        blocked = False
        for b in by_height[curr[0][2] - 1]:
            if is_supporting(b, curr):
                blocked = True
                break

        if not blocked:
            curr[0][2] -= 1
            curr[1][2] -= 1
        else:
            break

    by_height[curr[1][2]].append(curr)
    curr = tuple(curr[0]), tuple(curr[1])
    new_bricks.append(curr)
bricks = new_bricks

on_top = [[] for _ in range(len(bricks))]  # the bricks supporting each brick
supporting = [[] for _ in range(len(bricks))]  # the bricks each brick is supporting
for i, b1 in enumerate(bricks):
    for j, b2 in enumerate(bricks):
        if i != j and is_supporting(b1, b2):
            on_top[j].append(i)
            supporting[i].append(j)

can_remove = set(range(len(bricks)))
for o in on_top:
    if len(o) == 1:
        can_remove.discard(o[0])  # til this method exists

fall_sum = 0
for b in range(len(bricks)):
    if b in can_remove:
        continue

    num_supports = [len(i) for i in on_top]
    to_fall = [b]
    fallen = 0
    while to_fall:
        curr = to_fall.pop()
        for s in supporting[curr]:
            num_supports[s] -= 1
            if num_supports[s] == 0:
                fallen += 1
                to_fall.append(s)
    fall_sum += fallen

print(f"alright it's 12/23 and i finally optimized this: {len(can_remove)}")
print(f"pretty neat problem, if a bit sussy: {fall_sum}")
