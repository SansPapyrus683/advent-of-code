TIMER_START = 6
NEW_TIMER = 8
P1_DAYS = 80
P2_DAYS = 256

lanterns = [int(i) for i in input().split(",")]

timer_amt = [0 for _ in range(max(TIMER_START, NEW_TIMER) + 1)]
for l in lanterns:
    timer_amt[l] += 1

p1_lantern_num = 0
p2_lantern_num = 0
for d in range(max(P1_DAYS, P2_DAYS)):
    new_amt = 0
    new_timers = [0 for _ in range(max(TIMER_START, NEW_TIMER) + 1)]
    for t, l in enumerate(timer_amt):
        if t == 0:
            new_amt += l
            new_timers[TIMER_START] = l
        else:
            new_timers[t - 1] += l
    new_timers[NEW_TIMER] += new_amt
    timer_amt = new_timers

    if d == P1_DAYS - 1:
        p1_lantern_num = sum(timer_amt)
    elif d == P2_DAYS - 1:
        p2_lantern_num = sum(timer_amt)

print(f"can't believe it i got #18 for this part: {p1_lantern_num}")
print(f"bruh i used a dict at first for this lol: {p2_lantern_num}")
