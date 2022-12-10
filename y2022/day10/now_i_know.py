RELEVANT_CYCLES = {20, 60, 100, 140, 180, 220}
G_WIDTH = 40
G_HEIGHT = 6
LIT = "█"

instructions = []
with open("what_my_heart_wants.txt") as read:
    for i in read.readlines():
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
        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter
        if abs((cycle - 1) % G_WIDTH - counter) <= 1:
            pos = cycle - 1
            grid[pos // G_WIDTH][pos % G_WIDTH] = LIT

    elif i[0] == "addx":
        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter
        if abs((cycle - 1) % G_WIDTH - counter) <= 1:
            pos = cycle - 1
            grid[pos // G_WIDTH][pos % G_WIDTH] = LIT

        cycle += 1
        if cycle in RELEVANT_CYCLES:
            sig_total += cycle * counter
        if abs((cycle - 1) % G_WIDTH - counter) <= 1:
            pos = cycle - 1
            grid[pos // G_WIDTH][pos % G_WIDTH] = LIT

        counter += i[1]

print(f"OMG DIDN'T EVEN GET TOP 1000 FOR THIS ONE: {sig_total}")
for r in grid:
    print(''.join(r))
