from statistics import median

crabs = [int(i) for i in input().split(",")]

"""
this approach is from this thread here
https://math.stackexchange.com/questions/113270
idek how it 100% works, but it does, so i'm using it
"""
med_pos = median(crabs)
p1_fuel = int(sum(abs(c - med_pos) for c in crabs))  # should always be an integer
print(f"thank god for this obscure math black magic thing: {p1_fuel}")

"""
lmao idk if there's a better way to do this
ME 20 MINS LATER: turns out the mean is the one that minimizes the squared error
"""
min_pos = min(crabs)
max_pos = max(crabs)
p2_fuel = float("inf")
for p in range(min_pos, max_pos + 1):
    total = 0
    for c in crabs:
        dist = abs(c - p)
        total += dist * (dist + 1) // 2
    p2_fuel = min(p2_fuel, total)
print(f"yoooo 1st time i got top 100 for both stars: {p2_fuel}")
