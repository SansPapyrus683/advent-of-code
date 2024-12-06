import sys
from collections import Counter

left = []
right = []
for i in sys.stdin:
    l, r = [int(i) for i in i.split()]
    left.append(l)
    right.append(r)

right_amt = Counter(right)
left.sort()
right.sort()

dist = 0
sim_score = 0
for l, r in zip(left, right):
    dist += abs(l - r)
    sim_score += l * right_amt[l]

print(f"HAHAHAHAHAHA WRONG ANSWERED ON P1: {dist}")
print(f"yeah this year is gonna be cooked: {sim_score}")
