import sys

GALAXY = "#"
EMPTY = "."
P1_EXPAND = 2
P2_EXPAND = 10 ** 6


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


univ = [r.strip() for r in sys.stdin]
assert all(len(r) == len(univ[0]) for r in univ)

rows = set()
cols = set()
for r in range(len(univ)):
    if all(c == EMPTY for c in univ[r]):
        rows.add(r)
for c in range(len(univ[0])):
    if all(r[c] == EMPTY for r in univ):
        cols.add(c)

gals = []
for r in range(len(univ)):
    for c in range(len(univ[0])):
        if univ[r][c] == GALAXY:
            gals.append((r, c))

total_p1 = 0
total_p2 = 0
for i in range(len(gals)):
    gi = gals[i]
    for j in range(i + 1, len(gals)):
        gj = gals[j]
        trav_rows = range(*sorted([gi[0], gj[0]]))
        void_rows = sum(r in rows for r in trav_rows)
        norm_rows = len(trav_rows) - void_rows

        trav_cols = range(*sorted([gi[1], gj[1]]))
        void_cols = sum(c in cols for c in trav_cols)
        norm_cols = len(trav_cols) - void_cols

        dist_p1 = P1_EXPAND * (void_rows + void_cols) + norm_rows + norm_cols
        total_p1 += dist_p1
        dist_p2 = P2_EXPAND * (void_rows + void_cols) + norm_rows + norm_cols
        total_p2 += dist_p2

print(f"i guess every streak has an end: {total_p1}")
print(f"didn't even make top 1000 for p2 lmao: {total_p2}")
