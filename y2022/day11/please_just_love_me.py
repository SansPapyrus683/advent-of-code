from math import lcm
from dataclasses import dataclass
from copy import deepcopy
import re

P1_ROUNDS = 20
P2_ROUNDS = 10000


@dataclass
class Monkey:
    id: int
    items: list[int]
    op: str
    div_test: int
    if_true: int
    if_false: int


# fricking cursed regex
monkey_fmt = r"""Monkey (\d+):
  Starting items: ([\d, ]+)
  Operation: (new = .*)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""

monkeys = {}
with open("this_xmas.txt") as read:
    for m in read.read().split('\n\n'):
        if re.match(monkey_fmt, m):
            monkey, start, op, condition, if_true, if_false = re.findall(monkey_fmt, m)[0]
            monkey = int(monkey)
            monkeys[int(monkey)] = Monkey(
                int(monkey),
                [int(i) for i in start.split(',')], op,
                int(condition), int(if_true), int(if_false)
            )

p1_monkeys = deepcopy(monkeys)
inspect_amt = {m: 0 for m in p1_monkeys}
for _ in range(P1_ROUNDS):
    for m in p1_monkeys.values():
        for i in m.items:
            new = 0
            old = i
            exec(m.op)
            new //= 3
            inspect_amt[m.id] += 1
            if new % m.div_test == 0:
                p1_monkeys[m.if_true].items.append(new)
            else:
                p1_monkeys[m.if_false].items.append(new)
        m.items = []

amts = sorted(inspect_amt.values())
print(f"I'M BACK BABY: {amts[-1] * amts[-2]}")

global_lcm = 1
for m in monkeys.values():
    global_lcm = lcm(global_lcm, m.div_test)

p2_monkeys = deepcopy(monkeys)
inspect_amt = {m: 0 for m in p2_monkeys}
for _ in range(P2_ROUNDS):
    for m in p2_monkeys.values():
        for i in m.items:
            new = 0
            old = i
            exec(m.op)
            new %= global_lcm
            inspect_amt[m.id] += 1
            if new % m.div_test == 0:
                p2_monkeys[m.if_true].items.append(new)
            else:
                p2_monkeys[m.if_false].items.append(new)
        m.items = []

amts = sorted(inspect_amt.values())
print(f"top 100 both times! {amts[-1] * amts[-2]}")
