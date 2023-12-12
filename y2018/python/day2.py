box_ids = [b.strip() for b in open('input/day2.txt').readlines()]

exactly_two = 0
exactly_three = 0
for b in box_ids:
    occ = {}
    for c in b:
        if c not in occ:
            occ[c] = 0
        occ[c] += 1
    exactly_two += 2 in occ.values()
    exactly_three += 3 in occ.values()

print(f"checksum: {exactly_two * exactly_three}")

found_correct = False
for i in range(len(box_ids)):
    for j in range(i + 1, len(box_ids)):
        diff_num = sum(c1 != c2 for c1, c2 in zip(box_ids[i], box_ids[j]))
        if diff_num == 1:
            common = ''
            for c1, c2 in zip(box_ids[i], box_ids[j]):
                if c1 == c2:
                    common += c1
            print(f"common box id string: {common}")

            found_correct = True

    if found_correct:
        break
