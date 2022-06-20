import re
import numpy as np

bot_fmt = r'pos=<(-?\d+),(-?\d+),(-?\d+)>,\s*r=(\d+)'
bots = []
with open('day23.txt') as read:
    for b in read.readlines():
        p1, p2, p3, rad = [int(i) for i in next(iter(re.findall(bot_fmt, b)))]
        bots.append((np.array([p1, p2, p3]), rad))

max_r = max(b[1] for b in bots)
max_r_bots = [b for b in bots if b[1] == max_r]
assert len(max_r_bots) == 1
bot, bot_range = max_r_bots[0]
in_range = 0
for b in bots:
    in_range += np.abs(b[0] - bot).sum() <= bot_range

print(f"number of nanbots in range: {in_range}")
