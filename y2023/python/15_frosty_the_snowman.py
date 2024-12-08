import sys
from collections import defaultdict


def hash_(s: str) -> int:
    curr = 0
    for c in s:
        c = ord(c)
        curr += c
        curr = (curr * 17) % 256
    return curr


ops = [o.strip() for o in sys.stdin.read().split(",")]

tot_hash = 0
boxes = defaultdict(list)
for o in ops:
    tot_hash += hash_(o)
    if o.endswith("-"):
        name = o[:-1]
        box_num = hash_(name)
        boxes[box_num] = [[n, num] for n, num in boxes[box_num] if n != name]

    elif "=" in o:
        mid = o.find("=")
        name = o[:mid]
        num = int(o[mid + 1:])
        box_num = hash_(name)
        for i, lens in enumerate(boxes[box_num]):
            if lens[0] == name:
                boxes[box_num][i][1] = num
                break
        else:
            boxes[box_num].append([name, num])

    else:
        raise ValueError(f"invalid operation {o}")

focus_power = 0
for o, j in boxes.items():
    for v, (a, b) in enumerate(j):
        focus_power += (o + 1) * (v + 1) * b

print(f"well i finally got ONE t100: {tot_hash}")
print(f"why am i getting so worked up over some funny elves: {focus_power}")
