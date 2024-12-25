import sys

ROW_NUM = 7
COL_NUM = 5

keys = []
locks = []
for group in sys.stdin.read().split("\n\n"):
    group = group.split()
    assert len(group) == ROW_NUM and all(len(r) == COL_NUM for r in group)
    if "." not in group[0]:
        locks.append(group)
    else:
        keys.append(group)

fit_pairs = 0
for k in keys:
    for l in locks:
        fit = True
        for r in range(ROW_NUM):
            for c in range(COL_NUM):
                if k[r][c] == l[r][c] == "#":
                    fit = False
                    break
            if not fit:
                break
        fit_pairs += fit

print(f"no lb lmao. it is what it is {fit_pairs}")
