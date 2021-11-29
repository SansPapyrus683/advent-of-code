from typing import List

said = [2, 15, 0, 9, 1, 20]


def all_said_numbers(numbers: List[int], sim_until: int) -> List[int]:
    numbers = numbers.copy()
    recent = {}
    for v, n in enumerate(numbers[:-1]):  # don't process the last element just yet
        recent[n] = v

    for _ in range(sim_until - len(numbers)):  # just brute force simulate
        previous = numbers[-1]
        if previous not in recent:
            numbers.append(0)
        else:
            # no idea why the -1 is necessary, think it's because of that 0-indexing
            numbers.append(len(numbers) - 1 - recent[previous])
        # -2 because we already appended the thing, so we have to go back 1 more
        recent[numbers[-2]] = len(numbers) - 1 - 1
    return numbers


PART1 = 2020
PART2 = 30000000
print(f"this is the most boring game of All Time: {all_said_numbers(said, PART1)[-1]}")
print(f"who has patience to recite till the THIRTY MILLIONTH NUM: {all_said_numbers(said, PART2)[-1]}")
