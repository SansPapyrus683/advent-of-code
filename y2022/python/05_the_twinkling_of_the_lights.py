import sys
from copy import deepcopy
import re

stacks = []
initial, instructions = [i.split("\n") for i in sys.stdin.read().split("\n\n")]
for col in initial[:-1]:
    string_ind = 1
    stack_ind = 0
    while string_ind < len(col):
        if not col[string_ind].isspace():
            while stack_ind >= len(stacks):
                stacks.append([])
            stacks[stack_ind].append(col[string_ind])
        string_ind += 4
        stack_ind += 1

for col in range(len(stacks)):
    stacks[col] = stacks[col][::-1]

p1_stacks = deepcopy(stacks)
p2_stacks = deepcopy(stacks)

instruct_fmt = r"move (\d+) from (\d+) to (\d+)"
for i in instructions:
    fmt_res = re.match(instruct_fmt, i)
    if fmt_res is not None:
        amt, start, end = [int(b) for b in re.search(instruct_fmt, i).groups()]
        start -= 1
        end -= 1

        for _ in range(amt):
            p1_stacks[end].append(p1_stacks[start].pop())

        p2_stacks[end].extend(p2_stacks[start][-amt:])
        del p2_stacks[start][-amt:]

top1 = "".join(s[-1] for s in p1_stacks)
top2 = "".join(s[-1] for s in p2_stacks)
print(f"damn i got top 100 both times again! {top1}")
print(f"input parsing was really stupid this time tho: {top2}")
