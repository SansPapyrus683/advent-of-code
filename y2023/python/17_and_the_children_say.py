import enum
import heapq
import sys

# max travel distance and min distance to be able to turn
P1_DRILL = 3, 1
P2_DRILL = 10, 4


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def turn(self) -> list["Direction"]:
        if self in [self.UP, self.DOWN]:
            return [self.LEFT, self.RIGHT]
        return [self.UP, self.DOWN]

    def delta(self) -> tuple[int, int]:
        return {
            self.UP: (-1, 0),
            self.DOWN: (1, 0),
            self.LEFT: (0, -1),
            self.RIGHT: (0, 1)
        }[self]


def min_heat_loss(grid: list[list[int]], max_dist: int, turn_thresh: int):
    # is this properly formatted? who knows.
    min_loss = [[
        [float("inf") for _ in range(len(Direction))] for _ in range(len(grid[0]))
    ] for _ in range(len(grid))]
    min_loss[0][0] = [0 for _ in range(len(Direction))]
    frontier = [(0, (0, 0, d.value - 1)) for d in Direction]
    while frontier:
        curr_cost, (cr, cc, cd) = heapq.heappop(frontier)
        if min_loss[cr][cc][cd] != curr_cost:
            continue

        if cr == len(grid) - 1 and cc == len(grid[0]) - 1:
            return curr_cost

        for nd in Direction(cd + 1).turn():
            delta = nd.delta()
            n_cost = curr_cost
            nr, nc = cr, cc
            for d in range(1, max_dist + 1):
                nr, nc = nr + delta[0], nc + delta[1]
                if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
                    break

                n_cost += grid[nr][nc]
                if n_cost < min_loss[nr][nc][nd.value - 1] and d >= turn_thresh:
                    min_loss[nr][nc][nd.value - 1] = n_cost
                    heapq.heappush(frontier, (n_cost, (nr, nc, nd.value - 1)))

    assert False, "something went horribly wrong"


grid = [[int(i) for i in r.strip()] for r in sys.stdin]

print(f"today was nice: {min_heat_loss(grid, *P1_DRILL)}")
print(f"t100 for p2 asw: {min_heat_loss(grid, *P2_DRILL)}")
