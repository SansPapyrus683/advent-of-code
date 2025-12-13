import sys
from collections import defaultdict

P1_ENDS = "you", "out"
P2_ENDS = "svr", "out"
P2_NEED = ["fft", "dac"]

nodes = set()
goto = defaultdict(list)
in_deg = defaultdict(int)
for n in sys.stdin:
    from_, to = n.split(": ")
    to = to.split()
    goto[from_] = to

    nodes.add(from_)
    for i in to:
        nodes.add(i)
        in_deg[i] += 1

frontier = [n for n in nodes if in_deg[n] == 0]
topo_order = []
while frontier:
    curr = frontier.pop()
    topo_order.append(curr)
    for n in goto[curr]:
        in_deg[n] -= 1
        if in_deg[n] == 0:
            frontier.append(n)


def num_paths(start: str, end: str) -> int:
    # i can't think of a better way to design this
    ways = defaultdict(int)
    ways[start] = 1
    for n in topo_order:
        for i in goto[n]:
            ways[i] += ways[n]
    return ways[end]


print(f"choked pretty hard today: {num_paths(*P1_ENDS)}")

need_order = sorted(P2_NEED, key=lambda n: topo_order.index(n))
p2_path = [P2_ENDS[0], *need_order, P2_ENDS[1]]

p2_ways = 1
for i in range(len(p2_path) - 1):
    p2_ways *= num_paths(p2_path[i], p2_path[i + 1])
print(f"idk why, i thought i was doing fine: {p2_ways}")
