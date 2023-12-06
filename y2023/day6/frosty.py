from math import sqrt, ceil, floor


def valid_times(time: int, dist: int) -> int:
    x = (-time + sqrt(time ** 2 - 4 * dist)) / -2
    y = (-time - sqrt(time ** 2 - 4 * dist)) / -2
    return floor(y) - ceil(x) + 1


with open("the_snowman.txt") as read:
    time = [int(x) for x in read.readline().split(":")[1].split()]
    distance = [int(x) for x in read.readline().split(":")[1].split()]

p1_prod = 1
for t, d in zip(time, distance):
    p1_prod *= valid_times(t, d)

big_time = int("".join(map(str, time)))
big_dist = int("".join(map(str, distance)))
p2_amt = valid_times(big_time, big_dist)

print(f"BRO WHAT THE HELL: {p1_prod}")
print(f"I THOUGHT P2 INVOLVED MATH WHEN BRUTE FORCE WORKED: {p2_amt}")
