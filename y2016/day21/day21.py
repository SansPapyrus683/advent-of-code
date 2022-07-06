import re
from scramble import Op

PW_START = "abcdefgh"
UNSCRAMBLE = "fbgdceah"

with open("day21.txt") as read:
    ops = []
    for i in read.readlines():
        for o in Op:
            res = re.findall(o.value, i)
            if res:
                if type(res[0]) == tuple:
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
