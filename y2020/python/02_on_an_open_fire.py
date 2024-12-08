import sys

passwords = [p.rstrip() for p in sys.stdin]

p1_valid = 0
p2_valid = 0
for p in passwords:
    numbers, char = p[: p.find(":")].split()
    num1 = int(numbers[: numbers.find("-")])
    num2 = int(numbers[numbers.find("-") + 1 :])
    pw = p[p.find(":") + 1 :].strip()
    if num1 <= pw.count(char) <= num2:
        p1_valid += 1
    if (pw[num1 - 1] == char) ^ (pw[num2 - 1] == char):
        p2_valid += 1

print(f"i absolutely hate input provided like this: {p1_valid}")
print(f"but i guess i can't do anything about it: {p2_valid}")
