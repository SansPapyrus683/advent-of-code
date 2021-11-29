def tree_num(r_mov: int, c_mov: int, hills: [str]) -> int:
    start = (0, 0)  # row and column
    total = 0
    while start[0] + r_mov < len(hills):
        start = (start[0] + r_mov, (start[1] + c_mov) % len(hills[0]))
        if hills[start[0]][start[1]] == '#':
            total += 1
    return total


with open('yuletide.txt') as read:
    big_hill = [line.rstrip() for line in read.readlines()]

print(f"these sled coordinates really got me tripping: {tree_num(1, 3, big_hill)}")
tree_product = 1
for r, c in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
    tree_product *= tree_num(r, c, big_hill)
print(f"but this was a pretty nice (if ez) puzzle overall: {tree_product}")
