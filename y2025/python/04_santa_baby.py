import sys

THRESH = 4


def neighbors8(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


arr = [list(row.strip()) for row in sys.stdin]

accessible = 0
first_time = -1
while True:
    doable = set()
    for r in range(len(arr)):
        for c in range(len(arr[0])):
            if arr[r][c] != "@":
                continue

            adj = sum(arr[nr][nc] == "@" for nr, nc in neighbors8(r, c, len(arr), len(arr[0])))
            if adj < 4:
                doable.add((r, c))

    if not doable:
        break

    for r, c in doable:
        arr[r][c] = "."

    accessible += len(doable)
    if first_time == -1:
        first_time = len(doable)

print(f"HOLY CHOKE: {first_time}")
print(f"at least p2 was fast... {accessible}")
