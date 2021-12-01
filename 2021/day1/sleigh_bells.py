with open("ringing.txt") as read:
    measurements = [int(i) for i in read.readlines()]

total = 0
for i in range(len(measurements) - 1):
    total += measurements[i] < measurements[i + 1]
print(f"i wish eric'd stop w/ the flavor text lol: {total}")

sum_amt = 3
all_sums = []
curr_sum = 0
for v, i in enumerate(measurements):
    curr_sum += i
    if v >= sum_amt:
        curr_sum -= measurements[v - sum_amt]
    all_sums.append(curr_sum)

all_sums = all_sums[sum_amt - 1:]
total = 0
for i in range(len(all_sums) - 1):
    total += all_sums[i] < all_sums[i + 1]
print(f"bruh i spent way too long figuring out what that A, B, C... meant: {total}")
