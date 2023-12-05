import enum
from collections import defaultdict


class Op(enum.Enum):
    CPY = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    JNZ = enum.auto()
    TGL = enum.auto()

    def toggle(self):
        return {
            self.CPY: self.JNZ,
            self.INC: self.DEC,
            self.DEC: self.INC,
            self.JNZ: self.CPY,
            self.TGL: self.INC
        }[self]


def exec_lst(
        instructions: list[tuple[Op, str] | tuple[Op, str, str]],
        reg: defaultdict[str, int]
) -> defaultdict[str, int]:
    def to_int(x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else reg[x]

    instructions = [list(i) for i in instructions]
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
            if to_int(i[1]) != 0:
                at += to_int(i[2]) - 1
        elif i[0] == Op.TGL:
            tgl_ind = at + to_int(i[1])
            if 0 <= tgl_ind < len(instructions):
                instructions[tgl_ind][0] = instructions[tgl_ind][0].toggle()
        at += 1
    return reg


lst = []
with open("day23.txt") as read:
    for i in read.readlines():
        if i.isspace():
            break
        args = i.split()
        op = Op[args[0].upper()]
        lst.append((op, *args[1:]))

init_reg = defaultdict(int)
init_reg["a"] = 7
print(f"register a value (p1): {exec_lst(lst, init_reg)['a']}")
