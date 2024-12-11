from collections import defaultdict

P1_BLINKS = 25
P2_BLINKS = 75

stones = defaultdict(int)
for s in input().split():
    stones[int(s)] += 1

for b in range(max(P1_BLINKS, P2_BLINKS)):
    new_stones = defaultdict(int)
    for s, amt in stones.items():
        if s == 0:
            new_stones[1] += amt
        elif len(str(s)) % 2 == 0:
            str_s = str(s)
            new_stones[int(str_s[:len(str_s) // 2])] += amt
            new_stones[int(str_s[len(str_s) // 2:])] += amt
        else:
            new_stones[s * 2024] += amt
    stones = new_stones

    if b == P1_BLINKS - 1:
        print(f"ok not too hot today: {sum(stones.values())}")
    elif b == P2_BLINKS - 1:
        print(f"but we keep trying! {sum(stones.values())}")
