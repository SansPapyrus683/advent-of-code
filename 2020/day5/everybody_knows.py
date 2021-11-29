ROW_POW = 7
COL_POW = 3

with open('something_lol.txt') as read:
    boarding_passes = [[p[:ROW_POW], p[ROW_POW:ROW_POW + COL_POW].rstrip()] for p in read.readlines()]

seat_ids = []
for b in boarding_passes:
    row_lo = 0
    row_hi = 2 ** ROW_POW
    for i in b[0]:  # doing all that binary searching for usaco did help, neat
        if i == 'B':
            row_lo = (row_lo + row_hi) // 2
        elif i == 'F':
            row_hi = (row_lo + row_hi) // 2
        else:
            raise ValueError("wait are you sure your input's valid?")

    col_lo = 0
    col_hi = 2 ** COL_POW
    for i in b[1]:
        if i == 'R':
            col_lo = (col_lo + col_hi) // 2
        elif i == 'L':
            col_hi = (col_lo + col_hi) // 2
        else:
            raise ValueError("wait are you sure your input's valid?")
    seat_ids.append(row_lo * (ROW_POW + 1) + col_lo)

print(f"wait lol it's day 5 and we're STILL on the plane? bruh... {max(seat_ids)}")
for i in range(min(seat_ids) + 1, max(seat_ids)):  # get the lower and upper bound for all the seats
    if i not in seat_ids:
        print(f"wait aren't online boarding passes a thing? couldn't we've just looked there: {i}")
        break
