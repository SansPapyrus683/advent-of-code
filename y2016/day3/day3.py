import numpy as np

with open("day3.txt") as read:
    triangles = []
    for t in read.readlines():
        triangles.append([int(i) for i in t.split()])
        assert len(triangles[-1]) == 3
triangles = np.array(triangles)

possible = 0
for t in triangles:
    longest = t.max()
    possible += longest < t.sum() - longest
print(f"# of possible triangles (reading by row): {possible}")

by_column = triangles.T.reshape((-1, 3))
possible = 0
for t in by_column:
    longest = t.max()
    possible += longest < t.sum() - longest
print(f"# of possible triangles (reading by column): {possible}")
