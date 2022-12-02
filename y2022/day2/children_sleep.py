PLAY_SCORE = {"A": 1, "B": 2, "C": 3}
P1_MAPPING = {"X": "A", "Y": "B", "Z": "C"}
BEATS = {"A": "C", "B": "A", "C": "B"}  # BEATS[x] = what does x win against?
LOSES = {k: v for v, k in BEATS.items()}  # LOSES[x] = what does x lose against?

LOSE = 0
DRAW = 3
WIN = 6

strat = []
with open("one_eye_open.txt") as read:
    for i in read.readlines():
        them, me = i.split()
        strat.append((them, me))

p1_score = 0
p2_score = 0
for them, me in strat:
    my_play = P1_MAPPING[me]
    p1_score += PLAY_SCORE[my_play]
    if my_play == them:
        p1_score += DRAW
    elif BEATS[my_play] == them:
        p1_score += WIN
    elif LOSES[my_play] == them:
        p1_score += LOSE

    if me == "X":
        p2_score += LOSE
        p2_score += PLAY_SCORE[BEATS[them]]
    elif me == "Y":
        p2_score += DRAW
        p2_score += PLAY_SCORE[them]
    elif me == "Z":
        p2_score += WIN
        p2_score += PLAY_SCORE[LOSES[them]]

print(f"i was literally reciting rock paper scissors out loud lol: {p1_score}")
print(f"and i still managed to choke hard on p2: {p2_score}")
