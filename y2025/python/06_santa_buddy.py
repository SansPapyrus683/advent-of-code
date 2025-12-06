import sys
import math

raw_lines = [list(line.rstrip()) for line in sys.stdin]

spaces = []
min_len = min(len(l) for l in raw_lines)
for i in range(min_len):
    if all(l[i] == " " for l in raw_lines):
        for l in raw_lines:
            l[i] = "|"

lines = ["".join(l).split("|") for l in raw_lines]

p1_sum = 0
p2_sum = 0
for eq in range(len(lines[0])):
    params = [l[eq] for l in lines]

    nums1 = [int(n) for n in params[:-1]]

    nums2 = []
    for i in range(len(params[0])):
        curr = []
        for n in params[:-1]:
            if i < len(n) and n[i] != " ":
                curr.append(n[i])
        nums2.append(int("".join(curr)))

    op = params[-1].strip()
    if op == "+":
        p1_sum += sum(nums1)
        p2_sum += sum(nums2)

    elif op == "*":
        p1_sum += math.prod(nums1)
        p2_sum += math.prod(nums2)

print(f"well p1 was quick: {p1_sum}")
print(f"p2, not so much... {p2_sum}")
