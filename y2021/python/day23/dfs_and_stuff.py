import sys
from typing import Union, List
from bisect import bisect

sys.setrecursionlimit(10 ** 5)  # should be large enough

"""
so a config that hypothetically looks like this:
#############
#.....D.D.A.#
###.#B#B#.###
  #A#C#C#.#
  #########
would be represented as such:
[None, None, (A,), None, (C, B), D, (C, B), D, (), A, None]

note that the space right above the hallways doesn't need to be represented
since amphibods will never move there
"""
Amphipods = Union[None, List[str]]


def min_cost(start: Amphipods, costs: dict[int, int], depth: int) -> int:
    order = set()
    for i in start:
        if i is not None:
            assert len(i) == depth
            for a in i:
                order.add(a)
    order = sorted(order)

    hallways = [i for i in range(len(start)) if start[i] is None]
    rooms = [i for i in range(len(start)) if start[i] is not None]
    assert len(rooms) == len(order)
    room_ind = 0
    target = []
    for i in range(len(start)):
        if i not in rooms:
            target.append(None)
        else:
            target.append((order[room_ind],) * depth)
            room_ind += 1

    def all_moves(curr: Amphipods) -> list[tuple[int, Amphipods]]:
        all_next = []
        for t, r in zip(order, rooms):
            if not curr[r] or (len(curr[r]) and all(s == t for s in curr[r])):
                continue

            move_out = curr[r][-1]
            cost = costs[move_out] * (depth + 1 - len(curr[r]))
            left = bisect(hallways, r) - 1
            prev = r
            while left >= 0 and curr[hallways[left]] is None:
                cost += costs[move_out] * (prev - hallways[left])
                new = curr.copy()
                new[r] = new[r][:-1]
                new[hallways[left]] = move_out
                all_next.append((cost, new))
                prev = hallways[left]
                left -= 1

            cost = costs[move_out] * (depth + 1 - len(curr[r]))
            right = bisect(hallways, r)
            prev = r
            while right < len(hallways) and curr[hallways[right]] is None:
                cost += costs[move_out] * (hallways[right] - prev)
                new = curr.copy()
                new[r] = new[r][:-1]
                new[hallways[right]] = move_out
                all_next.append((cost, new))
                prev = hallways[right]
                right += 1

        for v, h in enumerate(hallways):
            if curr[h] is None:
                continue
            dest = rooms[order.index(curr[h])]
            if len(curr[dest]) < depth:
                if len(curr[dest]) > 0 and any(in_ != curr[h] for in_ in curr[dest]):
                    continue
                d_int = bisect(hallways, dest)
                to_check = range(v + 1, d_int) if v < d_int else range(d_int, v)
                if all(curr[hallways[p]] is None for p in to_check):
                    dist = ((abs(h - dest)) + (depth - len(curr[dest])))
                    cost = costs[curr[h]] * dist
                    new = curr.copy()
                    new[h] = None
                    new[dest] = new[dest] + (curr[h],)
                    all_next.append((cost, new))

        return all_next

    sub_mins = {}

    def dfs_calc(curr: Amphipods, cost=0):
        if curr == target or cost > sub_mins.get(tuple(target), float("inf")):
            return
        for c, m in all_moves(curr):
            tm = tuple(m)
            if tm not in sub_mins or cost + c < sub_mins[tm]:
                sub_mins[tm] = cost + c
                dfs_calc(m, cost + c)

    dfs_calc(start)
    return sub_mins.get(tuple(target), -1)
