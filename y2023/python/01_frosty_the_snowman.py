import sys

NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

codes = list(sys.stdin)

p1_sum = 0
p2_sum = 0
for code in codes:
    res1 = ""
    res2 = ""
    for c in code:
        if c.isdigit():
            res1 += c
            break
    for v, c in enumerate(code):
        if c.isdigit():
            res2 += c
            break

        found = False
        for i, n in enumerate(NUMS):
            if code[v:].startswith(n):
                res2 += str(i + 1)
                found = True
                break
        if found:
            break

    for c in reversed(code):
        if c.isdigit():
            res1 += c
            break
    for v, c in enumerate(reversed(code)):
        if c.isdigit():
            res2 += c
            break

        found = False
        for i, n in enumerate(NUMS):
            if code[-(v + 1):].startswith(n):
                res2 += str(i + 1)
                found = True
                break
        if found:
            break

    p1_sum += int(res1)
    p2_sum += int(res2)

print(f"i'm actually washed: {p1_sum}")
print(f"didn't get top 100 for p2 lmao: {p2_sum}")
