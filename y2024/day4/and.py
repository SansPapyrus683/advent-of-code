DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

with open("mistletoe.txt") as read:
    grid = [row.strip() for row in read]

row_num = len(grid)
col_num = len(grid[0])

p1_count = 0
p2_count = 0
for r in range(len(grid)):
    for c in range(len(grid[r])):
        for d in DIRS:
            word = ""
            at = r, c
            for _ in range(4):
                if not (0 <= at[0] < row_num and 0 <= at[1] < col_num):
                    break
                word += grid[at[0]][at[1]]
                at = at[0] + d[0], at[1] + d[1]
            p1_count += word == "XMAS"

        if not (0 < r < len(grid) - 1 and 0 < c < len(grid[r]) - 1):
            continue

        corners = "".join(
            [grid[r - 1][c - 1], grid[r - 1][c + 1], grid[r + 1][c + 1], grid[r + 1][c - 1]]
        )
        p2_count += grid[r][c] == "A" and corners in {"MMSS", "SMMS", "SSMM", "MSSM"}

print(f"yeah it's cooked, no lb today: {p1_count}")
print(f"what i'm rlly salty is how gpt got p1 first try: {p2_count}")
