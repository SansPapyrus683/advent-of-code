import sys

DELTAS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
EXPAND = {"#": "##", "@": "@.", ".": "..", "O": "[]"}

grid = []
row = input()
while row:
    grid.append("".join(EXPAND[c] for c in row))
    row = input()

moves = [c for c in sys.stdin.read() if c in DELTAS]

boxes = set()
bad = set()
start = None
for r in range(len(grid)):
    for c, cell in enumerate(grid[r]):
        if cell == "[":
            boxes.add((r, c))
        elif cell == "#":
            bad.add((r, c))
        elif cell == "@":
            start = r, c
assert start is not None

at = start
get_box = lambda pt: next((p for p in [pt, (pt[0], pt[1] - 1)] if p in boxes), None)
for d in map(lambda c: DELTAS[c], moves):
    adj = at[0] + d[0], at[1] + d[1]
    if adj in bad:
        continue

    if (box_adj := get_box(adj)) is not None:
        if adj[0] != at[0]:  # move up or down
            levels = [{box_adj}]
            has_bad = False
            while levels[-1] and not has_bad:
                levels.append(set())
                for prev in levels[-2]:
                    cand = [(prev[0] + d[0], prev[1]), (prev[0] + d[0], prev[1] + 1)]
                    for c in cand:
                        if c in bad:
                            has_bad = True
                            levels[-1].add(c)
                        if (box := get_box(c)) is not None:
                            levels[-1].add(box)

            if has_bad:
                continue

            for l in reversed(levels):
                for b in l:
                    boxes.remove(b)
                    boxes.add((b[0] + d[0], b[1]))  # d[1] = 0 anyways

        elif adj[1] != at[1]:  # move left or right
            path = [box_adj]
            while (prev := path[-1]) in boxes:
                path.append((prev[0], prev[1] + d[1] + d[1]))

            last_box = path[-2]
            poss = [(last_box[0], last_box[1] - 1), (last_box[0], last_box[1] + 2)]
            if any(pt in bad for pt in poss):
                continue

            for b in path[:-1]:
                boxes.remove(b)
                boxes.add((b[0], b[1] + d[1]))  # here, d[0] = 0 yeah

    at = adj

pos_sum = sum(100 * r + c for r, c in boxes)
print(f"but oh my GOD i was stuck for nearly an hour on p2: {pos_sum}")
