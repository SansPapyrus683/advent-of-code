import sys
from operator import mul
from functools import reduce

COLORS = {"red": 12, "green": 13, "blue": 14}

games = {}
for g in sys.stdin:
    id_, info = g.split(":")
    id_ = int(id_.split()[1])
    rounds = []
    for i in info.split("; "):
        balls = {}
        for b in i.split(","):
            amt, ball = b.split()
            assert ball in COLORS
            balls[ball] = int(amt)
        rounds.append(balls)
    games[id_] = rounds

valid_sum = 0
power_tot = 0
for id_, g in games.items():
    min_needed = {c: 0 for c in COLORS}
    valid = True
    for r in g:
        if any(r.get(c, 0) > COLORS[c] for c in COLORS):
            valid = False
        for c in COLORS:
            min_needed[c] = max(min_needed[c], r.get(c, 0))

    if valid:
        valid_sum += id_
    power_tot += reduce(mul, min_needed.values(), 1)

print(f"it's confirmed: {valid_sum}")
print(f"i am 100% washed as hell: {power_tot}")
