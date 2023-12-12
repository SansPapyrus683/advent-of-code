claims = []
max_r = 0
max_c = 0
with open('day3.txt') as read:
    for c in read.readlines():
        c = ''.join(i if i.isdigit() else ' ' for i in c)
        c = [int(i) for i in c.split()]

        max_r = max(max_r, c[1] + c[3])
        max_c = max(max_c, c[2] + c[4])

        assert all(i >= 0 for i in c)
        claims.append(c)

fabric = [[0] * max_c for _ in range(max_r)]
for claim in claims:
    for r in range(claim[1], claim[1] + claim[3]):
        for c in range(claim[2], claim[2] + claim[4]):
            fabric[r][c] += 1

conflicts = 0
for r in range(max_r):
    for c in range(max_c):
        conflicts += fabric[r][c] >= 2

print(f"conflicting area amt: {conflicts}")

for claim in claims:
    valid = True
    for r in range(claim[1], claim[1] + claim[3]):
        for c in range(claim[2], claim[2] + claim[4]):
            if fabric[r][c] > 1:
                valid = False
                break
        if not valid:
            break
    else:
        print(f"non-conflicting claim id: {claim[0]}")
