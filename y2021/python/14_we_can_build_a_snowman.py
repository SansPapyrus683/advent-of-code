import sys
from collections import defaultdict

P1_AMT = 10
P2_AMT = 40


def most_minus_least(pair_amts: dict[str, int], start: str, end: str):
    assert len(start) == 1 and len(end) == 1
    assert all(len(k) == 2 for k in pair_amts)
    occ_num = defaultdict(int)
    for a, b in pair_amts.items():
        occ_num[a[0]] += b
        occ_num[a[1]] += b
    # we double counted every character save for the first and last ones
    occ_num[polymer[0]] += 1
    occ_num[polymer[-1]] += 1
    # ok now we can divide by 2, the start & end won't be affected
    occ_num = {a: b // 2 for a, b in occ_num.items()}
    return max(occ_num.values()) - min(occ_num.values())


polymer = input()
input()  # screw off whitespace
rules = []
for i in sys.stdin:
    rules.append(i.strip().split(" -> "))
rules = {a: b for a, b in rules}

pairs = defaultdict(int)
for i in range(len(polymer) - 1):
    pairs[polymer[i:i + 2]] += 1

p1_final = None
p2_final = None
for i in range(max(P1_AMT, P2_AMT)):
    new_pairs = pairs.copy()
    for p in pairs:
        if p not in rules:
            continue
        to_add = rules[p]
        left = p[0] + to_add
        right = to_add + p[1]
        new_pairs[left] += pairs[p]  # we've made some new pairs!
        new_pairs[right] += pairs[p]
        new_pairs[p] -= pairs[p]  # but the original pair is destroyed lol
    pairs = new_pairs

    if i == P1_AMT - 1:
        p1_final = pairs
    elif i == P2_AMT - 1:
        p2_final = pairs

p1_ans = most_minus_least(p1_final, polymer[0], polymer[-1])
print(f"me during p1: oh this ain't so bad- {p1_ans}")
p2_ans = most_minus_least(p2_final, polymer[0], polymer[-1])
print(f"me during p2: i regret everything- {p2_ans}")
