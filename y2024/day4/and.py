DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

with open("mistletoe.txt") as read:
    arr = [row.strip() for row in read]

row_num = len(arr)
col_num = len(arr[0])

p1_count = 0
p2_count = 0
for r in range(len(arr)):
    for c in range(len(arr[r])):
        for d in DIRS:
            word = ""
            at = r, c
            for _ in range(4):
                if not (0 <= at[0] < row_num and 0 <= at[1] < col_num):
                    break
                word += arr[at[0]][at[1]]
                at = at[0] + d[0], at[1] + d[1]
            p1_count += word == "XMAS"

        if not (0 < r < len(arr) - 1 and 0 < c < len(arr[r]) - 1):
            continue

        corners = "".join(
            [arr[r - 1][c - 1], arr[r - 1][c + 1], arr[r + 1][c + 1], arr[r + 1][c - 1]]
        )
        p2_count += arr[r][c] == "A" and corners in {"MMSS", "SMMS", "SSMM", "MSSM"}

print(f"yeah it's cooked, no lb today: {p1_count}")
print(f"what i'm rlly salty is how gpt got p1 first try: {p2_count}")
