P2_DIST_REQ = 1000


def room_dists(re: str) -> dict[tuple[int, int], int]:
    # sauce: https://todd.ginsberg.com/post/advent-of-code/2018/day20/
    dir_dict = {
        "N": lambda r, c: (r - 1, c),
        "S": lambda r, c: (r + 1, c),
        "E": lambda r, c: (r, c + 1),
        "W": lambda r, c: (r, c - 1),
    }
    start = (0, 0)
    dist = {start: 0}
    stack = [start]
    at = start
    for i in re.upper():
        if i in dir_dict:
            prev = at
            at = dir_dict[i](*at)
            dist[at] = min(dist.get(at, float("inf")), dist[prev] + 1)
        elif i == "(":
            stack.append(at)
        elif i == ")":
            at = stack.pop()
        elif i == "|":
            at = stack[-1]
    return dist


with open("input/day20.txt") as read:
    regex = read.readline().strip()[1:-1]

dists = room_dists(regex).values()
print(f"farthest room distance: {max(dists)}")
p2_ans = sum(d >= P2_DIST_REQ for d in dists)
print(f"# of rooms at least {P2_DIST_REQ} doors away: {p2_ans}")
