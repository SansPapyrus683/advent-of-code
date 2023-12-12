import enum


class Direction(enum.Enum):
    NORTH = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()
    WEST = enum.auto()

    def right(self):
        if self == self.NORTH:
            return self.EAST
        elif self == self.SOUTH:
            return self.WEST
        elif self == self.EAST:
            return self.SOUTH
        elif self == self.WEST:
            return self.NORTH

    def left(self):
        if self == self.NORTH:
            return self.WEST
        elif self == self.SOUTH:
            return self.EAST
        elif self == self.EAST:
            return self.NORTH
        elif self == self.WEST:
            return self.SOUTH
