import re

reg = {}
for r in "ABC":
    fmt = re.compile(rf"Register {r}: (\d+)")
    reg[r] = int(fmt.match(input()).group(1))
input()

prog_fmt = re.compile(r"Program: ([\d,]+)")
prog = [int(i) for i in prog_fmt.match(input()).group(1).split(",")]

ip = 0
get_combo = lambda o: o if o <= 3 else reg["ABC"[o - 4]]
output = []
while ip < len(prog):
    opcode = prog[ip]
    arg = prog[ip + 1]
    if opcode == 0:
        reg["A"] //= (1 << get_combo(arg))
    elif opcode == 1:
        reg["B"] ^= arg
    elif opcode == 2:
        reg["B"] = get_combo(arg) % 8
    elif opcode == 3:
        if reg["A"] != 0:
            ip = arg
            continue
    elif opcode == 4:
        reg["B"] ^= reg["C"]
    elif opcode == 5:
        output.append(get_combo(arg) % 8)
    elif opcode == 6:
        reg["B"] = reg["A"] // (1 << get_combo(arg))
    elif opcode == 7:
        reg["C"] = reg["A"] // (1 << get_combo(arg))
    ip += 2

str_out = ",".join(str(i) for i in output)
print(f"i got scared for a second thought intcode was gonna come back: {str_out}")


def calc_out_for_my_prog_only(out_seq: list[int]) -> int:
    best = float("inf")

    def dfs(at: int, a_bits: list[int | None]):
        nonlocal best
        if at == len(out_seq):
            best = min(best, sum(i * (1 << v) for v, i in enumerate(a_bits)))
            return

        for b in range(8):
            for c in range(8):
                if b ^ c ^ 0b110 != out_seq[at]:
                    continue

                actual_b = b ^ 1
                to_set = []
                for i in range(3):
                    bit = int(bool(actual_b & (1 << i)))
                    to_set.append((3 * at + i, bit))

                    bit = int(bool(c & (1 << i)))
                    to_set.append((3 * at + b + i, bit))

                new_a = a_bits.copy()
                for ind, val in to_set:
                    if ind >= len(new_a) and val == 0:
                        continue
                    if ind >= len(new_a) or new_a[ind] is not None and new_a[ind] != val:
                        break
                    new_a[ind] = val
                else:
                    dfs(at + 1, new_a)

    dfs(0, [None for _ in range(len(out_seq) * 3)])
    return -1 if best == float("inf") else best


print(f"god i HATE reverse engineering... {calc_out_for_my_prog_only(prog)}")
