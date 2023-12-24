import re
from dataclasses import dataclass


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
with open("melt_away.txt") as read:
    for h in read.readlines():
        if res := re.findall(hail_fmt, h):
            hails.append(Hailstone(*[int(i) for i in res[0]]))

intersections = 0
lo_pos = 200000000000000
hi_pos = 400000000000000
for i in range(len(hails)):
    for j in range(i + 1, len(hails)):
        intersections += hails[i].cross_paths(hails[j], lo_pos, hi_pos)

print(f"as always, the morning solution works just fine... {intersections}")
