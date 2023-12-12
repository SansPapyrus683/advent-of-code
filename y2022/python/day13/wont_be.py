from functools import cmp_to_key

KEY1 = [[2]]
KEY2 = [[6]]


def packet_cmp(a: list[list | int] | int, b: list[list | int] | int):
    if type(a) == list and type(b) == int:
        return packet_cmp(a, [b])
    elif type(b) == list and type(a) == int:
        return packet_cmp([a], b)
    elif type(a) == type(b) == int:
        return a - b

    if len(a) == len(b) == 0:
        return 0
    elif len(a) == 0:
        return -1
    elif len(b) == 0:
        return 1

    x, y = a[0], b[0]
    res = packet_cmp(x, y)
    if res == 0:
        return packet_cmp(a[1:], b[1:])
    return res


pairs = []
with open("wrapped_under_a_tree.txt") as read:
    raw_pairs = read.read().split("\n\n")
    for p in raw_pairs:
        p1, p2 = [eval(i) for i in p.strip().split("\n")]
        pairs.append((p1, p2))

bad_order_sum = 0
for v, (p1, p2) in enumerate(pairs):
    if packet_cmp(p1, p2) <= 0:
        bad_order_sum += v + 1
print(f"god this was awful: {bad_order_sum}")

all_packets = [KEY1, KEY2]
for p in pairs:
    all_packets.extend(p)
all_packets.sort(key=cmp_to_key(packet_cmp))

decoder_key = (all_packets.index(KEY1) + 1) * (all_packets.index(KEY2) + 1)
print(f"i ended up having to recode my entire function again: {decoder_key}")
