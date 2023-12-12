import enum
from collections import defaultdict

CHECK_THRESH = 10  # this was enough for me lol


class Op(enum.Enum):
    CPY = enum.auto()
    INC = enum.auto()
    DEC = enum.auto()
    JNZ = enum.auto()
    TGL = enum.auto()
    OUT = enum.auto()

    def toggle(self):
        return {
            self.CPY: self.JNZ,
            self.INC: self.DEC,
            self.DEC: self.INC,
            self.JNZ: self.CPY,
            self.TGL: self.INC,
            self.OUT: self.INC
        }[self]


def exec_lst(
        instructions: list[tuple[Op, str] | tuple[Op, str, str]],
        reg: defaultdict[str, int]
) -> list[int]:
    def to_int(x: str) -> int:
        return int(x) if x.lstrip("-").isdigit() else reg[x]

    instructions = [list(i) for i in instructions]
    at = 0
    ret = []
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
        elif i[0] == Op.OUT:
            ret.append(to_int(i[1]))
            if len(ret) == CHECK_THRESH:
                return ret

        at += 1


lst = []
with open("input/day25.txt") as read:
    for line in read.readlines():
        args = line.split()
        op = Op[args[0].upper()]
        lst.append((op, *args[1:]))

a = 0
while True:
    init_reg = defaultdict(int, {"a": a})
    res = exec_lst(lst, init_reg)
    if all(v % 2 == i for v, i in enumerate(res)):
        print(f"you need to set a to {a} for the sequence")
        break
    a += 1
