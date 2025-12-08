import sys
import math

CUTOFF = 1000


class DisjointSets:
    """sauce: https://usaco.guide/gold/dsu?lang=py#implementation"""
    def __init__(self, size: int) -> None:
        self.parents = [i for i in range(size)]
        self.sizes = [1 for _ in range(size)]

    def find(self, x: int) -> int:
        if self.parents[x] == x:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def unite(self, x: int, y: int) -> bool:
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False

        if self.sizes[x_root] < self.sizes[y_root]:
            x_root, y_root = y_root, x_root

        self.parents[y_root] = x_root
        self.sizes[x_root] += self.sizes[y_root]
        return True


def sq_dist(p1: list[int], p2: list[int]) -> int:
    return sum((a - b) ** 2 for a, b in zip(p1, p2))


points = []
for pt in sys.stdin:
    points.append([int(i) for i in pt.split(",")])

edges = []
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        edges.append((sq_dist(points[i], points[j]), i, j))
edges.sort()

circuits = DisjointSets(len(points))
linked = 0
for v, (_, b1, b2) in enumerate(edges):
    linked += circuits.unite(b1, b2)
    if v == CUTOFF - 1:
        sizes = []
        for i in range(len(points)):
            if circuits.find(i) == i:
                sizes.append(circuits.sizes[i])
        sizes.sort(reverse=True)

        top3 = math.prod(sizes[:3])
        print(f"wanted food truck lol: {top3}")

    if linked == len(points) - 1:
        ans = points[b1][0] * points[b2][0]
        print(f"took me a bit to realize it was l2 norm haha: {ans}")
        break
