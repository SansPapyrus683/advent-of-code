import re
from functools import reduce
from operator import mul

START = "in"
ACC = "A"
REJ = "R"
RANGE = (1, 4000)


def group(seq, sep):
    ret = []
    for el in seq:
        if el == sep:
            yield ret
            ret = []
        else:
            ret.append(el)
    yield ret


pt_fmt = r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}"
with open("you_and_me.txt") as read:
    workflow = {}
    parts = []
    for v, g in enumerate(group(read.readlines(), "\n")):
        if v == 0:
            for i in g:
                i = i.strip()
                break_at = i.find("{")
                name = i[:break_at]
                rest = i[break_at + 1:-1].split(",")
                for j in range(len(rest) - 1):
                    rest[j] = rest[j].split(":")
                workflow[name] = rest

        elif v == 1:
            for i in g:
                parts.append([int(a) for a in re.findall(pt_fmt, i)[0]])

frontier = [("in", [])]
acc_reqs = []
while frontier:
    next_up = []
    for i, reqs in frontier:
        if i in [ACC, REJ]:
            if i == ACC:
                acc_reqs.append(reqs)
            continue

        negate = []
        for cond, n in workflow[i][:-1]:
            next_up.append((n, reqs + negate + [cond]))
            cond = cond.translate({ord(">"): "<=", ord("<"): ">="})
            negate.append(cond)

        next_up.append((workflow[i][-1], reqs + negate))

    frontier = next_up

acc_ranges = []
for ar in acc_reqs:
    use_range = {c: list(RANGE) for c in "xmas"}
    for r in ar:
        if "<=" in r:
            x, y = r.split("<=")
            y = int(y)
            use_range[x][1] = min(use_range[x][1], y)
        elif ">=" in r:
            x, y = r.split(">=")
            y = int(y)
            use_range[x][0] = max(use_range[x][0], y)
        elif "<" in r:
            x, y = r.split("<")
            y = int(y)
            use_range[x][1] = min(use_range[x][1], y - 1)
        elif ">" in r:
            x, y = r.split(">")
            y = int(y)
            use_range[x][0] = max(use_range[x][0], y + 1)

    for y in use_range.values():
        if y[0] > y[1]:
            break
    else:
        acc_ranges.append(use_range)

tot_rating = 0
for p in parts:
    for ar in acc_ranges:
        for val, (lb, ub) in zip(p, ar.values()):
            if not lb <= val <= ub:
                break
        else:
            tot_rating += sum(p)
            break

tot_valid = 0
for ar in acc_ranges:
    tot_valid += reduce(mul, [r[1] - r[0] + 1 for r in ar.values()])

print(f"REDEEMED: {tot_rating}")
print(f"t100 both times! (prob gon fail d20 tho lol): {tot_valid}")
