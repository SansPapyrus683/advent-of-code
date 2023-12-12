UNFOLD_FACTOR = 5

GOOD = "."
BAD = "#"
UNK = "?"


def valid_combs(s: str, combs: list[int]) -> int:
    fill_ways = [[0 for _ in range(len(combs) + 1)] for _ in range(len(s) + 1)]
    good = {GOOD, UNK}
    bad = {BAD, UNK}

    for i, char in enumerate(s):
        for j, seq in enumerate(combs):
            if char in bad:
                if seq == i + 1:
                    prev = fill_ways[0][j]
                    if all(c in bad for c in s[:i + 1]):
                        fill_ways[i + 1][j + 1] = prev if j > 0 else 1
                
                elif seq < i + 1:
                    prev = fill_ways[i + 1 - seq - 1][j]
                    all_valid = all(c in bad for c in s[i + 1 - seq:i + 1])
                    prev_valid = j != 0 or all(c in good for c in s[:i + 1 - seq])

                    if all_valid and prev_valid and s[i - seq] in good:
                        fill_ways[i + 1][j + 1] = prev if j > 0 else 1

            if char in good:
                fill_ways[i + 1][j + 1] += fill_ways[i][j + 1]

    return fill_ways[-1][-1]


with open("they_found.txt") as read:
    records = []
    for r in read.readlines():
        r = r.strip().split(" ")
        records.append((r[0], [int(x) for x in r[1].split(",")]))

p1_tot = 0
p2_tot = 0
for row, arrangement in records:
    p1_tot += valid_combs(row, arrangement)
    row = UNK.join(row for _ in range(UNFOLD_FACTOR))
    arrangement *= UNFOLD_FACTOR
    p2_tot += valid_combs(row, arrangement)

print(f"bro what are these problems: {p1_tot}")
print(f"this is like a usaco gold problem almost: {p2_tot}")
