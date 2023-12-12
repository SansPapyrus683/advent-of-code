import enum
from collections import defaultdict


class Op(enum.Enum):
    CPY = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    JNZ = enum.auto()


def exec_lst(
        instructions: list[tuple[Op, str] | tuple[Op, str, str]],
        reg: defaultdict[str, int]
) -> None:
    def to_int(x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else reg[x]

    at = 0
    while 0 <= at < len(instructions):
        i = instructions[at]
        if i[0] == Op.CPY:
            reg[i[2]] = to_int(i[1])
        elif i[0] == Op.INC:
            reg[i[1]] += 1
        elif i[0] == Op.DEC:
            reg[i[1]] -= 1
        elif i[0] == Op.JNZ:
            if to_int(i[1]):
                at += to_int(i[2])
                at -= 1
        at += 1


lst = []
with open("day12.txt") as read:
    for line in read.readlines():
        args = line.split()
        op = Op[args[0].upper()]
        lst.append((op, *args[1:]))

init_reg = defaultdict(int)
exec_lst(lst, init_reg)
print(f"register a value (p1): {init_reg['a']}")

init_reg = defaultdict(int, {"c": 1})
exec_lst(lst, init_reg)
print(f"register a value (p2): {init_reg['a']}")
