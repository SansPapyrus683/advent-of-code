INIT = "01111001100111011"
P1_LEN = 272
P2_LEN = 35651584


def checksum(string: str) -> str:
    res = []
    for i in range(len(string) // 2):
        res.append(str(int(string[i * 2] == string[i * 2 + 1])))
    res = "".join(res)
    return res if len(res) % 2 == 1 else checksum(res)


def fill_disk(sz: int) -> str:
    filled = INIT
    while len(filled) < sz:
        # there's probably a faster way to do this, but oh well
        rev = "".join("1" if c == "0" else "0" for c in reversed(filled))
        filled = filled + "0" + rev
    return filled[:sz]


print(f"checksum for disk 1: {checksum(fill_disk(P1_LEN))}")
print(f"checksum for disk 2: {checksum(fill_disk(P2_LEN))}")
