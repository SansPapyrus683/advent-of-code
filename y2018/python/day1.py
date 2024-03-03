freq_changes = [int(i) for i in open("input/day1.txt").readlines()]

print(f"final freq: {sum(freq_changes)}")

dupe_found = False
freq = 0
seen = {freq}
while True:
    for fc in freq_changes:
        freq += fc
        if freq in seen:
            print(f"first dupe freq: {freq}")
            dupe_found = True
            break
        seen.add(freq)

    if dupe_found:
        break
