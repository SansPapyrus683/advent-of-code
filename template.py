"""this file contains file io init. & some functions you might find useful"""


def chunks(lst: list, n: int):
    """source: https://stackoverflow.com/questions/312443"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def neighbors4raw(x: int, y: int) -> list[tuple[int, int]]:
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def neighbors4(x: int, y: int, x_max: int, y_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
    ] if 0 <= p[0] < y_max and 0 <= p[1] < x_max]


def neighbors8raw(x: int, y: int) -> list[tuple[int, int]]:
    return [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),
    ]


def neighbors8(x: int, y: int, x_max: int, y_max: int) -> list[tuple[int, int]]:
    return [p for p in [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1),
    ] if 0 <= p[0] < y_max and 0 <= p[1] < x_max]


# replace input.txt w/ whatever your thing is
with open("input.txt") as read:
    for i in read.readlines():
        pass
