import re

ADJ = 2  # how many pots do we have to check on the side?
PLANT = '#'
EMPTY = '.'
P1_TIME = 20
P2_TIME = 50000000000


rules = {}
with open('input/day12.txt') as read:
    both = PLANT + EMPTY
    pots = next(iter(re.findall(
        f'initial state: ([{both}]*)', read.readline()
    )))

    read.readline()  # idk why there's a blank line
    for r in read.readlines():
        config, res = next(iter(re.findall(
            f'([{both}]{{{2 * ADJ + 1}}}) => ([{both}])', r
        )))
        rules[config] = res
assert rules[EMPTY * (2 * ADJ + 1)] == EMPTY

zero_pos = 0
prev = None
time = 0
while True:
    curr = ADJ * EMPTY + pots + ADJ * EMPTY
    updated = []
    for i in range(len(curr)):
        if i < ADJ:
            config = EMPTY * (ADJ - i) + curr[:i + ADJ + 1]
        elif len(curr) - ADJ <= i:
            config = curr[i - ADJ:] + EMPTY * (i - (len(curr) - ADJ) + 1)
        else:
            config = curr[i - ADJ:i + ADJ + 1]
        updated.append(rules.get(config, EMPTY))

    zero_pos += ADJ
    time += 1
    pots = ''.join(updated)
    if prev is not None:
        prev_relevant = prev[prev.find(PLANT):prev.rfind(PLANT) + 1]
        curr_relevant = pots[pots.find(PLANT):pots.rfind(PLANT) + 1]
        if prev_relevant == curr_relevant:
            prev_pos = prev.find(PLANT) - zero_pos
            curr_pos = curr.find(PLANT) - zero_pos
            diff = curr_pos - prev_pos - ADJ

            total = 0
            for i in range(len(pots)):
                if pots[i] == PLANT:
                    total += i - zero_pos
            p2_total = total + diff * pots.count(PLANT) * (P2_TIME - time)
            print(f"pot total after {P2_TIME} gens: {p2_total}")
            break

    if time == P1_TIME or time == P2_TIME:
        total = 0
        for i in range(len(pots)):
            if pots[i] == PLANT:
                total += i - zero_pos
        print(f"pot total after {time} gens: {total}")

    prev = curr
