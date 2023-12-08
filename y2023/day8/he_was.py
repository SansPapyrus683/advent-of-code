from collections.abc import Callable
import re
from math import lcm


def num_steps(
        adj: dict[str, tuple[str, str]], seq: str,
        start: str, is_end: Callable[[str], bool]
) -> int:
    ret = 0
    at = start
    ind = 0
    while not is_end(at):
        use = 0 if seq[ind] == "L" else 1
        at = adj[at][use]
        ind = (ind + 1) % len(seq)
        ret += 1
    return ret


with open("made_of_snow.txt") as read:
    seq = read.readline().strip()
    read.readline()  # why is there an empty newline what

    adj = {}
    node_fmt = r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)"
    for node in read.readlines():
        if (res := re.match(node_fmt, node)) is not None:
            u, v1, v2 = res.group(1, 2, 3)
            adj[u] = v1, v2

p1_dist = -1
times = {}
for n in adj:
    if n.endswith("A"):
        times[n] = num_steps(adj, seq, n, lambda n: n.endswith("Z"))

    if n == "AAA":
        p1_dist = num_steps(adj, seq, n, lambda n: n == "ZZZ")

assert p1_dist != -1
p2_dist = lcm(*times.values())

print(f"i just realized: {p1_dist}")
print(f"why the hell does using the lcm work? {p2_dist}")
