import re
import sys
from dataclasses import dataclass
import sympy as sp  # who knows what the standard alias is


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    def cross_paths(self, h: "Hailstone", min_pos: int, max_pos: int):
        """https://stackoverflow.com/a/2932601/12128483"""
        dx = self.x - h.x
        dy = self.y - h.y
        det = h.vx * self.vy - h.vy * self.vx
        if det == 0:
            return False

        # if u&v (in the SO link) >= 0 the hailstones intersect
        u = -(dy * h.vx - dx * h.vy) / det
        v = -(dy * self.vx - dx * self.vy) / det
        if u >= 0 and v >= 0:
            return all(min_pos <= p <= max_pos for p in [
                self.x + u * self.vx,
                self.y + u * self.vy,
                h.x + v * h.vx,
                h.y + v * h.vy
            ])
        return False


hail_fmt = r"(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*@\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)"
hails = []
for h in sys.stdin:
    if res := re.findall(hail_fmt, h):
        hails.append(Hailstone(*[int(i) for i in res[0]]))

lo_pos = 200000000000000
hi_pos = 400000000000000
intersections = 0
for i in range(len(hails)):
    for j in range(i + 1, len(hails)):
        intersections += hails[i].cross_paths(hails[j], lo_pos, hi_pos)

x, y, z, vx, vy, vz = sp.symbols("x y z vx vy vz")
equations = []
solve_for = [x, y, z, vx, vy, vz]
for v, h in enumerate(hails[:4]):
    t = sp.Symbol(f"t{v}")
    solve_for.append(t)
    equations.extend([
        x + t * vx - (h.x + t * h.vx),
        y + t * vy - (h.y + t * h.vy),
        z + t * vz - (h.z + t * h.vz)
    ])
res = sp.solve(equations, solve_for, dict=True)
if not res:
    raise RuntimeError("haha your p2 input is bugged L")
res = res[0]
pos_sum = res[x] + res[y] + res[z]

print(f"as always, the morning solution works just fine... {intersections}")
print(f"and p2 today was just 'do you know a CAS': {pos_sum}")
