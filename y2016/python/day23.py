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
) -> None:
    def to_int(x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else reg[x]

    mul_ind = 4  # hardcoding this sucks, i know
    op1 = instructions[mul_ind][1]
    op2 = instructions[mul_ind + 4][1]
    temp = instructions[mul_ind][2]
    store_in = instructions[mul_ind + 1][1]

    instructions = [list(i) for i in instructions]
    at = 0
    while 0 <= at < len(instructions):
        if at == mul_ind:
            reg[store_in] = reg[op1] * reg[op2]
            reg[op2] = 0
            reg[temp] = 0
            at = mul_ind + 6

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
            assert not mul_ind <= tgl_ind < mul_ind + 6
            if 0 <= tgl_ind < len(instructions):
                instructions[tgl_ind][0] = instructions[tgl_ind][0].toggle()

        at += 1


lst = []
with open("input/day23.txt") as read:
    for line in read.readlines():
        args = line.split()
        op = Op[args[0].upper()]
        lst.append((op, *args[1:]))

init_reg = defaultdict(int, {"a": 7})
exec_lst(lst, init_reg)
print(f"register a value (p1): {init_reg['a']}")

init_reg = defaultdict(int, {"a": 12})
exec_lst(lst, init_reg)
print(f"register a value (p2): {init_reg['a']}")
