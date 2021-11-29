class Cup:
    def __init__(self, val: int, next_: "Cup" = None):
        self.val = val
        self.next = next_

    def __repr__(self):
        return f"Cup{{val={self.val},nextVal={self.next.val}}}"

    def trav(self, amt: int):
        val = self.next
        for _ in range(amt - 1):
            val = val.next
        return val


def simulate(circle: [Cup], amt: int = 100) -> [Cup]:
    curr = circle[0]
    highest = max(c.val for c in circle)
    circle.sort(key=lambda c: c.val)  # make it a list of the values to indices (off by one, keep that in mind)
    for _ in range(amt):
        taken = [curr.next, curr.trav(2), curr.trav(3)]
        no_no_vals = [c.val for c in taken]

        destination = highest if curr.val == 1 else curr.val - 1
        while destination in no_no_vals:
            destination = highest if destination == 1 else destination - 1

        curr.next = curr.trav(4)
        insert_after = circle[destination - 1]
        taken[-1].next = insert_after.next
        insert_after.next = taken[0]
        curr = curr.next
    return circle


def order(circle: [Cup]) -> str:
    start = circle[0]
    pos = circle[0]
    result = str(pos.val)
    while pos.next != start:
        pos = pos.next
        result += str(pos.val)
    return result


cups = [int(i) for i in "467528193"]

p1_cups = [Cup(c) for c in cups]
for i in range(len(p1_cups)):
    p1_cups[i].next = p1_cups[(i + 1) % len(p1_cups)]
simulate(p1_cups, 100)
print(f"ngl i kinda want to kill this crab: {order(p1_cups)[1:]}")

p2_cups = [Cup(c) for c in cups + [i for i in range(max(cups) + 1, 10 ** 6 + 1)]]
for i in range(len(p2_cups)):
    p2_cups[i].next = p2_cups[(i + 1) % len(p2_cups)]
simulate(p2_cups, 10 ** 7)
cup1 = p2_cups[0]
print(f"where did the crab even get all those cups lol: {(cup1.next.val * cup1.trav(2).val)}")
