from string import ascii_lowercase


def react(poly: str) -> str:
    assert poly.isalpha()

    while True:
        at = 0
        after_step = []
        while at < len(poly):
            if at == len(poly) - 1:
                after_step.append(poly[at])
                at += 1
                continue

            curr1, curr2 = poly[at], poly[at + 1]
            if curr1.lower() == curr2.lower() and curr1 != curr2:
                at += 2
            else:
                after_step.append(curr1)
                at += 1

        if len(after_step) == len(poly):
            break
        poly = ''.join(after_step)

    return poly


polymer = open('day5.txt').readline().strip()

print(f"length after reacting: {len(react(polymer))}")

# this takes a long time to run, so just be patient
smallest = float('inf')
for a in ascii_lowercase:
    removed = ''.join(c for c in polymer if c.lower() != a)
    removed = react(removed)
    if len(removed) < smallest:
        smallest = len(removed)

print(f"smallest length after removing a char: {smallest}")
