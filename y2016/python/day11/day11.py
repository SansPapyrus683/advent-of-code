import re


def min_steps(init_pairs: list[tuple[int, int]], top: int) -> int:
    init_pairs = tuple(sorted(init_pairs))

    def move(pairs: list[tuple[int, int]], inds: tuple[int, ...], delta: int):
        pairs = [list(p) for p in pairs]
        for i in inds:
            pairs[i // 2][i % 2] += delta
        return sorted(tuple(p) for p in pairs)

    start = 0
    frontier = [(start, list(init_pairs))]
    visited = {(start, init_pairs)}
    steps = 0
    while frontier:
        next_up = []
        for at, pairs in frontier:
            if all(p == (top, top) for p in pairs):
                return steps

            movable = []
            for i in range(len(pairs) * 2):
                if pairs[i // 2][i % 2] != at:
                    continue
                movable.append((i,))
                for j in range(i + 1, len(pairs) * 2):
                    if pairs[j // 2][j % 2] != at:
                        continue
                    movable.append((i, j))

            for d in [-1, 1]:
                n_at = at + d
                if not 0 <= n_at <= top:
                    continue
                for m in movable:
                    n_pairs = move(pairs, m, d)
                    for c, g in n_pairs:
                        if c != g and any(p[1] == c for p in n_pairs):
                            break
                    else:
                        n_state = n_at, tuple(n_pairs)
                        if n_state not in visited:
                            visited.add(n_state)
                            next_up.append((n_at, n_pairs))

        steps += 1
        frontier = next_up

    raise ValueError("something is wrong")


with open("day11.txt") as read:
    chips, gens = {}, {}
    floor_num = 0
    for f_at, f in enumerate(read.readlines()):
        floor_fmt = "The [a-zA-Z]+ floor contains (.*)"
        res = re.match(floor_fmt, f).group(1)\
            .replace(".", "")\
            .replace("and", ",")\
            .split(",")

        microchip_fmt = r"a ([a-zA-Z]+)\-compatible microchip"
        generator_fmt = r"a ([a-zA-Z]+) generator"
        curr_pairs = []
        for r in res:
            r = r.strip()
            if (res := re.match(microchip_fmt, r)) is not None:
                chips[res.group(1).lower()] = f_at
            elif (res := re.match(generator_fmt, r)) is not None:
                gens[res.group(1).lower()] = f_at
        floor_num += 1

elem_pairs = [(chips[e], gens[e]) for e in chips]
p1_best = min_steps(elem_pairs, floor_num - 1)
print(f"you can get everything to the top floor in {p1_best} steps")

new_elem_pairs = elem_pairs + [(0, 0), (0, 0)]
p2_best = min_steps(new_elem_pairs, floor_num - 1)
print(f"with the additional elements, it's {p2_best} steps")
