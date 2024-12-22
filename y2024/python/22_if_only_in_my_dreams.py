import sys
from collections import defaultdict

SECRET_LEN = 2000
SEQ_LEN = 4


def evolve(secret: int) -> int:
    mod = 16777216
    secret = (secret ^ (secret * 64)) % mod
    # ngl not sure if the mod here is necessary. too bad!
    secret = (secret ^ (secret // 32)) % mod
    return (secret ^ (secret * 2048)) % mod


numbers = [int(i) for i in sys.stdin]
changes = []
secret_sum = 0
for n in numbers:
    curr_changes = []
    for _ in range(SECRET_LEN):
        old_n = n
        n = evolve(n)
        curr_changes.append((n % 10) - (old_n % 10))
    secret_sum += n
    changes.append(curr_changes)

seq_gains = defaultdict(int)
for v, ch in enumerate(changes):
    curr_price = numbers[v] % 10 + sum(ch[: SEQ_LEN - 1])
    visited = set()
    for i in range(SEQ_LEN, SECRET_LEN):
        curr_price += ch[i - 1]
        seq = tuple(ch[i - SEQ_LEN : i])
        if seq in visited:
            continue
        visited.add(seq)
        seq_gains[seq] += curr_price

print(f"well scraped into t100 for today: {secret_sum}")
print(f"thank you eric for the easy day: {max(seq_gains.values())}")
