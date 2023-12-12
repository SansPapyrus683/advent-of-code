import re
import enum


class Op(enum.Enum):
    SWAP_POS = r"swap position (\d+) with position (\d+)"
    SWAP_LET = r"swap letter ([a-z]) with letter ([a-z])"
    ROT_LEFT = r"rotate left (\d+) step"
    ROT_RIGHT = r"rotate right (\d+) step"
    ROT_POS = r"rotate based on position of letter ([a-z])"
    REV_POS = r"reverse positions (\d+) through (\d+)"
    MOVE_POS = r"move position (\d+) to position (\d+)"

    def exec(
            self,
            pw: list[str],
            args: tuple[str | int, ...],
            rev: bool = False
    ) -> list[str]:
        pw = pw.copy()

        # print(pw, args, rev)

        if self == Op.SWAP_POS:
            a, b = [int(i) for i in args]
            pw[a], pw[b] = pw[b], pw[a]

        elif self == Op.SWAP_LET:
            a, b = [pw.index(i) for i in args]
            pw[a], pw[b] = pw[b], pw[a]

        elif self == Op.ROT_LEFT:
            a = int(args[0]) % len(pw)
            pw = pw[a:] + pw[:a] if not rev else Op.ROT_RIGHT.exec(pw, (a,))

        elif self == Op.ROT_RIGHT:
            a = int(args[0]) % len(pw)
            pw = pw[-a:] + pw[:-a] if not rev else Op.ROT_LEFT.exec(pw, (a,))

        elif self == Op.ROT_POS:
            ind = pw.index(args[0])
            if not rev:
                pw = Op.ROT_RIGHT.exec(pw, (1 + ind + (ind >= 4),))
            else:
                for rl_amt in range(len(pw)):
                    init_ind = (ind - rl_amt) % len(pw)
                    rr_amt = (1 + init_ind + (init_ind >= 4)) % len(pw)
                    if rr_amt == rl_amt:
                        pw = Op.ROT_LEFT.exec(pw, (rl_amt,))
                        break

        elif self == Op.REV_POS:
            a, b = [int(i) for i in args]
            pw[a:b + 1] = list(reversed(pw[a:b + 1]))

        elif self == Op.MOVE_POS:
            a, b = [int(i) for i in args]
            if rev:
                a, b = b, a
            x = pw.pop(a)
            pw.insert(b, x)

        return pw


PW_START = "abcdefgh"
UNSCRAMBLE = "fbgdceah"

with open("input/day21.txt") as read:
    ops = []
    for i in read.readlines():
        for o in Op:
            res = re.findall(o.value, i)
            if res:
                if isinstance(res[0], tuple):
                    res = res[0]
                ops.append((o, *res))

curr_pw = list(PW_START)
for o in ops:
    curr_pw = o[0].exec(curr_pw, o[1:])

print(f"scrambled pw: {''.join(curr_pw)}")

curr_pw = list(UNSCRAMBLE)
for o in reversed(ops):
    curr_pw = o[0].exec(curr_pw, o[1:], True)

print(f"unscrambled pw: {''.join(curr_pw)}")
