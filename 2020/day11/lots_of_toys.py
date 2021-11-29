from functools import lru_cache


@lru_cache(None)  # this thing is fricking WONDERFUL
def p1_neighbors(row: int, col: int, r_max: int, c_max: int) -> [(int, int)]:
    return [p for p in [
        (row + 1, col), (row - 1, col),
        (row, col + 1), (row, col - 1),
        (row + 1, col + 1), (row + 1, col - 1),
        (row - 1, col - 1), (row - 1, col + 1)
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


@lru_cache(None)
def p2_neighbors(row: int, col: int, r_max: int, c_max: int, seats: [str]):
    neighbor_funcs = [
        lambda x, y: (x + 1, y),
        lambda x, y: (x - 1, y),
        lambda x, y: (x, y - 1),
        lambda x, y: (x, y + 1),
        lambda x, y: (x + 1, y + 1),
        lambda x, y: (x + 1, y - 1),
        lambda x, y: (x - 1, y + 1),
        lambda x, y: (x - 1, y - 1),
    ]
    neighbor_pos = []
    for f in neighbor_funcs:
        at = f(row, col)
        if not (0 <= at[0] < r_max and 0 <= at[1] < c_max):
            continue

        while seats[at[0]][at[1]] == '.':
            at = f(at[0], at[1])
            if not (0 <= at[0] < r_max and 0 <= at[1] < c_max):
                break
        else:
            neighbor_pos.append(at)
    return neighbor_pos


with open('on_sleigh.txt') as read:
    seats = [line.rstrip() for line in read.readlines()]
backup_seats = seats.copy()

max_r = len(seats)
max_c = len(seats[0])

while True:
    new_seats = []
    for r in range(max_r):
        new_row = ''
        for c in range(max_c):
            neighbors = p1_neighbors(r, c, max_r, max_c)
            if seats[r][c] == 'L' and \
                    all(seats[i][j] != '#' for i, j in neighbors):
                new_row += '#'
            elif seats[r][c] == '#' and \
                    sum(seats[i][j] == '#' for i, j in neighbors) >= 4:
                new_row += 'L'
            else:
                new_row += seats[r][c]
        new_seats.append(new_row)
    if new_seats == seats:
        seats = new_seats
        break
    seats = new_seats
print("this ran slower than expected, oof: %i" % sum(r.count('#') for r in seats))

seats = backup_seats  # reset for part 2
tupled_seats = tuple(seats)  # 2021 me: why the hell did i need this
while True:
    new_seats = []
    for r in range(max_r):
        new_row = ''
        for c in range(max_c):
            neighbors = p2_neighbors(r, c, max_r, max_c, tupled_seats)
            if seats[r][c] == 'L' and \
                    all(seats[i][j] != '#' for i, j in neighbors):
                new_row += '#'
            elif seats[r][c] == '#' and \
                    sum(seats[i][j] == '#' for i, j in neighbors) >= 5:
                new_row += 'L'
            else:
                new_row += seats[r][c]
        new_seats.append(new_row)
    if new_seats == seats:
        seats = new_seats
        break
    seats = new_seats
print("don't you hate it when you have too segments "
      "that are so similar but just different enough so that "
      f"they can't be made into a function: {sum(r.count('#') for r in seats)}")
