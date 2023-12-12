import ast
import re
from collections import defaultdict
from ops import Op, op_res

P1_THRESHOLD = 3


before_fmt = r"Before:\s+(\[.*\])"
after_fmt = r"After:\s+(\[.*\])"
samples = []
with open("input/day16p2.txt") as read:
    lines = read.readlines()
    for s in range(0, len(lines), 4):
        bef, op, aft = [l.strip() for l in lines[s:s + 4]][:3]
        bef = ast.literal_eval(next(iter(re.findall(before_fmt, bef))))
        op = [int(i) for i in op.split()]
        aft = ast.literal_eval(next(iter(re.findall(after_fmt, aft))))
        samples.append((bef, op, aft))

total = 0
valid_ops = []
for bef, op, aft in samples:
    valid = 0
    valid_ops.append(set())
    for o in Op:
        if op_res(bef, op[1:], o) == aft:
            valid += 1
            valid_ops[-1].add(o)
    total += valid >= P1_THRESHOLD
print(f"values that have at least {P1_THRESHOLD} valid ops: {total}")

defined = {}
while len(defined) < len(Op):
    for i, v in enumerate(valid_ops):
        if len(v) == 1:
            new = next(iter(v))
            defined[new] = samples[i][1][0]
            for v_ in valid_ops:
                if new in v_:
                    v_.remove(new)
            break
rev_defined = {n: o for o, n in defined.items()}

instructions = []
with open("input/day16p1.txt") as read:
    for i in read.readlines():
        instructions.append([int(j) for j in i.split()])

reg = defaultdict(int)
for i in instructions:
    reg = op_res(reg, i[1:], rev_defined[i[0]])
print(f"value of register 0: {reg[0]}")
