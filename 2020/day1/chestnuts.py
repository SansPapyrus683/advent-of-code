import sys

with open('fire.txt') as read:
    expenses = [int(i) for i in read.readlines()]

found = False
for v, e1 in enumerate(expenses):
    for e2 in expenses[:v] + expenses[v + 1:]:  # just a precaution, we don't want to use the same # twice
        if e1 + e2 == 2020:
            print(f"i'm getting super heavy mario sunshine vibes from this: {e1 * e2}")
            found = True
            break
    if found:
        break

for v1, e1 in enumerate(expenses):
    for v2, e2 in enumerate(expenses):
        for v3, e3 in enumerate(expenses):
            if e1 + e2 + e3 == 2020 and len({v1, v2, v3}) == 3:
                print(f"there's a more efficient algo but idc lol it works anyways: {e1 * e2 * e3}")
                sys.exit()
