WIN = 1000
ROLL_AMT = 3
MAX_POS = 10


class Die:
    def __init__(self, max_roll: int):
        assert 1 <= max_roll
        self.max = max_roll
        self.val = 1

    def roll(self) -> int:
        rolled = self.val
        self.val += 1
        if self.val > self.max:
            self.val = 1
        return rolled


p1_pos = 8
p2_pos = 6
p1_score = 0
p2_score = 0
turn = True  # true for p1, false for p2
die = Die(100)
roll_num = 0
result = -1
while True:
    result = sum(die.roll() for _ in range(ROLL_AMT))
    roll_num += ROLL_AMT
    if turn:
        p1_pos += result
        p1_pos = MAX_POS if p1_pos % MAX_POS == 0 else p1_pos % MAX_POS
        p1_score += p1_pos
        if p1_score >= WIN:
            result = roll_num * p2_score
            break
    else:
        p2_pos += result
        p2_pos = MAX_POS if p2_pos % MAX_POS == 0 else p2_pos % MAX_POS
        p2_score += p2_pos
        if p2_score >= WIN:
            result = roll_num * p1_score
            break
    turn = not turn

print(f"these games are so stupid lol: {result}")
