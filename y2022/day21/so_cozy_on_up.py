ROOT_OP = "█"

monkeys = {}
with open("by_the_fireplace.txt") as read:
    for m in read.readlines():
        monkey, yell = [i.strip() for i in m.split(":")]
        monkeys[monkey] = yell.split()

alr_done = {}
for m, y in monkeys.items():
    if len(y) == 1 and y[0].isnumeric():
        alr_done[m] = int(y[0])

expr = monkeys["root"]
expr[expr.index("+")] = ROOT_OP
while True:
    bad = False
    new = []
    for t in expr:
        if t == "humn" or not t.isalpha():
            new.append(t)
            continue

        new.append("(")
        new.extend(monkeys[t])
        new.append(")")
        bad = True
    expr = new
    if not bad:
        break

str_expr = "".join(expr)
humn = alr_done["humn"]
root = eval(str_expr.replace(ROOT_OP, "+"))
print(f"number the root monkey yells: {root}")

cutoff = str_expr.index(ROOT_OP)
left = str_expr[:cutoff]
right = eval(str_expr[cutoff + 1:])

lo = 0
hi = 10 ** 30  # this should definitely be large enough
while lo <= hi:
    humn = (lo + hi) // 2
    left_res = eval(left)
    if left_res < right:
        hi = humn - 1
    elif left_res > right:
        lo = humn + 1
    else:
        print(f"number you should yell: {humn}")
        break
else:
    print("well, sorry mate, can't find the answer for p2")
