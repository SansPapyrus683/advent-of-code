import enum


# i realize i could have just used raw characters... oh well...
class Track(enum.Enum):
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()
    SLASH = enum.auto()
    BACKSLASH = enum.auto()
    PLUS = enum.auto()


class Cart(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


CHAR_MAP = {
    '-': Track.HORIZONTAL,
    '|': Track.VERTICAL,
    '/': Track.SLASH,
    '\\': Track.BACKSLASH,
    '+': Track.PLUS,
    '>': Cart.RIGHT,
    '<': Cart.LEFT,
    '^': Cart.UP,
    'v': Cart.DOWN
}

SLASH_TURNS = {
    Track.SLASH: {
        Cart.RIGHT: Cart.UP,
        Cart.LEFT: Cart.DOWN,
        Cart.UP: Cart.RIGHT,
        Cart.DOWN: Cart.LEFT
    },
    Track.BACKSLASH: {
        Cart.RIGHT: Cart.DOWN,
        Cart.LEFT: Cart.UP,
        Cart.UP: Cart.LEFT,
        Cart.DOWN: Cart.RIGHT
    }
}

track = []
carts = []
with open('input/day13.txt') as read:
    for i, row in enumerate(read.readlines()):
        track.append([])
        for j, c in enumerate(row.rstrip()):
            type_ = CHAR_MAP.get(c, None)
            if isinstance(type_, Cart):
                match type_:
                    case Cart.LEFT | Cart.RIGHT:
                        track[-1].append(Track.HORIZONTAL)
                    case Cart.UP | Cart.DOWN:
                        track[-1].append(Track.VERTICAL)
                carts.append([[i, j], type_, 0])
            else:
                track[-1].append(type_)

first_crash = True
while len(carts) > 1:
    carts.sort()
    occupied = {tuple(c[0]): v for v, c in enumerate(carts)}
    still_in = {c for c in range(len(carts))}
    for v, (pos, type_, turn_num) in enumerate(carts):
        del occupied[tuple(pos)]
        match type_:
            case Cart.RIGHT:
                pos[1] += 1
            case Cart.LEFT:
                pos[1] -= 1
            case Cart.UP:
                pos[0] -= 1
            case Cart.DOWN:
                pos[0] += 1

        if tuple(pos) in occupied:
            if first_crash:
                print(f"first crash position: {pos[1]},{pos[0]}")
                first_crash = False
            still_in.remove(v)
            still_in.remove(occupied.pop(tuple(pos)))
        occupied[tuple(pos)] = v

        assert track[pos[0]][pos[1]] is not None
        match track[pos[0]][pos[1]]:
            case Track.SLASH | Track.BACKSLASH:
                carts[v][1] = SLASH_TURNS[track[pos[0]][pos[1]]][type_]
            case Track.PLUS:
                if turn_num % 3 == 0:
                    carts[v][1] = Cart((carts[v][1].value - 1) % len(Cart))
                elif turn_num % 3 == 2:
                    carts[v][1] = Cart((carts[v][1].value + 1) % len(Cart))
                carts[v][2] += 1

    carts = [carts[c] for c in still_in]

if len(carts) == 1:
    print(f"position of last cart: {carts[0][0][1]},{carts[0][0][0]}")
else:
    print("uuhh all the carts killed each other lol idt that's should happen")
