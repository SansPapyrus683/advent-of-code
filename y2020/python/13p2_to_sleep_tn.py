"""
solves part 2 of the problem
but it's like 99% shorter
"""

from math import lcm


def min_time(
    wanted_modulos: list[tuple[int, int]], search_from: int = 0, increment: int = 1
):
    if not wanted_modulos:
        return search_from
    satisfied = wanted_modulos[0]
    while search_from % satisfied[0] != satisfied[1]:
        search_from += increment
    return min_time(wanted_modulos[1:], search_from, lcm(increment, satisfied[0]))


buses = [int(b) if b.lower() != "x" else -1 for b in input().split(",")]

buses_and_mods = [(b, (b - v) % b) for v, b in enumerate(buses) if b != -1]
print(f"boy this method was so much simpler lol: {min_time(buses_and_mods)}")
