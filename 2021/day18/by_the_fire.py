from bisect import bisect


def reduce(shellfish):
    def parse_shellfish(shellfish):
        new_exp = ""
        for c in shellfish:
            if c == "[":
                new_exp += "["
            elif c == "]":
                new_exp += "],"
            elif type(c) == int:
                new_exp += str(c) + ", "
            else:
                raise ValueError("invalid shellfish stuff")
        return eval(new_exp[:-1])

    def break_shellfish(shellfish):
        new = []
        for c in str(shellfish):
            if c.isdigit():
                new.append(int(c))
            elif c in "[]":
                new.append(c)
        return new

    shellfish = break_shellfish(shellfish)
    valid = False
    while not valid:
        valid = True
        level = 0
        reg_ind = [i for i in range(len(shellfish)) if type(shellfish[i]) == int]
        for v, c in enumerate(shellfish):
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
                        shellfish[reg_ind[left_num]] += c
                    if right_num < len(reg_ind):
                        shellfish[reg_ind[right_num]] += shellfish[v + 1]

                    shellfish[v - 1:v + 3] = [0]
                    valid = False
                    break

        if valid:
            for v, c in enumerate(shellfish):
                if type(c) == int and c >= 10:
                    shellfish[v:v + 1] = ["[", c // 2, c // 2 + c % 2, "]"]
                    valid = False
                    break
    return parse_shellfish(shellfish)


def add(first, second):
    return reduce([first] + [second])


def magnitude(shellfish):
    first = shellfish[0] if type(shellfish[0]) == int else magnitude(shellfish[0])
    second = shellfish[1] if type(shellfish[1]) == int else magnitude(shellfish[1])
    return 3 * first + 2 * second


with open("to_face_unafraid.txt") as read:
    fish = [eval(l) for l in read.readlines()]


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
