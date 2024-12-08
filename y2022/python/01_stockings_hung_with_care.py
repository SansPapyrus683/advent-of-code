import sys

elves = []
elf = []
for i in sys.stdin:
    if i == "\n":
        elves.append(elf)
        elf = []
    else:
        elf.append(int(i))
if elf:
    elves.append(elf)

calories = sorted(sum(e) for e in elves)
print(f"BRO I FORGOT AOC STARTED ON 11/30 OMG: {calories[-1]}")
print(f"just barely eeked out top 1k: {sum(calories[-3:])}")
