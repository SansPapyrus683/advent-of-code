from typing import Optional

ELF_NUM = 3012210


class Elf:
    def __init__(self, has_present: bool):
        self.has_present = has_present
        self.nxt: Optional["Elf"] = None


elves = [Elf(True) for i in range(ELF_NUM)]
for e in range(len(elves)):
    elves[e].nxt = elves[(e + 1) % ELF_NUM]

at = elves[0]
for _ in range(ELF_NUM - 1):
    at.nxt.has_present = False
    at.nxt = at.nxt.nxt
    at = at.nxt

for e in range(len(elves)):
    if elves[e].has_present:
        print(f"final elf: {e + 1}")
        break
