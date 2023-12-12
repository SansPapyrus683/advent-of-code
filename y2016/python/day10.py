import re

# gotten from skimming my puzzle input, change them as you wish
BOT_NUM = 250
OUTPUT_NUM = 25
CMP_DETECT = [17, 61]
OUTPUT_PROD = [0, 1, 2]

val_fmt = r"value (\d+) goes to bot (\d+)"
cmp_fmt = r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)"

cmp = []
val = []
with open("input/day10.txt") as read:
    for b in read.readlines():
        if re.match(val_fmt, b) is not None:
            b = list(re.findall(val_fmt, b)[0])
        elif re.match(cmp_fmt, b) is not None:
            b = list(re.findall(cmp_fmt, b)[0])
        b = list(filter(lambda i: i != "bot", b))

        if len(b) == 2:
            val.append([int(i) for i in b])
        else:
            for i in range(len(b)):
                b[i] = int(b[i]) if b[i].isdigit() else b[i]
            # boolean for if it's processed or not
            cmp.append(b + [False])

bots = [[] for _ in range(BOT_NUM)]
outputs = [[] for _ in range(OUTPUT_NUM)]

for r in val:
    bots[r[1]].append(r[0])

# go through all the bots until they've compared their stuff
while not all(r[-1] for r in cmp):
    for r in cmp:
        bot = bots[r[0]]
        if not r[-1] and len(bot) >= 2:
            if CMP_DETECT[0] in bot and CMP_DETECT[1] in bot:
                print(f"robot which compares instructions: {r[0]}")

            sec_ind = 2
            if r[1] == "output":
                outputs[r[2]].append(min(bot))
                sec_ind = 3
            else:
                bots[r[1]].append(min(bot))

            if r[sec_ind] == "output":
                outputs[r[sec_ind + 1]].append(max(bot))
            else:
                bots[r[sec_ind]].append(max(bot))
            r[-1] = 1

prod = 1
for o in OUTPUT_PROD:
    prod *= outputs[o][0]
print(f"output products: {prod}")
