# target area: x=282..314, y=-80..-45

x_valid = [282, 314]
y_valid = [-80, -45]

assert x_valid[0] <= x_valid[1] and all(i >= 0 for i in x_valid)
assert y_valid[0] <= y_valid[1] and all(i <= 0 for i in y_valid)

total = 0
start = [0, 0]
highest_valids = []
valid = 0
# negatives not needed because it'll just go back lol
for x_vel in range(x_valid[1]):
    # this should work i think
    for y_vel in range(min(y_valid), -min(y_valid)):
        pos = start.copy()
        curr_x_vel = x_vel
        curr_y_vel = y_vel
        max_y_pos = 0
        # if it's passed these boundaries, it's hopeless
        while pos[0] <= x_valid[1] and pos[1] >= y_valid[0]:
            pos[0] += curr_x_vel
            pos[1] += curr_y_vel
            max_y_pos = max(max_y_pos, pos[1])

            if curr_x_vel < 0:
                curr_x_vel += 1
            elif curr_x_vel > 0:
                curr_x_vel -= 1
            curr_y_vel -= 1

            if (x_valid[0] <= pos[0] <= x_valid[1]
                    and y_valid[0] <= pos[1] <= y_valid[1]):
                highest_valids.append(max_y_pos)
                valid += 1
                break

print(f"BRUH I'M THROWING THESE LATER DAYS SO HARD: {max(highest_valids)}")
print(f"and this is just a math problem tbh: {valid}")
