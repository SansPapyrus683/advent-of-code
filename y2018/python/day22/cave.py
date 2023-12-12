import enum


class Region(enum.Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

    def compatible(self) -> list["Tool"]:
        if self == Region.ROCKY:
            return [Tool.TORCH, Tool.GEAR]
        elif self == Region.WET:
            return [Tool.GEAR, Tool.NONE]
        elif self == Region.NARROW:
            return [Tool.NONE, Tool.TORCH]
        raise ValueError('bruh')


class Tool(enum.Enum):
    NONE = 0
    TORCH = 1
    GEAR = 2

    def compatible(self) -> list[Region]:
        if self == Tool.NONE:
            return [Region.WET, Region.NARROW]
        elif self == Tool.TORCH:
            return [Region.ROCKY, Region.NARROW]
        elif self == Tool.GEAR:
            return [Region.ROCKY, Region.WET]
        raise ValueError('bruh')
