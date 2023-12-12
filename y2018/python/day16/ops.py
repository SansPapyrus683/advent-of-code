import enum


class Op(enum.Enum):
    ADDR = enum.auto()
    ADDI = enum.auto()
    MULR = enum.auto()
    MULI = enum.auto()
    BANR = enum.auto()
    BANI = enum.auto()
    BORR = enum.auto()
    BORI = enum.auto()
    SETR = enum.auto()
    SETI = enum.auto()
    GTIR = enum.auto()
    GTRI = enum.auto()
    GTRR = enum.auto()
    EQIR = enum.auto()
    EQRI = enum.auto()
    EQRR = enum.auto()


def op_res(
        registers: list[int], args: tuple[int, int, int], op_code: Op
) -> list[int]:
    a, b, c = args
    registers = registers.copy()
    match op_code:
        case Op.ADDR:
            registers[c] = registers[a] + registers[b]
        case Op.ADDI:
            registers[c] = registers[a] + b
        case Op.MULR:
            registers[c] = registers[a] * registers[b]
        case Op.MULI:
            registers[c] = registers[a] * b
        case Op.BANR:
            registers[c] = registers[a] & registers[b]
        case Op.BANI:
            registers[c] = registers[a] & b
        case Op.BORR:
            registers[c] = registers[a] | registers[b]
        case Op.BORI:
            registers[c] = registers[a] | b
        case Op.SETR:
            registers[c] = registers[a]
        case Op.SETI:
            registers[c] = a
        case Op.GTIR:
            registers[c] = int(a > registers[b])
        case Op.GTRI:
            registers[c] = int(registers[a] > b)
        case Op.GTRR:
            registers[c] = int(registers[a] > registers[b])
        case Op.EQIR:
            registers[c] = int(a == registers[b])
        case Op.EQRI:
            registers[c] = int(registers[a] == b)
        case Op.EQRR:
            registers[c] = int(registers[a] == registers[b])
    return registers
