import numpy as np
from collections import defaultdict

asdf = []
with open("hes_parson_brown.txt") as read:
    for l in read.readlines():
        a, b = l.strip().split()
        on = a == 'on'
        b = b.split(',')
        b = [x.split('=') for x in b]
        for i in range(len(b)):
            b[i][1] = [int(y) for y in b[i][1].split('..')]
        asdf.append([on, np.array([x[1] for x in b])])

min_val = min(a.min() for o, a in asdf)
max_val = max(a[0].max() for o, a in asdf)

if min_val <= 0:
    for o, a in asdf:
        a -= min_val

total = 0
for i in range(max_val + 1):
    stuff = defaultdict(lambda: defaultdict(int))
    for o, a in asdf:
        if a[0][0] <= i <= a[0][1]:
            if o:
                stuff[a[1, 0]][a[2, 0]] = 1
                stuff[a[1, 1]][a[2, 0]] = 1
            else:
                stuff[a[1, 0]][a[2, 0]] = 0
                stuff[a[1, 1]][a[2, 0]] = 0
            stuff[a[1, 1]][a[2, 1]] = 0
            stuff[a[1, 0]][a[2, 1]] = 0
    print({v: dict(k) for v, k in dict(stuff).items()})
    curr = 0
    last_r = 0
    this_total = 0
    for r in sorted(stuff.keys()):
        row = stuff[r]
        last_c = 0
        for c in sorted(row.keys()):
            val = row[c]
            if curr == 1:
                this_total += (c - last_c) * (r - last_r)
            if val == 1:
                curr = 1
            else:
                curr = 0
            last_c = c
    print(this_total)
    total += this_total
print(total)
