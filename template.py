from collections import defaultdict
from itertools import permutations, combinations
from copy import deepcopy


# region utility
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
    """source: https://stackoverflow.com/questions/312443"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def neighbors4raw(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def neighbors8raw(r: int, c: int) -> list[tuple[int, int]]:
    return [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ]


def neighbors8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def inter(a_start: int, a_end: int, b_start: int, b_end: int) -> tuple[int, int] | None:
    """intersection of [a_start, a_end] and [b_start, b_end]"""
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    return None if start > end else (start, end)


def sign(n: int) -> int:
    if n == 0:
        return 0
    return -1 if n < 0 else 1
# endregion


# replace input.txt w/ whatever your thing is
with open("input.txt") as read:
    for g in group(read.readlines(), "\n"):
        for i in g:
            pass
