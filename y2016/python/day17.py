from collections import deque
from hashlib import md5  # dear god this is the third time

PW = "njfxhljp"

DIMS = 4, 4

START = 0, 0
END = 3, 3

DIR = list("UDLR")
POS_CHANGE = [[-1, 0], [1, 0], [0, -1], [0, 1]]
assert len(DIR) == len(POS_CHANGE)

vault_paths = []
frontier = deque([(START[0], START[1], "")])
min_dist = {(frontier[0]): 0}
while frontier:
    r, c, path = frontier.popleft()
    if (r, c) == END:
        vault_paths.append(path)
        continue

    curr_dist = min_dist[(r, c, path)]

    hsh = md5((PW + path).encode()).hexdigest()
    for i in range(len(DIR)):
        if hsh[i] <= "a":
            continue

        nr = r + POS_CHANGE[i][0]
        nc = c + POS_CHANGE[i][1]
        n_path = path + DIR[i]
        state = nr, nc, n_path
        if (0 <= nr < DIMS[0] and 0 <= nc < DIMS[1]
                and curr_dist + 1 < min_dist.get(state, float("inf"))):
            min_dist[state] = curr_dist + 1
            frontier.append(state)

print(f"shortest path: {vault_paths[0]}")
print(f"longest path length: {max(len(p) for p in vault_paths)}")
