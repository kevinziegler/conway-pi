#!/usr/bin/env python3

from Cell import Cell, NEIGHBOR_OFFSETS
from Grid import Grid


def dump_transition(c : Cell):
    neighbor_coords = [ f"({x + c.x},{y + c.y})" for (x,y) in NEIGHBOR_OFFSETS ]
    print(f"{str(c)} -> {[str(cell) for cell in c.neighbors]}")
    print(f"\tOffsets: {[str(coord) for coord in NEIGHBOR_OFFSETS]}")
    print(f"\tCoords: {neighbor_coords}")
    print(f"str(c)")

grid = Grid(8, 8, dump_transition)

for i in range(1):
    grid.dump()
    grid.update()
    print("Grid is:")
    print(grid.debug_str())
    grid.dump()
