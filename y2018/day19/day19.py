import re
from collections import defaultdict
from y2018.day16.ops import Op, op_res

P2_RUN_AMT = 1000

ip_fmt = r'#ip ([0-5])'
instruction_fmt = r'([a-zA-Z]+) (\d+) (\d+) (\d+)'
instructions = []
with open('day19.txt') as read:
    lines = read.readlines()
    ip = int(next(iter(re.findall(ip_fmt, lines[0]))))
    for l in lines[1:]:
        op, a, b, c = next(iter(re.findall(instruction_fmt, l)))
        a, b, c = map(int, (a, b, c))
        instructions.append((Op[op.upper()], a, b, c))

ip_val = 0
registers = defaultdict(int)
while 0 <= ip_val < len(instructions):
    i = instructions[ip_val]
    registers[ip] = ip_val
    registers = op_res(registers, i[1:], i[0])
    ip_val = registers[ip]
    ip_val += 1

print(f"p1 register 0 val: {registers[0]}")

ip_val = 0
registers = defaultdict(int)
registers[0] = 1
for _ in range(P2_RUN_AMT):
    i = instructions[ip_val]
    registers[ip] = ip_val
    registers = op_res(registers, i[1:], i[0])
    ip_val = registers[ip]
    ip_val += 1

# explanation sauce: https://todd.ginsberg.com/post/advent-of-code/2018/day19/
giant_num = max(registers.values())
total = 0
for i in range(1, giant_num + 1):
    if giant_num % i == 0:
        total += i
print(f"p2 register 0 val: {total}")
