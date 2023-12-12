def inv(n: int, mod: int) -> int:
    """
    i think this computes the modular inverse of n mod m
    plagiarized from https://www.geeksforgeeks.org/chinese-remainder-theorem-set-2-implementation/ lol
    """
    m0 = mod
    x0 = 0
    x1 = 1

    if mod == 1:
        return 0
    while n > 1:  # so this is the extended euclidean algo?
        q = n // mod
        t = mod

        mod = n % mod
        n = t

        t = x0
        x0 = x1 - q * x0
        x1 = t
    # always return a positive value
    return x1 + m0 if x1 < 0 else x1


def find_min_x(divisors, remainders):
    """
    ok so given an array num an array num
    this function calcs the min x so that x % num[i] == rem[i] for all the i's
    """
    assert len(divisors) == len(remainders), "you know what you did wrong buddy"
    prod = 1
    for i in range(len(divisors)):
        prod *= divisors[i]
    result = 0
    for i in range(len(divisors)):
        pp = prod // divisors[i]  # haha can't believe they used pp as a variable name
        result += remainders[i] * inv(pp, divisors[i]) * pp
    return result % prod


with open('really_fly.txt') as read:
    earliest_dep_time = int(read.readline())
    buses = [int(b) if b.lower() != 'x' else -1 for b in read.readline().rstrip().split(',')]

time_at = earliest_dep_time
found = False
while True:
    for b in buses:
        if b == -1:
            continue
        if time_at % b == 0:
            print(f"bruh why are so many buses out of service: {(time_at - earliest_dep_time) * b}")
            found = True
            break
    if found:
        break
    time_at += 1

minBusTime = find_min_x([b for b in buses if b != -1], [(b - v) % b for v, b in enumerate(buses) if b != -1])
print(f"boy it is a very good thing that python has builtin bigint handling: {minBusTime}")
