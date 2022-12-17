START_X = 2  # how far from the left wall you have to be
START_Y = 3  # how far above the last rock you have to be
WIDTH = 7

ORDER = [
    ['####'],
    ['.#.', '###', '.#.'],
    ['..#', '..#', '###'],
    ['#', '#', '#', '#'],
    ['##', '##']
]

P1_ROCK_NUM = 2022
P2_ROCK_NUM = 1000000000000
LOOKBACK = 100

with open("joy_and_laughter.txt") as read:
    jets = read.read().strip()

height = 0
curr_rock = 0
rock = ORDER[curr_rock]
pos = [1 + START_X, height + START_Y + len(rock)]
tower = [[False for _ in range(WIDTH + 2)] for _ in range(10000)]
for c in range(WIDTH + 2):
    tower[0][c] = True
for t in tower:
    t[0] = t[-1] = True

rock_num = 0
history_seq = []
history = {}
jet_at = 0
rep_state = None
while True:
    pos[0] += 1 if jets[jet_at] == ">" else -1

    valid = True
    for r in range(len(rock)):
        for c in range(len(rock[r])):
            if rock[r][c] == "#" and tower[pos[1] - r][pos[0] + c]:
                valid = False
                break

    if not valid:
        pos[0] += -1 if jets[jet_at] == ">" else 1

    pos[1] -= 1
    valid = True  # yes, this is a duplicated code section, sue me
    for r in range(len(rock)):
        for c in range(len(rock[r])):
            if rock[r][c] == "#" and tower[pos[1] - r][pos[0] + c]:
                valid = False
                break

    if not valid:
        pos[1] += 1

        prev_h = height
        height = max(height, pos[1])

        prev_rows = ""
        for r in tower[max(prev_h - LOOKBACK, 0):prev_h]:
            prev_rows += "".join("#" if c else " " for c in r)
        state = (jet_at, curr_rock, prev_rows)
        if state in history:
            rep_state = state
            history_seq.append(state)
            break
        history[state] = height - prev_h
        history_seq.append(state)

        for r in range(len(rock)):
            for c in range(len(rock[r])):
                if rock[r][c] == "#":
                    tower[pos[1] - r][pos[0] + c] = True

        curr_rock = (curr_rock + 1) % len(ORDER)
        rock = ORDER[curr_rock]
        pos = [1 + START_X, height + START_Y + len(rock)]
        rock_num += 1

    jet_at = (jet_at + 1) % len(jets)

assert rep_state is not None

cyc_start = history_seq.index(rep_state)
cyc_len = len(history) - cyc_start
cyc_add = 0
for i in range(cyc_start, cyc_start + cyc_len):
    cyc_add += history[history_seq[i]]

total_p1 = 0
for i in range(min(cyc_start, P1_ROCK_NUM)):
    total_p1 += history[history_seq[i]]

rem = P1_ROCK_NUM - cyc_start
if rem >= 0:
    cyc_amt, rem = divmod(rem, cyc_len)
    total_p1 += cyc_add * cyc_amt

    for i in range(cyc_start, cyc_start + rem):
        total_p1 += history[history_seq[i]]

total_p2 = 0
for i in range(min(cyc_start, P2_ROCK_NUM)):
    total_p2 += history[history_seq[i]]

rem = P2_ROCK_NUM - cyc_start
if rem >= 0:
    cyc_amt, rem = divmod(rem, cyc_len)
    total_p2 += cyc_add * cyc_amt

    for i in range(cyc_start, cyc_start + rem):
        total_p2 += history[history_seq[i]]

print(f"this is literally tetris: {total_p1}")
print(f"bruh do the elephants know how large ONE TRILLION IS: {total_p2}")
