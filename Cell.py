from itertools import product
from typing import Any, Callable

NEIGHBOR_OFFSETS = list(product([0, 1, -1], repeat=2))

class Cell:
    def __init__(
            self,
            x: int,
            y: int,
            alive: bool,
            grid: Callable[[int, int], 'Cell'],
            on_transition: Callable[['Cell'], Any]
    ):
        self.alive = alive
        self.x = x
        self.y = y
        self.grid = grid
        self.on_transition = on_transition

    @property
    def neighbors(self):
        return [
            self.grid(self.x + x, self.y + y)
            for (x, y) in NEIGHBOR_OFFSETS if (x, y) != (0, 0)
        ]

    def calculate_next(self):
        living = len([cell for cell in self.neighbors if cell.alive])
        self.next = (self.alive and living in range(2,4)) or living == 3

    def transition(self):
        self.alive = self.next
        self.on_transition(self)

    def __str__(self):
        return f"CELL({self.x},{self.y},{'A' if self.alive else 'D' })"


class NullCell(Cell):
    def __init__(self):
        super().__init__(-1, -1, False, lambda x, y: NullCell(), lambda _: None)

    def __str__(self):
        return "NULLCELL"
