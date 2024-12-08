import sys

PREV_NUM = 25

numbers = [int(i) for i in sys.stdin]

invalid_num = -1
for i in range(PREV_NUM, len(numbers)):
    all_prev = numbers[i - PREV_NUM:i]
    valid = False
    for j in range(PREV_NUM):
        for k in range(PREV_NUM):
            if j != k and all_prev[j] + all_prev[k] == numbers[i]:
                valid = True
                break
        if valid:
            break
    if not valid:
        invalid_num = numbers[i]
        print(f"ok what are we even trying to do here: {invalid_num}")
        break

if invalid_num == -1:
    raise ValueError("hold on here i thought there was always going to be an invalid number")

prefix_sum = [0]  # this speeds it up SO much faster lol
for n in numbers:
    prefix_sum.append(prefix_sum[-1] + n)

# i think with a sliding windows you can get faster
# but with 1000 lines it doesn't really matter
for i in range(len(numbers)):
    for j in range(i + 2, len(numbers)):  # the subset has to contain at least 2 numbers
        sub_sum = prefix_sum[j + 1] - prefix_sum[i]
        if sub_sum == invalid_num:
            subset = numbers[i:j]
            print(f"i thought planes were supposed to have like user-friendly UIs: {min(subset) + max(subset)}")
