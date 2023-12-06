import re


with open("day11.txt") as read:
    floors = []
    for f in read.readlines():
        floor_fmt = "The [a-zA-Z]+ floor contains (.*)"
        res = re.match(floor_fmt, f).group(1)\
            .strip()\
            .replace(".", "")\
            .replace("and", ",")\
            .split(",")

        microchip_fmt = r"a ([a-zA-Z]+)\-compatible microchip"
        generator_fmt = r"a ([a-zA-Z]+) generator"
        curr_floor = []
        for r in res:
            r = r.strip()
            if (res := re.match(microchip_fmt, r)) is not None:
                curr_floor.append((res.group(1), True))
            elif (res := re.match(generator_fmt, r)) is not None:
                curr_floor.append((res.group(1), False))
        floors.append(curr_floor)

print(floors)

