def simulate(instruction_list: [[str, int]]) -> (int, bool):
    at = 0  # the instruction we're going to execute
    acc = 0
    visited = set()
    while at < len(lines) and at not in visited:
        instruct, arg = instruction_list[at]
        visited.add(at)
        if instruct == 'nop':
            at += 1  # do nothing lol
        elif instruct == 'acc':
            acc += arg  # add the argument and go to next
            at += 1
        elif instruct == 'jmp':
            at += arg
    return acc, at not in visited  # the resulting value of acc and whether we get stuck in an infinite loop or not


with open('children.txt') as read:
    lines = []
    for line in read.readlines():
        line = line.split()  # string parsing was pretty ez for this day
        lines.append([line[0], int(line[1])])

print(f"i thought goto statements were like a bad practice lol: {simulate(lines)[0]}")

for v, i in enumerate(lines):
    if lines[v][0] not in ['nop', 'jmp']:  # don't touch any acc instructions
        continue
    initial = i.copy()  # preserve a copy to reset
    lines[v][0] = 'nop' if lines[v][0] == 'jmp' else 'nop'
    result = simulate(lines)
    if result[1]:  # if it terminated correctly, print result and break
        print(f"please don't make this a recurring thing eric: {result[0]}")
        break
    lines[v] = initial  # reset the simulation
