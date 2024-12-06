from functools import cmp_to_key

cmp = set()
pages = []
with open("presents.txt") as read:
    reading_order = True
    for line in read:
        if line == "\n":
            reading_order = False
            continue

        line = line.strip()
        if reading_order:
            cmp.add(tuple(int(i) for i in line.split("|")))
        else:
            pages.append([int(i) for i in line.split(",")])

p1_total = 0
p2_total = 0
for p in pages:
    sorted_ = sorted(p, key=cmp_to_key(lambda a, b: -1 if (a, b) in cmp else 1))
    if p == sorted_:
        p1_total += p[len(p) // 2]
    else:
        p2_total += sorted_[len(p) // 2]

print(f"barely top 100 for p1: {p1_total}")
print(f"and threw p2. great. {p2_total}")
