"""an alternate solution involving recursion and cashing"""
from functools import cache

UNFOLD_FACTOR = 5

GOOD = "."
BAD = "#"
UNK = "?"


def valid_combs(s: str, combs: list[int]) -> int:
    @cache
    def solve(s_at: int, c_at: int) -> int:
        if s_at >= len(s):
            return int(c_at == len(combs))
        elif c_at == len(combs):
            return int(all(c != BAD for c in s[s_at:]))
        else:
            if len(s) - s_at < combs[c_at]:
                return 0

            ans = 0
            if s[s_at] != BAD:
                ans += solve(s_at + 1, c_at)

            for i in range(s_at, s_at + combs[c_at]):
                if s[i] == GOOD:
                    break
            else:
                prev_valid = s_at == 0 or s[s_at - 1] != BAD
                n_ind = s_at + combs[c_at]
                next_valid = n_ind == len(s) or s[n_ind] != BAD
                if prev_valid and next_valid:
                    ans += solve(n_ind + 1, c_at + 1)

            return ans

    return solve(0, 0)


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

print(f"well it's the next morning: {p1_tot}")
print(f"and all it takes is a cache for brute force to work... {p2_tot}")
