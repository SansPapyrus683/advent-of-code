# unfortunate, there weren't enough days for all the lyrics

RIGHT = ">"
DOWN = "v"
EMPTY = "."

with open("do_the_job.txt") as read:
    cucumbers = [list(a.strip()) for a in read.readlines()]
for r in cucumbers:
    assert set(r).issubset({RIGHT, DOWN, EMPTY})

row_num = len(cucumbers)
col_num = len(cucumbers[0])

steps = 0
while True:
    moved = False
    for r in range(row_num):
        can_wrap = cucumbers[r][0] == EMPTY
        c = 0
        while c < col_num - 1:
            curr = cucumbers[r][c]
            if curr == RIGHT and cucumbers[r][c + 1] == EMPTY:
                cucumbers[r][c] = EMPTY
                cucumbers[r][c + 1] = RIGHT
                if c + 1 == col_num - 1:
                    can_wrap = False
                c += 2
                moved = True
            else:
                c += 1

        if cucumbers[r][-1] == RIGHT and can_wrap:
            cucumbers[r][-1] = EMPTY
            cucumbers[r][0] = RIGHT
            moved = True

    for c in range(col_num):
        can_wrap = cucumbers[0][c] == EMPTY
        r = 0
        while r < row_num - 1:
            curr = cucumbers[r][c]
            if curr == DOWN and cucumbers[r + 1][c] == EMPTY:
                cucumbers[r][c] = EMPTY
                cucumbers[r + 1][c] = DOWN
                if r + 1 == row_num - 1:
                    can_wrap = False
                r += 2
                moved = True
            else:
                r += 1

        if cucumbers[-1][c] == DOWN and can_wrap:
            cucumbers[-1][c] = EMPTY
            cucumbers[0][c] = DOWN
            moved = True

    steps += 1
    if not moved:
        print(f"can't believe it, i got 95th place globally overall: {steps}")
        break
