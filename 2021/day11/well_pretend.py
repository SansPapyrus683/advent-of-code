P1_STEP_NUM = 100


def neighbors(r: int, c: int, r_max: int, c_max: int) -> [(int, int)]:
    test_neighbors = [
        (r, c + 1),
        (r, c - 1),
        (r + 1, c),
        (r - 1, c),
        (r + 1, c - 1),
        (r - 1, c + 1),
        (r - 1, c - 1),
        (r + 1, c + 1),
    ]
    return [n for n in test_neighbors if 0 <= n[0] < r_max and 0 <= n[1] < c_max]


with open("hes_parson_brown.txt") as read:
    octo = [[int(i) for i in r.strip()] for r in read.readlines()]

row_amt = len(octo)
col_amt = len(octo[0])

flashes = 0
step_num = 0
while True:
    for r in range(row_amt):
        for c in range(col_amt):
            octo[r][c] += 1

    flashed = [[False for _ in range(col_amt)] for _ in range(row_amt)]
    while True:
        # if only i knew to use numpy from the start
        to_add = [[0 for _ in range(col_amt)] for _ in range(row_amt)]
        for r in range(row_amt):
            for c in range(col_amt):
                if not flashed[r][c] and octo[r][c] > 9:
                    flashed[r][c] = True
                    flashes += 1
                    for n in neighbors(r, c, row_amt, col_amt):
                        to_add[n[0]][n[1]] += 1

        can_flash = False
        for r in range(row_amt):
            for c in range(col_amt):
                octo[r][c] += to_add[r][c]
                if not flashed[r][c] and octo[r][c] > 9:
                    can_flash = True

        if not can_flash:
            break

    for r in range(row_amt):
        for c in range(col_amt):
            if flashed[r][c]:
                octo[r][c] = 0

    step_num += 1
    if step_num == P1_STEP_NUM:
        print(f"bruh i threw this one so hard ahahaha: {flashes}")
    if all(all(i for i in r) for r in flashed):
        break

print(f"at least i didn't have to worry about optimization: {step_num}")
