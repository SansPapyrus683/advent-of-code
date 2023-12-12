from typing import Optional, Callable
from hashlib import md5
from collections import defaultdict
from itertools import count
from functools import cache

SALT = "qzyelonm"
KEY_NUM = 64


@cache
def normal_hash(ind: int) -> str:
    return md5((SALT + str(ind)).encode()).hexdigest()


@cache
def stretched_hash(ind: int) -> str:
    hsh = normal_hash(ind)
    for _ in range(2016):
        hsh = md5(hsh.encode()).hexdigest()
    return hsh


def keys(n: int, hash_func: Callable[[int], str]) -> list[int]:
    def first_consec3(hsh: str) -> Optional[str]:
        for i in range(len(hsh) - 2):
            if hsh[i] == hsh[i + 1] == hsh[i + 2]:
                return hsh[i]
        return None

    def consec5(hsh: str) -> set[str]:
        res = set()
        for i in range(len(hsh) - 4):
            if hsh[i] == hsh[i + 1] == hsh[i + 2] == hsh[i + 3] == hsh[i + 4]:
                res.add(hsh[i])
        return res

    consec5_occs = defaultdict(int)
    for i in range(1, 10 ** 3 + 1):
        for c in consec5(hash_func(i)):
            consec5_occs[c] += 1

    inds = []
    for i in count(0):
        to_find = first_consec3(hash_func(i))
        if to_find is not None and consec5_occs[to_find] > 0:
            inds.append(i)
            if len(inds) == n:
                break

        to_remove = i + 1
        for c in consec5(hash_func(to_remove)):
            consec5_occs[c] -= 1

        to_add = 10 ** 3 + i + 1
        for c in consec5(hash_func(to_add)):
            consec5_occs[c] += 1
        assert all(i >= 0 for i in consec5_occs.values())
    return inds


print(f"p1 {KEY_NUM} hash end: {keys(KEY_NUM, normal_hash)[-1]}")
print(f"p2 {KEY_NUM} hash end: {keys(KEY_NUM, stretched_hash)[-1]}")
