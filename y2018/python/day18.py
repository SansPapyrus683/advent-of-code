import numpy as np
import numpy.typing as npt

OPEN = '.'
TREE = '|'
YARD = '#'

P1_TIME = 10
P2_TIME = 10 ** 9


def mat_to_str(mat: npt.NDArray[str]):
    return ''.join(''.join(row) for row in mat)


def resource_value(grid: npt.NDArray[str]):
    return (grid == TREE).sum() * (grid == YARD).sum()


area = []
with open('input/day18.txt') as read:
    for r in read.readlines():
        r = r.strip()
        assert all(c in [OPEN, TREE, YARD] for c in r)
        area.append(list(r))
area = np.array(area)

time = 0
cyc_start = -1
seen = {mat_to_str(area): time}
order = [mat_to_str(area)]
while True:
    init = area.copy()
    for r in range(len(area)):
        for c in range(len(area[r])):
            adj = init[max(r - 1, 0):r + 2, max(c - 1, 0):c + 2]
            open_amt = (adj == OPEN).sum() - (area[r, c] == OPEN)
            tree_amt = (adj == TREE).sum() - (area[r, c] == TREE)
            yard_amt = (adj == YARD).sum() - (area[r, c] == YARD)

            if area[r, c] == OPEN:
                if tree_amt >= 3:
                    area[r, c] = TREE
            elif area[r, c] == TREE:
                if yard_amt >= 3:
                    area[r, c] = YARD
            elif area[r, c] == YARD:
                if not (tree_amt > 0 and yard_amt > 0):
                    area[r, c] = OPEN

    time += 1
    if time == P1_TIME:
        print(f"resource value after {P1_TIME} mins: {resource_value(area)}")

    str_area = mat_to_str(area)
    if str_area in seen:
        cyc_start = seen[str_area]
        break
    order.append(str_area)
    seen[str_area] = time

cyc_len = len(seen) - cyc_start
equal_to = cyc_start + ((P2_TIME - cyc_start) % cyc_len)
final_array = np.array(list(order[equal_to])).reshape(area.shape)
print(f"resource value after {P2_TIME} minutes: {resource_value(final_array)}")
