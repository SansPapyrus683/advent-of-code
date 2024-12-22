import sys
from functools import cache
from itertools import permutations

P1_ROBOTS = 2
P2_ROBOTS = 25

# disgusting
KEYPAD = ["789", "456", "123", " 0A"]
KEY_POS = {
    KEYPAD[r][c]: (r, c) for r in range(len(KEYPAD)) for c in range(len(KEYPAD[r]))
}
ARROWS = [" ^A", "<v>"]
ARROW_POS = {
    ARROWS[r][c]: (r, c) for r in range(len(ARROWS)) for c in range(len(ARROWS[r]))
}
MOVES = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def delta_string(delta: tuple[int, int]) -> str:
    res = []
    for _ in range(abs(delta[0])):
        res.append("^v"[delta[0] > 0])
    for _ in range(abs(delta[1])):
        res.append("<>"[delta[1] > 0])
    return "".join(res)


@cache
def min_moves(arrows: str, robots: int) -> int:
    if robots == 0:
        return len(arrows)

    pos = [ARROW_POS["A"], *(ARROW_POS[a] for a in arrows)]
    best = 0
    for i in range(1, len(pos)):
        at, prev_at = pos[i], pos[i - 1]
        moves = delta_string((at[0] - prev_at[0], at[1] - prev_at[1]))
        this_best = float("inf")
        for move_p in permutations(moves):
            temp_at = prev_at
            for m in move_p:
                temp_at = temp_at[0] + MOVES[m][0], temp_at[1] + MOVES[m][1]
                if ARROWS[temp_at[0]][temp_at[1]] == " ":
                    break
            else:
                this_best = min(this_best, min_moves("".join(move_p) + "A", robots - 1))
        best += this_best
    return best


p1_complexity = p2_complexity = 0
for code in sys.stdin:
    code = code.strip()
    pos = [KEY_POS["A"], *(KEY_POS[c] for c in code)]

    p1_presses = 0
    p2_presses = 0
    for i in range(1, len(pos)):
        at, prev_at = pos[i], pos[i - 1]
        moves = delta_string((at[0] - prev_at[0], at[1] - prev_at[1]))
        p1_best = p2_best = float("inf")
        for move_p in permutations(moves):
            temp_at = prev_at
            for m in move_p:
                temp_at = temp_at[0] + MOVES[m][0], temp_at[1] + MOVES[m][1]
                if KEYPAD[temp_at[0]][temp_at[1]] == " ":
                    break
            else:
                p1_best = min(p1_best, min_moves("".join(move_p) + "A", P1_ROBOTS))
                p2_best = min(p2_best, min_moves("".join(move_p) + "A", P2_ROBOTS))
        p1_presses += p1_best
        p2_presses += p2_best

    int_part = int(code[:-1])
    p1_complexity += p1_presses * int_part
    p2_complexity += p2_presses * int_part

print(f"lmao i got top 10 for part 1: {p1_complexity}")
print(f"but then i had to go spent time w/ fam so died on p2: {p2_complexity}")
