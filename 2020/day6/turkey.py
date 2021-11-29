with open('mistletoe.txt') as read:
    so_far = []
    all_answers = []
    for line in read.readlines():
        if line == '\n':
            all_answers.append(so_far)
            so_far = []
        else:
            so_far.append(line.strip())
    all_answers.append(so_far)

p1_total = 0
p2_total = 0
for a in all_answers:
    everyone = set(a[0])
    for p in a[1:]:
        everyone = everyone.intersection(set(p))
    p2_total += len(everyone)
    p1_total += len(set(''.join(a)))
print(f"the premise of this problem is really weird ngl {p1_total}")
print(f"and there were only what, 1000 seats on the plane from day 5? how the frick-{p2_total}")
