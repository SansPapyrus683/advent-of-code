import sys

words = [i.strip() for i in input().split(",")]
input()  # stupid blank lines

poss_num = 0
way_num = 0
for big_word in sys.stdin:
    big_word = big_word.strip()
    ways = [0 for _ in range(len(big_word) + 1)]
    ways[0] = 1
    for i in range(1, len(big_word) + 1):
        for w in words:
            if big_word[:i].endswith(w):
                ways[i] += ways[i - len(w)]

    poss_num += bool(ways[-1])
    way_num += ways[-1]

print(f"not t100 today, but it is what it is: {poss_num}")
print(f"jack wang stop looking over my shoulder you nincompoop: {way_num}")
