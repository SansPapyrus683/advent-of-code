MIN = 0
MAX = (1 << 32) - 1

with open("day20.txt") as read:
    blocked = []
    for b in read.readlines():
        start, end = [int(i) for i in b.split("-")]
        blocked.append([start, end])

blocked.sort()
intervals = []
for b in blocked:
    if not intervals or intervals[-1][1] + 1 < b[0]:
        intervals.append(b)
        continue

    intervals[-1][1] = max(intervals[-1][1], b[1])

print(f"lowest unblocked ip: {intervals[0][1] + 1}")

prev = 0
total = 0
for i in intervals + [[MAX + 1, -1]]:
    total += max(i[0] - prev - 1, 0)
    prev = i[1]

print(f"allowed ip amt: {total}")
