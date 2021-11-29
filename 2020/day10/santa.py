MAX_DIFF = 3

with open('on_his_way.txt') as read:
    adapters = sorted(set(int(line) for line in read.readlines()))

adapters.append(adapters[-1] + 3)  # add the built-in joltage adapter and the wall adapter
adapters.insert(0, 0)
one_diff_num = 0
three_diff_num = 0
prev = 0
for a in adapters:
    if a - prev == 1:
        one_diff_num += 1
    elif a - prev == 3:
        three_diff_num += 1
    prev = a
print(f"jesus christ why does the protag have so many adapters: {one_diff_num * three_diff_num}")

# this[i] = amt of ways given that we use adapters[i]
combs_so_far = [0 for _ in range(len(adapters))]
combs_so_far[0] = 1
for i in range(1, len(adapters)):
    for a in range(max(0, i - MAX_DIFF), i):
        if adapters[a] + MAX_DIFF >= adapters[i]:
            combs_so_far[i] += combs_so_far[a]

# we have to end at the built-in adapter, so just take the last element
print(f"were they preparing for like a worldwide adapter shortage or something: {combs_so_far[-1]}")
