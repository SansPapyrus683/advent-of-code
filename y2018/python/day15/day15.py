from functools import lru_cache
from collections import deque
from copy import deepcopy
from dataclasses import dataclass


@lru_cache
def adj(r: int, c: int) -> list[tuple[int, int]]:
    return [
        (r + 1, c), (r - 1, c),
        (r, c - 1), (r, c + 1)
    ]


@dataclass
class Unit:
    is_elf: bool
    atk: int = 3
    hp: int = 200


class Battle:
    def __init__(
            self,
            elf_data: dict[tuple[int, int], Unit],
            gob_data: dict[tuple[int, int], Unit],
            wall_pos: set[tuple[int, int]]
    ):
        self._elves, self._elf_death = deepcopy(elf_data), False
        self._goblins, self._gob_death = deepcopy(gob_data), False
        self._walls = deepcopy(wall_pos)
        self._round = 0
        self._simmed = False

    def sim(self):
        if self._simmed:
            raise RuntimeError("can only simulate a battle once")

        while self._goblins and self._elves:
            everything = self._goblins | self._elves
            for pos in sorted(everything):
                unit = everything[pos]
                if unit.hp < 0:  # bruh you're supposed to be dead
                    continue

                good = self._elves if unit.is_elf else self._goblins
                bad = self._goblins if unit.is_elf else self._elves
                if not bad:
                    break

                has_bad = [(bad[n].hp, n) for n in adj(*pos) if n in bad]
                if not has_bad:
                    in_range = []

                    frontier = deque([pos])
                    visited = {pos: 0}
                    while frontier:
                        curr = frontier.popleft()
                        curr_dist = visited[curr]
                        for n in adj(*curr):
                            if (n not in self._elves
                                    and n not in self._goblins
                                    and n not in self._walls
                                    and n not in visited):
                                frontier.append(n)
                                visited[n] = curr_dist + 1

                    for b in bad:
                        in_range.extend([
                            (visited[n], n) for n in adj(*b)
                            if n in visited
                        ])
                    if not in_range:
                        continue

                    target = min(in_range)[1]
                    t_dist = {target: 0}
                    frontier = deque([target])
                    while frontier:
                        curr = frontier.popleft()
                        curr_dist = t_dist[curr]
                        for n in adj(*curr):
                            if n in visited and n not in t_dist:
                                frontier.append(n)
                                t_dist[n] = curr_dist + 1

                    move_to = [(t_dist[n], n) for n in adj(*pos) if n in visited]
                    result = min(move_to)[1]
                    good[result] = good.pop(pos)
                    pos = result
                    has_bad = [(bad[n].hp, n) for n in adj(*pos) if n in bad]

                # attack
                if has_bad:
                    _, atk_pos = min(has_bad)
                    to_atk = bad[atk_pos]
                    to_atk.hp -= unit.atk
                    if to_atk.hp <= 0:
                        if to_atk.is_elf:
                            self._elf_death = True
                        else:
                            self._gob_death = True
                        del bad[atk_pos]
            else:
                self._round += 1

        self._simmed = True

    def results(self) -> tuple[bool, int]:
        if not self._simmed:
            raise RuntimeError("battle needs to be simulated first")
        if self._elves:
            return True, self._round * sum(e.hp for e in self._elves.values())
        return False, self._round * sum(g.hp for g in self._goblins.values())

    def winning_death(self) -> bool:
        if not self._simmed:
            raise RuntimeError("battle needs to be simulated first")
        return self._elf_death if self._elves else self._gob_death


elves = {}
goblins = {}
walls = set()
with open('day15.txt') as read:
    for r, row in enumerate(read.readlines()):
        row = row.strip()
        for c, square in enumerate(row):
            if square == 'G':
                goblins[(r, c)] = Unit(False)
            elif square == 'E':
                elves[(r, c)] = Unit(True)
            elif square == '#':
                walls.add((r, c))

battle = Battle(elves, goblins, walls)
battle.sim()
print(f"initial outcome: {battle.results()[1]}")

min_atk = 4
while True:
    for e in elves.values():
        e.atk = min_atk

    battle = Battle(elves, goblins, walls)
    battle.sim()
    won, outcome = battle.results()
    if won and not battle.winning_death():
        print(f"winning outcome with 0 deaths: {outcome}")
        print(f"(min atk power was {min_atk} if you were curious)")
        break
    min_atk += 1
