DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

trees = []
with open("please_be_careful.txt") as read:
    for i in read.readlines():
        trees.append([int(x) for x in i.strip()])

total_visible = 0
max_scenery = 0
for r in range(len(trees)):
    for c in range(len(trees[r])):
        left_vis = all(trees[r][c] > trees[r][x] for x in range(c))
        right_vis = all(trees[r][c] > trees[r][x] for x in range(c + 1, len(trees[c])))
        top_vis = all(trees[r][c] > trees[x][c] for x in range(r))
        bottom_vis = all(trees[r][c] > trees[x][c] for x in range(r + 1, len(trees)))

        total_visible += left_vis or right_vis or top_vis or bottom_vis

        score = 1
        for d in DIRECTIONS:
            at = [r + d[0], c + d[1]]
            dist = 0
            while (0 <= at[0] < len(trees)
                   and 0 <= at[1] < len(trees[at[0]])):
                dist += 1
                if trees[at[0]][at[1]] >= trees[r][c]:
                    break
                at[0] += d[0]
                at[1] += d[1]

            score *= dist
        max_scenery = max(max_scenery, score)

print(f"well, i got #2 for p1: {total_visible}")
print(f"but i didn't even get top 100 for p2 :( {max_scenery}")
