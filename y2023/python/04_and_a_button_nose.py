import sys

cards = []
for c in sys.stdin:
    c_id, nums = c.split(":")
    c_id = int(c_id.split()[1])
    nums = nums.split("|")
    cards.append((
        c_id,
        {int(i) for i in nums[0].split()},
        [int(i) for i in nums[1].split()]
    ))

cards.sort()

total_pts = 0
card_amt = {c: 1 for c, _, _ in cards}
for c, win, have in cards:
    win_amt = sum(i in win for i in have)
    if win_amt > 1:
        total_pts += 2 ** (win_amt - 1)

    for i in range(win_amt):
        card_amt[c + i + 1] += card_amt[c]

print(f"honestly idk how i choked so hard: {total_pts}")
print(f"today wasn't even a hard day what: {sum(card_amt.values())}")
