import enum


class Tile:
    CLAY = enum.auto()
    SAND = enum.auto()
    STILL = enum.auto()
    FLOW = enum.auto()
    SRC = enum.auto()


TILE_STR = {
    Tile.CLAY: '#',
    Tile.SAND: '.',
    Tile.STILL: '~',
    Tile.FLOW: '|',
    Tile.SRC: '+',
}
