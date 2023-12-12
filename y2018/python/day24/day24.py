import re
from itertools import count
from battle import Group, Battle, BattleRes


def strip_all(lst: list[str]) -> list[str]:
    return [s.strip() for s in lst]


def parse_status(stat: str) -> tuple[list[str], list[str]]:
    def imm(i_: str) -> list[str]:
        return strip_all(i_[10:].split(","))

    def weak(w_: str) -> list[str]:
        return strip_all(w_[8:].split(","))

    if stat.count(";") == 1:
        a, b = [s.strip() for s in stat.split(";")]
        if "weak" in a:
            return imm(b), weak(a)
        elif "immune" in a:
            return imm(a), weak(b)
        return [], []  # worst case scenario
    else:
        if "weak" in stat:
            return [], weak(stat)
        elif "immune" in stat:
            return imm(stat), []
        return [], []


imm_marker = "immune system:"
inf_marker = "infection:"
group_fmt = (r"(\d+) units each with (\d+) hit points (\([a-z;,\s]*\) )?"
             r"with an attack that does (\d+) ([a-z]*) damage at initiative (\d+)")

with open("input/day24.txt") as read:
    units = []
    state = 0
    for l in read.readlines():
        l = l.strip().lower()
        if l == imm_marker:
            assert state == 0
            state += 1
        elif l == inf_marker:
            assert state == 1
            state += 1
        else:
            res = re.findall(group_fmt, l)
            if not res:
                continue

            sz, hp, stats, atk, atk_type, init = res[0]
            stats = parse_status(stats[1:-2])
            good = True if state == 1 else False
            group = Group(
                good, int(sz), int(hp), stats[0], stats[1],
                int(atk), atk_type, int(init)
            )
            units.append(group)

print(f"remaining unit num: {Battle(units).get_res()[1]}")

for boost_amt in count(1):
    for u in units:
        if u.good:
            u.atk += 1

    outcome, rem_units = Battle(units).get_res()
    if outcome == BattleRes.WIN:
        print(f"min units given a boost & a reindeer win: {rem_units}")
        break
