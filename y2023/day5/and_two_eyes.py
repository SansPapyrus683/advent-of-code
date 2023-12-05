import re


def group(seq, sep):
    ret = []
    for el in seq:
        if el == sep:
            yield ret
            ret = []
        else:
            ret.append(el)
    yield ret


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def inter(a_start: int, a_end: int, b_start: int, b_end: int) -> tuple[int, int] | None:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return None if start > end else (start, end)


def seed_to_loc(
        seed_start: int, seed_end: int,
        ranges: dict[str, tuple[str, list[list[int]]]]
) -> list[tuple[int, int]]:
    at = "seed"
    seed_at = [(seed_start, seed_end)]
    while at != "location":
        at, matches = ranges[at]
        next_up = []
        for r in seed_at:
            inters = []
            for dest, start, amt in matches:
                inter_ = inter(*r, start, start + amt - 1)
                if inter_ is not None:
                    offset = -start + dest
                    next_up.append((inter_[0] + offset, inter_[1] + offset))
                    inters.append(inter_)  # to calculate the subtractions

            inters.sort()
            last = r[0]
            for i in inters:
                if i[0] > last:
                    next_up.append((last, i[0] - 1))
                last = i[1] + 1
            if r[1] >= last:
                next_up.append((last, r[1]))

        seed_at = next_up

    return seed_at


with open("made_outta_coal.txt") as read:
    lines = read.readlines()
    parts = list(group(lines, "\n"))
    seeds = [int(i) for i in parts[0][0].split(":")[1].split()]

    mappings = {}
    patt = r"^([a-zA-Z]+)-to-([a-zA-Z]+) map:$"
    for p in parts[1:]:
        matching = re.match(patt, p[0])
        from_ = matching.group(1)
        to = matching.group(2)
        mappings[from_] = to, []
        for m in p[1:]:
            mappings[from_][1].append([int(i) for i in m.split()])

p1_loc = float("inf")
for s in seeds:
    loc = sorted(seed_to_loc(s, s, mappings))
    p1_loc = min(p1_loc, loc[0][0])


p2_loc = float("inf")
for s_start, s_amt in chunks(seeds, 2):
    loc = sorted(seed_to_loc(s_start, s_start + s_amt - 1, mappings))

    p2_loc = min(p2_loc, loc[0][0])

print(f"actual cancer problem what: {p1_loc}")
print(f"and it's only a day 5: {p2_loc}")
