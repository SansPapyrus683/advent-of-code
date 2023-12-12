P1_LEN = 10
P2_LEN = 4 * 10 ** 5

SAFE = "."
TRAP = "^"

TRAP_ARRANGEMENTS = (
    (False, False, True),
    (True, False, False),
    (True, True, False),
    (False, True, True)
)

with open("input/day18.txt") as read:
    row = []
    for c in read.readline().strip():
        if c == SAFE:
            row.append(True)
        elif c == TRAP:
            row.append(False)

room = [row]
for r in range(max(P1_LEN, P2_LEN) - 1):
    new = []
    prev = room[-1]
    for i in range(len(prev)):
        left = True if i == 0 else prev[i - 1]
        center = prev[i]
        right = True if i == len(prev) - 1 else prev[i + 1]
        new.append((left, center, right) not in TRAP_ARRANGEMENTS)
    room.append(new)

    if len(room) == P1_LEN:
        print(f"safe tiles for {P1_LEN} rows (p1): {sum(sum(r) for r in room)}")
    elif len(room) == P2_LEN:
        print(f"safe tiles for {P2_LEN} rows (p2): {sum(sum(r) for r in room)}")
