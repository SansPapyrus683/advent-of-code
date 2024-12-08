from collections import defaultdict
from itertools import product

WIN = 21


# turn is true if it's player 1, false if it's player 2
def neighbors(
        p1p: int, p2p: int, p1s: int, p2s: int, turn: bool
) -> list[tuple[int, int, int, int]]:
    sum_amt = 3
    max_roll = 3
    all_sums = [sum(rolls) for rolls in product(
        [r for r in range(1, max_roll + 1)], repeat=sum_amt)
                ]

    max_pos = 10
    poss = []
    for s in all_sums:
        # np = next position, ns = next score
        if turn:
            np = p1p + s
            np = max_pos if np % max_pos == 0 else np % max_pos
            ns = p1s + np
            poss.append((np, p2p, ns, p2s))
        else:
            np = p2p + s
            np = max_pos if np % max_pos == 0 else np % max_pos
            ns = p2s + np
            poss.append((p1p, np, p1s, ns))
    return poss


states = defaultdict(int)
# player 1 & 2's position followed by their score
states[(8, 6, 0, 0)] = 1
p1_win = 0
p2_win = 0
curr_turn = True
while states:
    next_states = defaultdict(int)
    for curr, amt in states.items():
        for n in neighbors(*curr, curr_turn):
            if n[2] >= WIN:
                p1_win += amt
            elif n[3] >= WIN:
                p2_win += amt
            else:
                next_states[n] += amt
    states = next_states
    curr_turn = not curr_turn

print(f"does god even have enough storage for all these universes: {max(p1_win, p2_win)}")
