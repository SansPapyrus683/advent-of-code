from collections import defaultdict
from functools import cmp_to_key
from collections.abc import Collection

P1_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
P2_ORDER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def prio(hand: Collection[str]) -> int:
    assert len(hand) == 5
    counts = defaultdict(int)
    for c in hand:
        counts[c] += 1

    if len(set(hand)) == 1:
        return 8
    elif 4 in counts.values():
        return 7
    elif 3 in counts.values() and 2 in counts.values():
        return 6
    elif 3 in counts.values():
        return 5
    elif list(counts.values()).count(2) == 2:
        return 4
    elif 2 in counts.values():
        return 3
    elif len(counts) == 5:
        return 2
    return 1


def joker_prio(hand: Collection[str]) -> int:
    j_inds = [v for v, c in enumerate(hand) if c == "J"]

    hand = list(hand)
    max_ = prio(hand)
    for o in P2_ORDER:
        for i in j_inds:
            hand[i] = o
        max_ = max(max_, prio(hand))
    return max_


def raw_cmp(a: str, b: str, order: list[str]) -> int:
    for x, y in zip(a, b):
        if x != y:
            return order.index(y) - order.index(x)
    return 0


def p1_cmp(a: tuple[str, int], b: tuple[str, int]) -> int:
    a_prio = prio(a[0])
    b_prio = prio(b[0])
    if a_prio != b_prio:
        return a_prio - b_prio
    return raw_cmp(a[0], b[0], P1_ORDER)


def p2_cmp(a: tuple[str, int], b: tuple[str, int]) -> int:
    a_prio = joker_prio(a[0])
    b_prio = joker_prio(b[0])
    if a_prio != b_prio:
        return a_prio - b_prio
    return raw_cmp(a[0], b[0], P2_ORDER)


def tot_winnings(ranks: list[tuple[str, int]]) -> int:
    tot = 0
    for v, (_, bet) in enumerate(ranks):
        tot += (v + 1) * bet
    return tot


hands = []
with open("fairy_tale.txt") as read:
    for h in read.readlines():
        h = h.split()
        hands.append((h[0], int(h[1])))

hands.sort(key=cmp_to_key(p1_cmp))
print(f"OMG TOP 10 FOR P1: {tot_winnings(hands)}")

hands.sort(key=cmp_to_key(p2_cmp))
print(f"seriously though what is this inconsistency: {tot_winnings(hands)}")
