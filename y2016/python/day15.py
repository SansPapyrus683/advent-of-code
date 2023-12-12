import re
from itertools import count

# number of positions then the starting position
P2_DISC = 11, 0


def capsule_time(disc_order: list[tuple[int, int]]) -> int:
    for t in count(0):
        times = [(start + t + i + 1) % mod for i, (mod, start) in enumerate(disc_order)]
        if all(t_ == 0 for t_ in times):
            return t


disc_fmt = r"disc #\d+ has (\d+) positions; at time=0, it is at position (\d+)."

discs = []
with open("input/day15.txt") as read:
    for d in read.readlines():
        d = d.lower()
        if re.match(disc_fmt, d):
            discs.append(tuple([int(i) for i in re.findall(disc_fmt, d)[0]]))

print(f"p1 capsule time: {capsule_time(discs)}")
print(f"p2 capsule time (aka with the added disc): {capsule_time(discs + [P2_DISC])}")
