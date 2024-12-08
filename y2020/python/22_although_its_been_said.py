import sys


def recursive_combat(first: [int], second: [int]) -> (int, [int], [int]):
    """
    this thing returns a tuple
    first element is who won- 1 is p1, 2 is p2
    and the following is the remaining decks of the stuff and yeah
    """
    first = first.copy()  # make sure nothing wonky happens because of list mutability
    second = second.copy()
    seen_configs = set()
    immediate_prev = (tuple(first), tuple(second))
    while all([first, second]):
        if (tuple(first), tuple(second)) in seen_configs:
            return 1, first, second
        next1 = first.pop(0)
        next2 = second.pop(0)
        if next1 <= len(first) and next2 <= len(second):
            if recursive_combat(first[:next1], second[:next2])[0] == 1:
                first.extend([next1, next2])
            else:
                second.extend([next2, next1])
        else:
            if next1 > next2:
                first.extend([next1, next2])
            else:
                second.extend([next2, next1])
        seen_configs.add(immediate_prev)
        immediate_prev = tuple(first), tuple(second)
    if first:
        return 1, first, second
    else:
        return 2, first, second


p1, p2 = [p.split("\n") for p in sys.stdin.read().split("\n\n")]
player1 = [int(c) for c in p1 if c.isdigit()]
player2 = [int(c) for c in p2 if c.isdigit()]
starting1 = player1.copy()
starting2 = player2.copy()

while all([player1, player2]):
    p1_next = player1.pop(0)
    p2_next = player2.pop(0)
    if p1_next > p2_next:
        player1.extend([p1_next, p2_next])
    else:
        player2.extend([p2_next, p1_next])

winner = player1 if player1 else player2
p1_total = sum((v + 1) * c for v, c in enumerate(reversed(winner)))
print(p1_total)

recursive_result = recursive_combat(starting1, starting2)
p2_total = sum(
    (v + 1) * c for v, c in enumerate(reversed(recursive_result[recursive_result[0]]))
)
print(p2_total)
