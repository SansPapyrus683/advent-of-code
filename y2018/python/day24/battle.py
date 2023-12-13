from dataclasses import dataclass
from copy import deepcopy
import enum


@dataclass
class Group:
    good: bool
    sz: int
    hp: int
    immune: list[str]
    weak: list[str]
    atk: int
    atk_type: str
    init: int

    @property
    def eff_power(self) -> int:
        return self.sz * self.atk

    def dmg(self, other: "Group") -> int:
        if self.atk_type in other.immune:
            return 0
        elif self.atk_type in other.weak:
            return self.eff_power * 2
        return self.eff_power

    def atk_other(self, other: "Group") -> None:
        dmg = self.dmg(other)
        dead_units = dmg // other.hp
        other.sz = max(other.sz - dead_units, 0)


class BattleRes(enum.Enum):
    WIN = enum.auto()
    LOSE = enum.auto()
    TIE = enum.auto()


class Battle:
    def __init__(self, units: list[Group]):
        self._units = deepcopy(units)
        self._simmed = False
        self._res = self._sim_res()

    def _step(self):
        # sort by power & tiebreak by initiative for the targeting order
        self._units.sort(key=lambda u_: (u_.eff_power, u_.init_refl), reverse=True)

        targeted = [False for _ in range(len(self._units))]
        to_atk = [-1 for _ in range(len(self._units))]
        for v1, u1 in enumerate(self._units):
            best = (-1, (0, 0, 0))
            for v2, u2 in enumerate(self._units):
                if v1 == v2 or targeted[v2] or u1.good == u2.good:
                    continue
                val = u1.dmg(u2), u2.eff_power, u2.init
                if val > best[1]:
                    best = v2, val
            if best[0] != -1 and best[1][0] != 0:
                to_atk[v1] = best[0]
                targeted[best[0]] = True

        atk_inds = list(range(len(self._units)))
        # for atk order it's just decreasing initiative
        atk_inds.sort(key=lambda i_: self._units[i_].init, reverse=True)
        for i in atk_inds:
            # dead, no use attacking
            if self._units[i].sz == 0 or to_atk[i] == -1:
                continue
            u1, u2 = self._units[i], self._units[to_atk[i]]
            u1.atk_other(u2)

        self._units = [u for u in self._units if u.sz > 0]

    def _sim_res(self) -> BattleRes:
        last_amt = sum(u.sz for u in self._units)
        while len({u.good for u in self._units}) > 1:
            self._step()
            new_amt = sum(u.sz for u in self._units)
            if new_amt == last_amt:
                return BattleRes.TIE
            last_amt = new_amt
        return BattleRes.WIN if self._units[0].good else BattleRes.LOSE

    def get_res(self) -> tuple[BattleRes, int]:
        return self._res, sum(u.sz for u in self._units)
