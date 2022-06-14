from itertools import permutations

# mappings from the letters in the display to the nums
TARGETS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

with open("while_we_go.txt") as read:
    signals = []
    for i in read.readlines():
        patterns, val = i.strip().split("|")
        signals.append([patterns.strip().split(), val.strip().split()])

unique_amt = 0
for patterns, val in signals:
    # i don't like magic numbers, but idk if there's a better way to do this
    unique_amt += sum(len(i) in [2, 4, 3, 7] for i in val)
print(f"this problem was crap imo: {unique_amt}")

total = 0
target = [i for i in range(10)]
for patterns, val in signals:
    # takes a bit of time, but it should still run in a reasonable amt of time
    for p in permutations("abcdefg"):
        mappings = {p[v]: i for v, i in enumerate("abcdefg")}
        got_nums = set()
        for w in patterns:
            w = "".join(sorted(mappings[c] for c in w))
            got_nums.add(TARGETS.get(w, -1))

        if sorted(got_nums) == [i for i in range(10)]:
            final = ""
            for i in val:
                final += str(TARGETS["".join(sorted(mappings[c] for c in i))])
            total += int(final)
            break
print(f"but hey maybe i'm just bad: {total}")
