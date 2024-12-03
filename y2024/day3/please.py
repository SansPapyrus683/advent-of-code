import re

with open("have_snow.txt") as read:
    mem = "".join(line.strip() for line in read.readlines())

mul_instr = re.compile(r"mul\((\d+),(\d+)\)")
relevant = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
enabled = True
p1_sum = 0
p2_sum = 0
for instr in relevant.findall(mem):
    if (res := mul_instr.match(instr)) is not None:
        a, b = [int(i) for i in res.groups()]
        p1_sum += a * b
        p2_sum += a * b * enabled
    elif instr == "do()":
        enabled = False
    elif instr == "don't()":
        enabled = True

print(f"man i got crapped on today: {p1_sum}")
print(f"well at least i beat adavya hahaha: {p2_sum}")
