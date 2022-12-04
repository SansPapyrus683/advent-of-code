from typing import Union
import enum
from collections import defaultdict


class Op(enum.Enum):
    CPY = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    JNZ = enum.auto()


def exec_lst(
        instructions: list[Union[tuple[Op, str], tuple[Op, str, str]]],
        reg: defaultdict[str, int]
) -> defaultdict[str, int]:
    at = 0
    while 0 <= at < len(instructions):
        i = instructions[at]
        if i[0] == Op.CPY:
            reg[i[2]] = int(i[1]) if i[1].isdigit() else reg[i[1]]
        elif i[0] == Op.INC:
            reg[i[1]] += 1
        elif i[0] == Op.DEC:
            reg[i[1]] -= 1
        elif i[0] == Op.JNZ:
            if (int(i[1]) if i[1].isdigit() else reg[i[1]]) != 0:
                at += int(i[2])
                at -= 1
        at += 1
    return reg


lst = []
with open("day12.txt") as read:
    for i in read.readlines():
        if i.isspace():
            break
        args = i.split()
        op = Op[args[0].upper()]
        lst.append((op, *args[1:]))

init_reg = defaultdict(int)
print(f"register a value (p1): {exec_lst(lst, init_reg)['a']}")

init_reg = defaultdict(int)
init_reg["c"] = 1
print(f"register a value (p2): {exec_lst(lst, init_reg)['a']}")
