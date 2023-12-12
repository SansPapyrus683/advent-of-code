import numpy as np

KEYPAD1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
KEYPAD2 = np.array([
    "  1  ",
    " 234 ",
    "56789",
    " ABC ",
    "  D  "
])
POS_CHANGE = {
    "U": np.array([-1, 0]),
    "D": np.array([1, 0]),
    "L": np.array([0, -1]),
    "R": np.array([0, 1])
}

with open("input/day2.txt") as read:
    code_dir = [l.strip() for l in read.readlines()]

at = np.array([1, 1])
code = []
for d in code_dir:
    for c in d:
        nxt = at + POS_CHANGE[c]
        if 0 <= nxt[0] < len(KEYPAD1) and 0 <= nxt[1] < len(KEYPAD1[nxt[0]]):
            at = nxt
    code.append(KEYPAD1[at[0], at[1]])

print(f"p1 code: {''.join(str(c) for c in code)}")

at = np.array([2, 0])
center = np.array([2, 2])
code = ""
for d in code_dir:
    for c in d:
        nxt = at + POS_CHANGE[c]
        if np.all(nxt >= 0) and np.abs(nxt - center).sum() <= 2:
            at = nxt
    code += KEYPAD2[at[0]][at[1]]
print(f"p2 code: {code}")
