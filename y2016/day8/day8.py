import enum
import re
import numpy as np

DIMS = 6, 50
FILLED = "█"
EMPTY = " "


class Op(enum.Enum):
    RECT = enum.auto()
    ROW = enum.auto()
    COL = enum.auto()


rect_fmt = r"rect (\d+)x(\d+)"
row_fmt = r"rotate row y=(\d+) by (\d+)"
col_fmt = r"rotate column x=(\d+) by (\d+)"

instructions = []
with open("day8.txt") as read:
    for i in read.readlines():
        if re.match(rect_fmt, i):
            args = [int(a) for a in re.findall(rect_fmt, i)[0]]
            instructions.append((Op.RECT, *args))
        elif re.match(row_fmt, i):
            args = [int(a) for a in re.findall(row_fmt, i)[0]]
            instructions.append((Op.ROW, *args))
        elif re.match(col_fmt, i):
            args = [int(a) for a in re.findall(col_fmt, i)[0]]
            instructions.append((Op.COL, *args))

screen = np.zeros(DIMS, dtype=bool)
for op, arg1, arg2 in instructions:
    if op == Op.RECT:
        screen[:arg2, :arg1] = True
    elif op == Op.ROW:
        screen[arg1] = np.roll(screen[arg1], arg2)
    elif op == Op.COL:
        screen[:, arg1] = np.roll(screen[:, arg1], arg2)

print(f"total # of lit pixels: {screen.sum()}")

print("message:")
for r in range(len(screen)):
    for c in screen[r]:
        print(FILLED if c else EMPTY, end="")
    print()
