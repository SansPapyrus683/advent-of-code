import re

P1_Y = 2000000
P2_RANGE = 4000000


def dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


sensors = []
# i've been told this is better performance-wise
sensor_fmt = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)
with open("on_this_cold_dec_night.txt") as read:
    for s in read.readlines():
        if sensor_fmt.match(s):
            nums = [int(i) for i in sensor_fmt.findall(s)[0]]
            sensors.append(((nums[0], nums[1]), (nums[2], nums[3])))

valid_pt = None
solved_p1 = False
for y in range(0, P2_RANGE + 1):
    ranges = []
    for s, b in sensors:
        d = dist(s, b)  # distance between sensor & beacon
        dy = abs(s[1] - y)
        if dy <= d:
            dx = d - dy
            ranges.append((s[0] - dx, s[0] + dx))

    if y == P1_Y:
        invalid = set()
        for r in ranges:
            for i in range(r[0], r[1] + 1):
                invalid.add((i, y))
        for _, b in sensors:
            if b in invalid:
                invalid.remove(b)
        print(f"# of impossible positions @ y={P1_Y}: {len(invalid)}")
        solved_p1 = True

    ranges.sort()
    if ranges[0][0] > 0:
        break
    prev_end = ranges[0][1]
    for i in range(1, len(ranges)):  # think slicing takes linear time
        if ranges[i][0] > prev_end + 1:
            valid_pt = prev_end + 1, y
            break
        prev_end = max(prev_end, ranges[i][1])

    if valid_pt is not None and solved_p1:
        break

tuning_freq = valid_pt[0] * P2_RANGE + valid_pt[1]
print(f"tuning freq (wow got another top 100): {tuning_freq}")
