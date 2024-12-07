import sys
import operator
from itertools import product


def concat(a: int, b: int):
    return int(f"{a}{b}")


P1_OPS = [operator.add, operator.mul]
P2_OPS = [operator.add, operator.mul, concat]


arr = []
for l in sys.stdin:
    target, nums = l.strip().split(":")
    arr.append((int(target), [int(i) for i in nums.split()]))

p1_sum = 0
p2_sum = 0
for target, nums in arr:
    p2_sat = False
    for combo in product(P1_OPS, repeat=len(nums) - 1):
        val = nums[0]
        for op, i in zip(combo, nums[1:]):
            val = op(val, i)
        if val == target:
            p1_sum += target
            p2_sum += target
            p2_sat = True
            break

    if p2_sat:
        continue

    for combo in product(P2_OPS, repeat=len(nums) - 1):
        val = nums[0]
        for op, i in zip(combo, nums[1:]):
            val = op(val, i)
        if val == target:
            p2_sum += target
            break

print(f"lmao i highkey trolled today: {p1_sum}")
print(f"like i was doing a exponential search after an already exponential computation: {p2_sum}")
