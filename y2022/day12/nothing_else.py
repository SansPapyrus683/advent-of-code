from collections import deque

START = "S"
END = "E"


def neighbors4(r: int, c: int, r_max: int, c_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
    ] if 0 <= p[0] < r_max and 0 <= p[1] < c_max]


grid = []
with open("im_gonna_need.txt") as read:
    for r in read.readlines():
        grid.append([ord(c) for c in r.strip()])

# just some shorthands
r_num = len(grid)
c_num = len(grid[0])

end = None
for r in range(r_num):
    for c in range(c_num):
        if grid[r][c] == ord(END):
            end = (r, c)
            break
    if end is not None:  # python please give me loop labels i'm begging you
        break
assert end is not None

grid[end[0]][end[1]] = ord("z")

total_shortest = float("inf")
for sr in range(r_num):
    for sc in range(c_num):
        first_start = False
        if grid[sr][sc] == ord(START):
            grid[sr][sc] = ord("a")
            first_start = True

        if grid[sr][sc] != ord("a"):
            continue

        frontier = deque([(sr, sc)])
        min_dist = [[float("inf") for _ in range(c_num)] for _ in range(r_num)]
        min_dist[sr][sc] = 0
        while frontier:
            cr, cc = frontier.popleft()
            new_dist = min_dist[cr][cc] + 1
            for nr, nc in neighbors4(cr, cc, r_num, c_num):
                if grid[cr][cc] + 1 >= grid[nr][nc] and new_dist < min_dist[nr][nc]:
                    min_dist[nr][nc] = new_dist
                    frontier.append((nr, nc))

        if first_start:
            print(f"min dist given the p1 start: {min_dist[end[0]][end[1]]}")
        total_shortest = min(total_shortest, min_dist[end[0]][end[1]])

print(f"i mean i didn't get top 50, but i'll take top 100: {total_shortest}")
