import sys
import re
import operator

OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}

inp_fmt = re.compile(r"([a-z0-9]+): ([01])")
gate_fmt = re.compile(r"([a-z0-9]+) (AND|XOR|OR) ([a-z0-9]+) -> ([a-z0-9]+)")
reading_inp = True
vals = {}
gates = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        reading_inp = False
        continue

    if reading_inp:
        match = inp_fmt.match(line)
        vals[match.group(1)] = int(match.group(2))
    else:
        match = gate_fmt.match(line)
        arg1, op, arg2, res = match.groups()
        gates[res] = arg1, OPS[op], arg2

fulfilled = 0
while fulfilled < len(gates):
    for reg, (arg1, op, arg2) in gates.items():
        if reg in vals:
            continue

        if arg1 in vals and arg2 in vals:
            vals[reg] = op(vals[arg1], vals[arg2])
            fulfilled += 1

output = 0
for reg, val in vals.items():
    if reg.startswith("z"):
        output += val * (1 << int(reg[1:]))

print(f"not even gonna bother trying to solve p2 programatically: {output}")
