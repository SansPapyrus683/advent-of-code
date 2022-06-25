#include <string>
#include <vector>
#include <map>

enum OpCode {
    ADDR, ADDI,
    MULR, MULI,
    BANR, BANI,
    BORR, BORI,
    SETR, SETI,
    GTIR, GTRI, GTRR,
    EQIR, EQRI, EQRR
};

struct Op {
    OpCode opcode;
    int a, b, c;
};

void exe_op(std::vector<long long>& reg, const Op& op) {
    switch (op.opcode) {
        case ADDR:
            reg[op.c] = reg[op.a] + reg[op.b];
            break;
        case ADDI:
            reg[op.c] = reg[op.a] + op.b;
            break;
        case MULR:
            reg[op.c] = reg[op.a] * reg[op.b];
            break;
        case MULI:
            reg[op.c] = reg[op.a] * op.b;
            break;
        case BANR:
            reg[op.c] = reg[op.a] & reg[op.b];
            break;
        case BANI:
            reg[op.c] = reg[op.a] & op.b;
            break;
        case BORR:
            reg[op.c] = reg[op.a] | reg[op.b];
            break;
        case BORI:
            reg[op.c] = reg[op.a] | op.b;
            break;
        case SETR:
            reg[op.c] = reg[op.a];
            break;
        case SETI:
            reg[op.c] = op.a;
            break;
        case GTIR:
            reg[op.c] = op.a > reg[op.b];
            break;
        case GTRI:
            reg[op.c] = reg[op.a] > op.b;
            break;
        case GTRR:
            reg[op.c] = reg[op.a] > reg[op.b];
            break;
        case EQIR:
            reg[op.c] = op.a == reg[op.b];
            break;
        case EQRI:
            reg[op.c] = reg[op.a] == op.b;
            break;
        case EQRR:
            reg[op.c] = reg[op.a] == reg[op.b];
            break;
    }
}

const std::map<std::string, OpCode> OP_MAP{
    {"addr", ADDR},
    {"addi", ADDI},
    {"mulr", MULR},
    {"muli", MULI},
    {"banr", BANR},
    {"bani", BANI},
    {"borr", BORR},
    {"bori", BORI},
    {"setr", SETR},
    {"seti", SETI},
    {"gtir", GTIR},
    {"gtri", GTRI},
    {"gtrr", GTRR},
    {"eqir", EQIR},
    {"eqri", EQRI},
    {"eqrr", EQRR},
};
