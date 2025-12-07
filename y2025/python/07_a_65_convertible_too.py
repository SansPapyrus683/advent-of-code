import sys
from collections import defaultdict

grid = [line.strip() for line in sys.stdin]

start = grid[0].index("S")
beams = {start: 1}
split_amt = 0
for row in grid[1:]:
    next_beams = defaultdict(int)
    for pos, ways in beams.items():
        if row[pos] == "^":
            next_beams[pos - 1] += beams[pos]
            next_beams[pos + 1] += beams[pos]
            split_amt += 1
        else:
            next_beams[pos] += beams[pos]

    beams = next_beams

print(f"well i could've done better today: {split_amt}")
print(f"but no big blunders, so p good! {sum(beams.values())}")
