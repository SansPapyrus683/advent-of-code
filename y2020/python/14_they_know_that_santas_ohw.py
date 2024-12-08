import sys
from itertools import product

BIT_NUM = 36


def apply_mask_p1(bitmask: str, num: str) -> str:
    assert len(bitmask) == len(num)
    to_return = ""
    for i_ in range(len(num)):  # underscore so intellij stops bugging me
        to_return += bitmask[i_] if bitmask[i_] != "X" else num[i_]
    return to_return


def apply_mask_p2(bitmask: str, num: str) -> str:
    assert len(bitmask) == len(num)
    to_return = ""
    for i_ in range(len(num)):
        to_return += bitmask[i_] if bitmask[i_] != "0" else num[i_]
    return to_return


instructions = []
for line in sys.stdin:
    line = [s.strip() for s in line.split("=")]
    if line[0] == "mask":
        instructions.append(["mask", line[1]])
    else:
        # for the sake of consistency, i made both binary
        address = int(line[0][4:-1])
        value = int(line[1])
        instructions.append(
            [bin(address)[2:].zfill(BIT_NUM), bin(value)[2:].zfill(BIT_NUM)]
        )

p1mem = {}
p2mem = {}
mask = None  # there should be a mask at the start of everything i think
for i in instructions:
    if i[0] == "mask":
        mask = i[1]
    else:
        p1mem[int(i[0], 2)] = int(apply_mask_p1(mask, i[1]), 2)

        address_bin = list(apply_mask_p2(mask, i[0]))
        indices = [v for v, c in enumerate(address_bin) if c == "X"]
        numbers = [["0", "1"]] * len(indices)

        for c in product(*numbers):
            for b, ind in zip(c, indices):
                address_bin[ind] = b
            p2mem[int("".join(address_bin), 2)] = int(i[1], 2)

print(f"why in god's green earth are these numbers 36-bit: {sum(p1mem.values())}")
print(
    f"but anyways, it's a good thing there weren't larger than like 16 X's in a mask: {sum(p2mem.values())}"
)
