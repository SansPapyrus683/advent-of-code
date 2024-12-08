import sys

RELEVANT_CYCLES = {20, 60, 100, 140, 180, 220}
G_WIDTH = 40
G_HEIGHT = 6
LIT = "█"

instructions = []
for i in sys.stdin:
    i = i.split()
    if len(i) == 1:
        instructions.append(i[0])
    else:
        instructions.append((i[0], int(i[1])))

cycle = 0
counter = 1
sig_total = 0
grid = [[" " for _ in range(G_WIDTH)] for _ in range(G_HEIGHT)]
for i in instructions:
    if i == "noop":
        # yes i know this part is used 3 times, sue me
        if abs(cycle % G_WIDTH - counter) <= 1:
            grid[cycle // G_WIDTH][cycle % G_WIDTH] = LIT
        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter

    elif i[0] == "addx":
        if abs(cycle % G_WIDTH - counter) <= 1:
            grid[cycle // G_WIDTH][cycle % G_WIDTH] = LIT
        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter

        if abs(cycle % G_WIDTH - counter) <= 1:
            grid[cycle // G_WIDTH][cycle % G_WIDTH] = LIT
        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter

        counter += i[1]

print(f"OMG DIDN'T EVEN GET TOP 1000 FOR THIS ONE: {sig_total}")
for r in grid:
    print(''.join(r))
