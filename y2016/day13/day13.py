from collections import deque

FAV_NUM = 1362
START = 1, 1
END = 39, 31  # reverse the coordinates for array stuff
SEARCH_DIST = 50


def is_open(r: int, c: int) -> bool:
    if r < 0 or c < 0:
        return False
    val = c * c + 3 * c + 2 * c * r + r + r * r + FAV_NUM
    return val.bit_count() % 2 == 0


def neighbors(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


assert is_open(1, 1)

frontier = deque([START])
dist = {START: 0}
while frontier:
    curr = frontier.popleft()
    if curr == END:
        print(f"dist to target point: {dist[curr]}")
        break
    curr_dist = dist[curr]
    for n in neighbors(*curr):
        if is_open(*n) and n not in dist:
            dist[n] = curr_dist + 1
            frontier.append(n)

frontier = deque([START])
dist = {START: 0}
while frontier:
    curr = frontier.popleft()
    curr_dist = dist[curr]
    for n in neighbors(*curr):
        if is_open(*n) and n not in dist and curr_dist < SEARCH_DIST:
            dist[n] = curr_dist + 1
            frontier.append(n)

print(f"# of squares reachable in {SEARCH_DIST} steps: {len(dist)}")
