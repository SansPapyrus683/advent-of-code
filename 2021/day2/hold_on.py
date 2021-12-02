with open("are_you_listening.txt") as read:
    directions = [l.split() for l in read.readlines()]
    for d in directions:
        d[1] = int(d[1])

pos = 0
depth = 0
aim = 0
for d in directions:
    if d[0] == "forward":
        pos += d[1]
    elif d[0] == "backward":
        pos -= d[1]
    elif d[0] == "up":
        depth -= d[1]
    elif d[0] == "down":
        depth += d[1]
print(f"these problems constantly remind me how bad my input parsing skills are: {pos * depth}")

pos = 0
depth = 0
aim = 0
for d in directions:
    if d[0] == "forward":
        pos += d[1]
        depth += aim * d[1]
    elif d[0] == "backward":
        pos -= d[1]
    elif d[0] == "up":
        aim -= d[1]
    elif d[0] == "down":
        aim += d[1]
print(f"but hey i guess that's life: {pos * depth}")
