with open('nipping_on_nose.txt') as read:
    passwords = [p.rstrip() for p in read.readlines()]

p1Valid = 0
p2Valid = 0
for p in passwords:
    numbers, char = p[:p.find(':')].split()
    num1 = int(numbers[:numbers.find('-')])
    num2 = int(numbers[numbers.find('-') + 1:])
    pw = p[p.find(':') + 1:].strip()
    if num1 <= pw.count(char) <= num2:
        p1Valid += 1
    if (pw[num1 - 1] == char) ^ (pw[num2 - 1] == char):
        p2Valid += 1

print(f"i absolutely hate input provided like this: {p1Valid}")
print(f"but i guess i can't do anything about it: {p2Valid}")
