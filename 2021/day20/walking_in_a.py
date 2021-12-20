import numpy as np

LIT = "#"  # hella lit
P1_AMT = 2
P2_AMT = 50

with open("winter_wonderland.txt") as read:
    algo = read.readline().strip()
    assert len(algo) == 1 << 9, "should be exactly 512 chars"
    read.readline()
    raw_img = [l.strip() for l in read.readlines()]

algo = np.array([i == LIT for i in algo], dtype=np.bool)
img = np.array([[i == LIT for i in r] for r in raw_img], dtype=np.bool)

mul_by = np.array([1 << i for i in range(9 - 1, -1, -1)]).reshape((3, 3))
# what the endless boundary looks like
border = False
for i in range(max(P1_AMT, P2_AMT)):
    # pad by 2 units on each side
    expanded_img = np.zeros((len(img) + 4, len(img[0]) + 4), dtype=np.bool)
    expanded_img.fill(border)
    expanded_img[2:len(expanded_img) - 2, 2:len(expanded_img[0]) - 2] = img

    new_img = np.zeros((len(img) + 4, len(img[0]) + 4), dtype=np.bool)
    next_border = algo[0] if not border else algo[-1]
    new_img.fill(next_border)

    # go through all the squares that aren't part of the endless boundary
    for r in range(1, len(expanded_img) - 1):
        for c in range(1, len(expanded_img[r]) - 1):
            surrounding = expanded_img[r - 1:r + 2, c - 1:c + 2]
            num = sum(surrounding * mul_by).sum()
            new_img[r, c] = algo[num]

    img = new_img
    border = next_border
    if i == P1_AMT - 1 or i == P2_AMT - 1:
        print(float("inf") if border else img.sum())
