import sys

THRESH = 4


def neighbors8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


arr = [list(row.strip()) for row in sys.stdin]

row_num = len(arr)
col_num = len(arr[0])

cleared = set()
for r in range(len(arr)):
    for c in range(len(arr[r])):
        adj = sum(arr[nr][nc] == "@" for nr, nc in neighbors8(r, c, row_num, col_num))
        if arr[r][c] == "@" and adj < THRESH:
            cleared.add((r, c))

print(f"HOLY CHOKE: {len(cleared)}")

# not sure if there's a more elegant way to implement this floodfill...
frontier = list(cleared)
while frontier:
    curr = frontier.pop()
    arr[curr[0]][curr[1]] = "."
    for r, c in neighbors8(*curr, row_num, col_num):
        if (r, c) in cleared:
            continue

        adj = sum(arr[nr][nc] == "@" for nr, nc in neighbors8(r, c, row_num, col_num))
        if arr[r][c] == "@" and adj < THRESH:
            frontier.append((r, c))
            cleared.add((r, c))

print(f"at least p2 was fast... {len(cleared)}")
