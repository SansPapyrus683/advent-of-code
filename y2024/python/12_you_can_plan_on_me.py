import sys
import re
from fractions import Fraction

P2_INC = 10000000000000


def token_amt(ax: int, ay: int, bx: int, by: int, x: int, y: int) -> int | None:
    # avoid any loss of precision
    ax, ay, bx, by, x, y = [Fraction(i) for i in [ax, ay, bx, by, x, y]]

    b_amt = (x - ax / ay * y) / (bx - ax * by / ay)
    if b_amt.is_integer():
        a_amt = (x - b_amt * bx) / ax
        if a_amt.is_integer():
            return int(a_amt * 3 + b_amt)
    return None


# eh, let's just calculate the input as we go along
p1_tokens = 0
p2_tokens = 0

raw = sys.stdin.read().split("\n\n")
machine_fmt = re.compile(r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)""")
for m in raw:
    res = machine_fmt.match(m)
    if res is None:
        continue

    ax, ay, bx, by, x, y = [int(res.group(i)) for i in range(1, 6 + 1)]
    if p1 := token_amt(ax, ay, bx, by, x, y):
        p1_tokens += p1
    if p2 := token_amt(ax, ay, bx, by, x + P2_INC, y + P2_INC):
        p2_tokens += p2

print(f"lol i stressed way too hard when i saw p2: {p1_tokens}")
print(f"thankfully(?) it was just some algebra: {p2_tokens}")
