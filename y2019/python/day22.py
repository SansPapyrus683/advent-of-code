import enum
import re

P1_DECK, P1_CARD = 10007, 2019
P2_DECK, P2_POS, P2_LOOPS = 119315717514047, 2020, 101741582076661


class CardOp(enum.Enum):
    STACK = enum.auto()
    CUT = enum.auto()
    INC = enum.auto()


def compress_ops(ops: list[tuple[CardOp, int]], deck: int) -> tuple[int, int]:
    mul = 1
    sub = 0
    for t, v in ops:
        if t == CardOp.STACK:
            mul, sub = -mul, -sub
            sub -= deck - 1
        elif t == CardOp.CUT:
            sub += v
        elif t == CardOp.INC:
            mul *= v
            sub *= v
        mul %= deck
        sub %= deck
    return mul, sub


def mod_inv(x: int, mod: int) -> int:
    """https://stackoverflow.com/a/9758173/12128483"""
    return pow(x, -1, mod)


def card_pos(
        ops: list[tuple[CardOp, int]],
        card: int, deck: int
):
    mul, sub = compress_ops(ops, deck)
    return (card * mul - sub) % deck


def pos_card(
        ops: list[tuple[CardOp, int]],
        pos: int, deck: int, loops: int
) -> int:
    # i really should explain what i'm doing here huh
    mul, sub = compress_ops(ops, deck)
    mul_pow = pow(mul, loops, deck)

    top = pos + sub * (mul_pow - 1) * mod_inv(mul - 1, deck)
    bot = mod_inv(mul_pow, deck)
    return top * bot % deck


stack_fmt = "^deal into new stack$"
cut_fmt = r"^cut (-?\d+)$"
inc_fmt = r"^deal with increment (\d+)"
ops = []
with open("input/day22.txt") as read:
    for i in read.readlines():
        if re.findall(stack_fmt, i):
            ops.append((CardOp.STACK, 0))  # 2nd # isn't needed lol
        elif res := re.findall(cut_fmt, i):
            ops.append((CardOp.CUT, int(res[0])))
        elif res := re.findall(inc_fmt, i):
            ops.append((CardOp.INC, int(res[0])))

print(f"pos of card {P1_CARD}: {card_pos(ops, P1_CARD, P1_DECK)}")
print(f"card in pos {P2_POS}: {pos_card(ops, P2_POS, P2_DECK, P2_LOOPS)}")
