from collections import deque

SCORE_INTERVAL = 23
CC_REMOVED = 7


def scores(player_num: int, last_marble_score: int) -> list[int]:
    ret = [0] * player_num
    circle = deque([0])
    for m in range(1, last_marble_score):
        if m % SCORE_INTERVAL == 0:
            player = (m - 1) % player_num
            ret[player] += m
            for _ in range(CC_REMOVED):
                circle.appendleft(circle.pop())
            ret[player] += circle.popleft()
        else:
            for _ in range(2):
                circle.append(circle.popleft())
            circle.appendleft(m)
    return ret


players = 413
p1_last_pts = 71082

print(f"winning score (p1): {max(scores(players, p1_last_pts))}")
print(f"winning score (p2): {max(scores(players, p1_last_pts * 10 ** 2))}")
