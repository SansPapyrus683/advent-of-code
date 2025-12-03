import sys


def largest_sub_number(string: str, len_: int) -> int:
    # sorry i can't come up w/ a better name
    # basically it's the best number we can get using a certain amt of digits
    dp = [-1 for _ in range(len_ + 1)]
    dp[0] = 0
    for dig in reversed(string):
        for i in range(len_, 0, -1):
            if dp[i - 1] == -1:
                continue
            dp[i] = max(dp[i], dp[i - 1] + 10 ** (i - 1) * int(dig))
    return dp[-1]


batteries = [line.strip() for line in sys.stdin]

p1_volt = sum(largest_sub_number(b, 2) for b in batteries)
p2_volt = sum(largest_sub_number(b, 12) for b in batteries)

print(f"HOLY CHOKE: {p1_volt}")
print(f"spent a whoppipng 5 minutes on p2: {p2_volt}")
