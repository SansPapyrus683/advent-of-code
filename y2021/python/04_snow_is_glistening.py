import sys
from sys import exit

LEN = 5


# bruh what kinda bingo game doesn't have diagonals
def won(have: list[list[bool]]) -> bool:
    for r in range(LEN):
        if all(have[r]):
            return True
    for c in range(LEN):
        if all(have[r][c] for r in range(LEN)):
            return True
    return False


# this is a really, really weird way to calculate the score tho
def score(board_nums: list[list[int]], have: list[list[bool]], last_num: int) -> int:
    total = 0
    for r in range(LEN):
        for c in range(LEN):
            total += board_nums[r][c] * (not have[r][c])
    return total * last_num


nums = [int(i) for i in input().split(",")]
boards = sys.stdin.readlines()
new_board = []
for i in range(len(boards) // (LEN + 1)):
    board = boards[i * (LEN + 1) : (i + 1) * (LEN + 1)]
    board = [[int(i) for i in b.split()] for b in board[1:]]
    new_board.append(board)
boards = new_board

first_alr = False
won_alr = [False] * len(boards)
selected = [
    [[False for _ in range(LEN)] for _ in range(LEN)] for _ in range(len(boards))
]
first_score = -1
last_score = -1
for n in nums:
    for r in range(LEN):
        for c in range(LEN):
            for v, b in enumerate(boards):
                if b[r][c] == n:
                    selected[v][r][c] = True
                if won(selected[v]):
                    won_alr[v] = True
                    if not first_alr:
                        first_alr = True
                        print(f"p1: {first_score}")
                        first_score = score(b, selected[v], n)

                    if all(won_alr):
                        last_score = score(b, selected[v], n)
                        print(f"p2: {last_score}")
                        exit()
