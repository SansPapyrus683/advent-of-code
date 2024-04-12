SERIAL_NUM = 9005
WIDTH = 300
P1_SUB_WIDTH = 3


def power_level(x: int, y: int) -> int:
    rack_id = x + 10
    lvl = rack_id * y
    lvl += SERIAL_NUM
    lvl *= rack_id
    lvl = (lvl // 100) % 10
    lvl -= 5
    return lvl


pref_grid = [
    [0 for _ in range(WIDTH + 1)]
    for _ in range(WIDTH + 1)
]
for x in range(1, WIDTH + 1):
    for y in range(1, WIDTH + 1):
        pref_grid[x][y] = (
            power_level(y, x)
            + pref_grid[x][y - 1]
            + pref_grid[x - 1][y]
            - pref_grid[x - 1][y - 1]
        )

p1_most_power = (None, -float('inf'))
p2_most_power = (None, -float('inf'))
for sx in range(1, WIDTH + 1):
    for sy in range(1, WIDTH + 1):
        for sub_width in range(1, WIDTH + 1):
            if sx > WIDTH - sub_width or sy > WIDTH - sub_width:
                continue

            power = (
                    pref_grid[sy + sub_width - 1][sx + sub_width - 1]
                    - pref_grid[sy - 1][sx + sub_width - 1]
                    - pref_grid[sy + sub_width - 1][sx - 1]
                    + pref_grid[sy - 1][sx - 1]
            )

            if power > p2_most_power[1]:
                p2_most_power = (sx, sy, sub_width), power
            if sub_width == P1_SUB_WIDTH and power > p1_most_power[1]:
                p1_most_power = (sx, sy), power

print(f"identifier for p1: {p1_most_power[0]}")
print(f"identifier for p2: {p2_most_power[0]}")
