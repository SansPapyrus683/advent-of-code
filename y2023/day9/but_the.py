with open("children_know.txt") as read:
    histories = []
    for i in read.readlines():
        histories.append([int(i) for i in i.split()])

p1_tot = 0
p2_tot = 0
for init_h in histories:
    diff_hist = [init_h]
    h_at = init_h
    while not all(i == 0 for i in h_at):
        h_at = [h_at[i + 1] - h_at[i] for i in range(len(h_at) - 1)]
        diff_hist.append(h_at)

    for v, hh in enumerate(reversed(diff_hist)):
        p1_tot += hh[-1]
        p2_tot += (1 if (len(diff_hist) - v - 1) % 2 == 0 else -1) * hh[0]

print(f"man today's was kinda underwhelming: {p1_tot}")
print(f"just add some numbers and you're done lol: {p2_tot}")
