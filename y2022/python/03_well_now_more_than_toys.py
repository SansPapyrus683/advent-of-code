import sys


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def priority(item: str) -> int:
    assert len(item) == 1 and item.isalpha()
    if item.isupper():
        return ord(item) - ord('A') + 26 + 1
    else:
        return ord(item) - ord('a') + 1


sacks = [l.strip() for l in sys.stdin]

p1_priority = 0
for s in sacks:
    half1, half2 = s[:len(s) // 2], s[len(s) // 2:]
    in_both = set(half1).intersection(set(half2))
    assert len(in_both) == 1
    p1_priority += priority(next(iter(in_both)))

p2_priority = 0
for s in chunks(sacks, 3):
    in_all = set(s[0])
    for os in s[1:]:
        in_all = in_all.intersection(set(os))

    assert len(in_all) == 1
    p2_priority += priority(next(iter(in_all)))

print(f"damit i forgot how to check if a string was uppercase: {p1_priority}")
print(f"didn't get double digits lb this time :( {p2_priority}")
