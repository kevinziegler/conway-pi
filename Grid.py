from hashlib import md5
from random import choice
from typing import Any, Callable

from Cell import Cell, NullCell

class Grid:
    def __init__(
        self,
        size_x: int,
        size_y: int,
        on_transition: Callable[[Cell], Any],
        on_reset: Callable[[Cell], Any]
    ):
        self.dim_x = range(size_x)
        self.dim_y = range(size_y)
        self.on_transition = on_transition
        self.resets = 0

        self.__reset_cells()
        self.__reset_run_metrics()

    @property
    def state(self) -> str:
        return md5(str(self).encode("utf-8")).hexdigest()

    def cell(self, x: int, y: int) -> Cell:
        if not (y in self.dim_y and x in self.dim_x):
            return NullCell()

        return self.cells[y][x]

    def reset(self) -> None:
        self.resets = self.resets + 1
        self.__reset_cells()
        self.__reset_run_metrics()

    def update(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.calculate_next()

        for row in self.cells:
            for cell in row:
                cell.transition()

        if self.state in self.history:
            self.reset()

        else:
            self.iterations = self.iterations + 1
            self.history[self.state] = self.iterations

    def __init_cell(self, x: int, y: int) -> Cell:
        init_state = choice([True, False])
        return Cell(x, y, init_state, self.cell, self.on_transition)

    def __reset_cells(self) -> None:
        self.cells = [[
            self.__init_cell(x, y) for x in self.dim_x
        ] for y in self.dim_y ]

    def __reset_run_metrics(self) -> None:
        self.iterations = 0
        self.history = {}

    def debug_str(self) -> str:
        return "\n".join([
            "".join(str(cell) for cell in row) for row in self.cells
        ])

    def dump(self):
        for y in self.dim_y:
            for x in self.dim_x:
                print(f"Cell at: ({x},{y})")
                print(f"\t{str(self.cell(x,y))}")

    def __str__(self) -> str:
        return "\n".join([
            "".join([ "X" if cell.alive else " " for cell in row ])
            for row in self.cells
        ])
