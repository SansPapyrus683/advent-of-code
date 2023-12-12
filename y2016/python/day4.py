import re
from collections import Counter
from string import ascii_lowercase

TARGET = "northpole object storage"

room_fmt = r"([a-z\-]*)-(\d+)\[([a-z]*)\]"
with open("input/day4.txt") as read:
    rooms = []
    for r in read.readlines():
        res = re.findall(room_fmt, r)
        if res is not None:
            name, sec_id, checksum = res[0]
            rooms.append((name.replace("-", " "), int(sec_id), checksum))

real_sum = 0
for name, sec_id, checksum in rooms:
    counter = Counter([c for c in name if c.isalpha()])
    most_common = counter.most_common()
    most_common.sort(key=lambda c: (c[1], -ord(c[0])), reverse=True)
    check = "".join(c[0] for c in most_common[:len(checksum)])
    if check == checksum:
        real_sum += sec_id

        real_name = []
        for c in name:
            if c.isalpha():
                ind = ord(c) - ord("a")
                real_name.append(
                    ascii_lowercase[(ind + sec_id) % len(ascii_lowercase)]
                )
            else:
                real_name.append(c)
        if "".join(real_name) == TARGET:
            print(f"north pole room id: {sec_id}")

print(f"sum of real room id#'s: {real_sum}")
