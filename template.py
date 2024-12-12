import sys
from typing import TypeVar
import collections.abc as abc
from collections import defaultdict as dd, deque as dq
from itertools import permutations as perm, combinations as combi
from copy import deepcopy as dc


# region utility
T = TypeVar("T")


def a2i(a: abc.Iterable[str]) -> list[int]:
    return [int(i) for i in a]


def add(first, second):
    return type(first)(f + s for f, s in zip(first, second))


def sub(first, second):
    return type(first)(f - s for f, s in zip(first, second))


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


def n4r(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def n4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


def n8r(r: int, c: int) -> list[tuple[int, int]]:
    return [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ]


def n8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
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


def gi(grid: list[abc.Sequence[T]]) -> abc.Generator[tuple[int, int, T]]:
    assert len({len(r) for r in grid}) == 1
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            yield r, c, grid[r][c]


def get(grid: list[list], r: int, c: int):
    return grid[r][c] if 0 <= r < len(grid) and 0 <= c < len(grid[r]) else None
# endregion

# even indices are the 4 cardinal directions, you can + mod 2 to turn right or - mod 2 to turn left
DIRS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

arr = []
acc = 0
# acc = float("inf")  # depends, usually it asks for the sum or the minimum
raw = sys.stdin.read().strip()
sys.stdin.seek(0)
for v, g in enumerate(group(sys.stdin.readlines(), "\n")):
    for l in g:
        l = l.strip()

print(arr)
