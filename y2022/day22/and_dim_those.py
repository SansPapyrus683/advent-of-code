def neighbors4raw(r: int, c: int) -> list[tuple[int, int]]:
    return [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]


def move(d: int) -> tuple[int, int]:
    if d == 0:
        return -1, 0
    elif d == 1:
        return 0, 1
    elif d == 2:
        return 1, 0
    elif d == 3:
        return 0, -1


with open("xmas_lights.txt") as read:
    x, y = read.read().split('\n\n')
    x = [' ' + r + ' ' * 1000 for r in x.split('\n')]
    y = y.strip()

x.insert(0, ' ' * 1000)
x.append(' ' * 1000)

start = None
for r in range(len(x[1])):
    if x[1][r] != ' ':
        start = (1, r)

asdf = []
curr = ''
for c in y:
    if c.isdigit():
        curr += c
    else:
        asdf.append(int(curr))
        asdf.append(c)
        curr = ''
if curr:
    asdf.append(int(curr))

for r in x:
    print(repr(r))

b_space_next = {}
for r in range(len(x)):
    for c in range(len(x[r])):
        if not x[r][c].isspace():
            for n in neighbors4raw(r, c):
                if x[n[0]][n[1]].isspace():
                    delta = (n[0] - r, n[1] - c)
                    rev = (-delta[0], -delta[1])
                    curr = (r, c)
                    while not x[curr[0]][curr[1]].isspace():
                        curr = (curr[0] + rev[0], curr[1] + rev[1])
                    curr = (curr[0] + delta[0], curr[1] + delta[1])
                    b_space_next[((r, c), n)] = curr

print(b_space_next)

direction = 1
curr = start
for thing in asdf:
    if type(thing) == int:
        delta = move(direction)
        print(direction, thing)
        for _ in range(thing):
            n = (curr[0] + delta[0], curr[1] + delta[1])
            if x[n[0]][n[1]] == ' ':
                poss = b_space_next[(curr, n)]
                if x[poss[0]][poss[1]] == '#':
                    break
                curr = poss
            elif x[n[0]][n[1]] == '#':
                break
            else:
                curr = n
            # print(curr)
    else:
        if thing == 'L':
            direction -= 1
        else:
            direction += 1
        direction %= 4

print(curr[0] * 1000 + curr[1] * 4 + ((direction - 1) % 4))
