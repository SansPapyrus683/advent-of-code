"""bruh couldn't get all the song lyrics in this year as well"""
import sys


def snafu_to_dec(n: str) -> int:
    base = 1
    ret = 0
    for c in reversed(n):
        ret += {
            "0": 0, "1": 1, "2": 2,
            "-": -1, "=": -2
        }[c] * base
        base *= 5
    return ret


def dec_to_snafu(n: int) -> str:
    raw_digits = []
    while n:
        n, r = divmod(n, 5)
        raw_digits.append(r)
    raw_digits.append(0)

    digits = []
    for v, d in enumerate(raw_digits):
        if 0 <= d <= 2:
            digits.append(d)
        else:
            digits.append({3: "=", 4: "-", 5: 0}[d])
            raw_digits[v + 1] += 1

    if len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return "".join(str(d) for d in reversed(digits))


fuel_reqs = [i.strip() for i in sys.stdin]

total = sum(snafu_to_dec(r) for r in fuel_reqs)
print(f"well, guess that's it! {dec_to_snafu(total)} and we're done...")
