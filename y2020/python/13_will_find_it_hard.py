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
        result += remainders[i] * pow(pp, -1, divisors[i]) * pp
    return result % prod


earliest_dep_time = int(input())
buses = [
    int(b) if b.lower() != "x" else -1 for b in input().split(",")
]

time_at = earliest_dep_time
found = False
while True:
    for b in buses:
        if b == -1:
            continue
        if time_at % b == 0:
            print(
                f"bruh why are so many buses out of service: {(time_at - earliest_dep_time) * b}"
            )
            found = True
            break
    if found:
        break
    time_at += 1

minBusTime = find_min_x(
    [b for b in buses if b != -1], [(b - v) % b for v, b in enumerate(buses) if b != -1]
)
print(
    f"boy it is a very good thing that python has builtin bigint handling: {minBusTime}"
)
