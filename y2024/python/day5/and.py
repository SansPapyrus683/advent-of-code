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
    elems = set(p)
    sorted_ = p.copy()

    update = True
    while update:
        update = False
        for a, b in cmp:
            if a not in elems or b not in elems:
                continue

            a_ind = sorted_.index(a)
            b_ind = sorted_.index(b)
            if a_ind > b_ind:
                sorted_[a_ind], sorted_[b_ind] = sorted_[b_ind], sorted_[a_ind]
                update = True

    if p == sorted_:
        p1_total += p[len(p) // 2]
    else:
        p2_total += sorted_[len(p) // 2]

print(f"barely top 100 for p1: {p1_total}")
print(f"and threw p2. great. {p2_total}")
