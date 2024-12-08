import sys
from bisect import bisect


def reduce(snailfish):
    def parse_snailfish(snailfish):
        new_exp = ""
        for c in snailfish:
            if c == "[":
                new_exp += "["
            elif c == "]":
                new_exp += "],"
            elif type(c) == int:
                new_exp += str(c) + ", "
            else:
                raise ValueError("invalid snailfish stuff")
        return eval(new_exp[:-1])

    def break_snailfish(snailfish):
        new = []
        for c in str(snailfish):
            if c.isdigit():
                new.append(int(c))
            elif c in "[]":
                new.append(c)
        return new

    snailfish = break_snailfish(snailfish)
    valid = False
    while not valid:
        valid = True
        level = 0
        reg_ind = [i for i in range(len(snailfish)) if type(snailfish[i]) == int]
        for v, c in enumerate(snailfish):
            if c == "[":
                level += 1
            elif c == "]":
                level -= 1
            else:
                # the level 4 ones are always guaranteed to be a reg. number pair
                if level == 4 + 1:
                    left_num = bisect(reg_ind, v - 1) - 1
                    right_num = bisect(reg_ind, v + 2)
                    if 0 <= left_num:
                        snailfish[reg_ind[left_num]] += c
                    if right_num < len(reg_ind):
                        snailfish[reg_ind[right_num]] += snailfish[v + 1]

                    snailfish[v - 1:v + 3] = [0]
                    valid = False
                    break

        if valid:
            for v, c in enumerate(snailfish):
                if type(c) == int and c >= 10:
                    snailfish[v:v + 1] = ["[", c // 2, c // 2 + c % 2, "]"]
                    valid = False
                    break
    return parse_snailfish(snailfish)


def add(first, second):
    return reduce([first] + [second])


def magnitude(snailfish):
    first = snailfish[0] if type(snailfish[0]) == int else magnitude(snailfish[0])
    second = snailfish[1] if type(snailfish[1]) == int else magnitude(snailfish[1])
    return 3 * first + 2 * second


fish = [eval(l) for l in sys.stdin]

curr = reduce(fish[0])
for f in fish[1:]:
    curr = add(curr, f)

print(f"bruh what even was this problem: {magnitude(curr)}")

max_mag = 0
for i in range(len(fish)):
    for j in range(len(fish)):
        if i != j:
            max_mag = max(max_mag, magnitude(add(fish[i], fish[j])))

print(f"60% reading comp, 39% implementation, 1% actual thinking: {max_mag}")
