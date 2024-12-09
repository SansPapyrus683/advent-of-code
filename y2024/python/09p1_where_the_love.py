from bisect import bisect_left

blocks = [int(i) for i in input()]

at = 0
p1_files = []
sizes = []
for v, b in enumerate(blocks):
    if v % 2 == 0:
        id_ = v // 2
        sizes.append(b)
        for _ in range(b):
            p1_files.append((at, id_))
            at += 1
    else:
        at += b

p1_check = 0
for t in range(len(p1_files)):
    pos = bisect_left(p1_files, (t, 0))
    if pos < len(p1_files) and p1_files[pos][0] == t:
        p1_check += p1_files[pos][1] * t
    else:
        p1_check += p1_files.pop()[1] * t

print(f"HAHAHAHA #100 ON P1: {p1_check}")
