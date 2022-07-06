from typing import Optional

ELF_NUM = 3012210


class Elf:
    def __init__(self, has_present: bool):
        self.has_present = has_present
        self.prev: Optional["Elf"] = None
        self.nxt: Optional["Elf"] = None


elves = [Elf(True) for i in range(ELF_NUM)]
for e in range(len(elves)):
    elves[e].nxt = elves[(e + 1) % ELF_NUM]
    elves[e].prev = elves[(e - 1) % ELF_NUM]

at = elves[0]
steal_from = elves[ELF_NUM // 2]
skip_twice = ELF_NUM % 2 != 0
for i in range(ELF_NUM - 1):
    steal_from.has_present = False

    prev = steal_from.prev
    nxt = steal_from.nxt
    prev.nxt = nxt
    nxt.prev = prev

    at = at.nxt
    steal_from = steal_from.nxt.nxt if skip_twice else steal_from.nxt
    skip_twice = not skip_twice

for e in range(len(elves)):
    if elves[e].has_present:
        print(f"final elf: {e + 1}")
        break
