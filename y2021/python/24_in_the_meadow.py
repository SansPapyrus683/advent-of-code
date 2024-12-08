import re
import sys

TO_MATCH = r"""
inp w
mul x 0
add x z
mod x 26
div z (1|26)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (-?\d+)
mul y x
add z y
""".strip()


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_valid(
        divs: list[int], val1: list[int], val2: list[int], most: bool = True
) -> int:
    assert len(divs) == len(val1) == len(val2)
    assert sorted(set(divs)) == [1, 26]
    range_ = range(1, 10) if most else range(9, 0, -1)
    valid = -1

    def process(w: int, z: int, ind_at: int):
        x = z % 26
        z //= divs[ind_at]
        x = int((x + val1[ind_at]) != w)
        y = 25 * x + 1
        z *= y
        y = (w + val2[ind_at]) * x
        z += y
        return z

    def solve(z: int, ind_at: int, curr: list[int]):
        nonlocal valid
        if ind_at == len(divs):
            valid = int("".join(str(d) for d in curr))
            return True
        if divs[ind_at] == 26:
            req = (z % 26) + val1[ind_at]
            if 1 <= req <= 9:
                new_z = process(req, z, ind_at)
                return solve(new_z, ind_at + 1, curr + [req])
            else:
                return False
        else:
            for d in range_:
                new_z = process(d, z, ind_at)
                assert new_z // (z + 1) <= 26
                success = solve(new_z, ind_at + 1, curr + [d])
                if success:
                    break

    solve(0, 0, [])
    return valid


instructions = [i.strip() for i in sys.stdin]
segments = chunks(instructions, 18)
div_by = []
value1 = []
value2 = []
for s in segments:
    s = "\n".join(s)
    assert re.match(TO_MATCH, s), "the day1.txt should be like that regex str"
    values = [int(v) for v in next(iter(re.findall(TO_MATCH, s)))]
    for add_to, v in zip([div_by, value1, value2], values):
        add_to.append(v)

smallest = get_valid(div_by, value1, value2)
largest = get_valid(div_by, value1, value2, False)

print(f"honestly today was more math than coding: {smallest}")
print(f"but yesterday also existed, so idk what i was expecting: {largest}")
