from collections import Counter

with open("day6.txt") as read:
    msgs = [l.strip() for l in read.readlines()]
    assert len(set(len(m) for m in msgs)) == 1

msg_len = len(msgs[0])
p1_og = []
p2_og = []
for i in range(msg_len):
    counter = Counter(m[i] for m in msgs)
    most_common = counter.most_common()
    p1_og.append(most_common[0][0])
    p2_og.append(most_common[-1][0])

print(f"p1 message: {''.join(p1_og)}")
print(f"p2 message: {''.join(p2_og)}")
