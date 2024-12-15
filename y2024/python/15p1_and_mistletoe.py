import sys

DELTAS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}

grid = []
row = input()
while row:
    grid.append(row)
    row = input()

moves = [c for c in sys.stdin.read() if c in DELTAS]

boxes = set()
bad = set()
start = None
for r in range(len(grid)):
    for c, cell in enumerate(grid[r]):
        if cell == "O":
            boxes.add((r, c))
        elif cell == "#":
            bad.add((r, c))
        elif cell == "@":
            start = r, c
assert start is not None

at = start
for d in map(lambda c: DELTAS[c], moves):
    adj = at[0] + d[0], at[1] + d[1]
    if adj in bad:
        continue

    if adj in boxes:
        trail = [adj]
        while trail[-1] in boxes:
            last = trail[-1]  # shorthand
            trail.append((last[0] + d[0], last[1] + d[1]))

        if trail[-1] in bad:
            continue
        boxes.remove(trail[0])
        boxes.add(trail[-1])

    at = adj

pos_sum = sum(100 * r + c for r, c in boxes)
print(f"oh wow top 100 for p1 today: {pos_sum}")
