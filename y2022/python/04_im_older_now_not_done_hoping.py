import sys

pairs = []
for i in sys.stdin:
    e1, e2 = i.split(",")
    e1_range = tuple(int(i) for i in e1.split('-'))
    e2_range = tuple(int(i) for i in e2.split('-'))
    assert len(e1_range) == len(e2_range) == 2
    pairs.append((e1_range, e2_range))

contain_num = 0
overlap_num = 0
for e1r, e2r in pairs:
    contain_num += (
            e1r[0] <= e2r[0] and e2r[1] <= e1r[1]
            or e2r[0] <= e1r[0] and e1r[1] <= e2r[1]
    )
    overlap_num += e1r[0] <= e2r[1] and e2r[0] <= e1r[1]

print(f"holy crap got ~top 50 in both parts! {contain_num}")
print(f"finna drop to ~top 1000 next day lol: {overlap_num}")
