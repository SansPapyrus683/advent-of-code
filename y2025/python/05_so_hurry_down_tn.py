import sys
from collections import defaultdict

fresh = []
ids = []
reading_ranges = True
for line in sys.stdin:
    line = line.strip()
    if not line:
        reading_ranges = False
        continue
    
    if reading_ranges:
        fresh.append([int(i) for i in line.split("-")])
    else:
        ids.append(int(line))

valid = 0
for i in ids:
    valid += any(start <= i <= end for start, end in fresh)

incs = defaultdict(int)
for start, end in fresh:
    incs[start] += 1
    incs[end + 1] -= 1

last_pos = min(incs)
active = 0
total_valid = 0
for pos, i in sorted(incs.items()):
    if active > 0:
        total_valid += pos - last_pos
    active += i
    last_pos = pos

print(f"alright! pretty good day! {valid}")
print(f"didn't expect prefix sums tho lol: {total_valid}")
