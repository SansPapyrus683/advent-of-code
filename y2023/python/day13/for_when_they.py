ReflLine = tuple[bool, int] | None

ASH = "."
ROCK = "#"


def group(seq, sep):
    ret = []
    for el in seq:
        if el == sep:
            yield ret
            ret = []
        else:
            ret.append(el)
    yield ret


def find(mirror: list[list[str] | str], bad: ReflLine) -> ReflLine:
    for v in range(len(mirror[0]) - 1):
        check = min(v + 1, len(mirror[0]) - v - 1)
        for i in range(check):
            up = [r[v - i] for r in mirror]
            right = [r[v + i + 1] for r in mirror]
            if up != right:
                break
        else:
            if (True, v + 1) != bad:
                return True, v + 1

    for h in range(len(mirror) - 1):
        check = min(h + 1, len(mirror) - h - 1)
        for i in range(check):
            if mirror[h - i] != mirror[h + i + 1]:
                break
        else:
            if (False, h + 1) != bad:
                return False, h + 1

    return None


with open("put_it_on_his_head.txt") as read:
    mirrors = []
    for m in group(read.readlines(), "\n"):
        mirrors.append([list(r.strip()) for r in m])

p1_vert, p1_horiz = 0, 0
p2_vert, p2_horiz = 0, 0
for arr in mirrors:
    init_refl = find(arr, None)
    if init_refl[0]:
        p1_vert += init_refl[1]
    else:
        p1_horiz += init_refl[1]

    found_smudge = False
    for r in range(len(arr)):
        for c in range(len(arr[0])):
            arr[r][c] = ASH if arr[r][c] == ROCK else ROCK
            refl = find(arr, init_refl)
            if refl is not None and refl != init_refl:
                if refl[0]:
                    p2_vert += refl[1]
                else:
                    p2_horiz += refl[1]
                found_smudge = True
                break

            # revert changes
            arr[r][c] = ASH if arr[r][c] == ROCK else ROCK
        if found_smudge:
            break

print(f"i just wasn't up to it today lol: {p1_vert + 100 * p1_horiz}")
print(f"spent 5 mins on off by one: {p2_vert + 100 * p2_horiz}")
