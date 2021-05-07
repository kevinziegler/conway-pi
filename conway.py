#!/usr/bin/env python3
from random import choice
from hashlib import md5
from itertools import product
from time import sleep
from typing import Callable

import curses

REFRESH_RATE=0.20
GRID_X=64
GRID_Y=32

class Grid:
    def __init__(self, size_x: int, size_y: int, on_transition):
        self.dim_x = range(size_x)
        self.dim_y = range(size_y)
        self.on_transition = on_transition
        self.resets = 0

        self.__reset_cells()
        self.__reset_run_metrics()

    @property
    def state(self):
        return md5(str(self).encode("utf-8")).hexdigest()

    def cell_at(self, x: int, y: int):
        if not (y in self.dim_y and x in self.dim_x):
            return None

        return self.cells[y][x]

    def reset(self):
        self.resets = self.resets + 1
        self.__reset_cells()
        self.__reset_run_metrics()

    def update(self):
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

    def __reset_cells(self):
        cell = lambda x, y: Cell(
            self,
            choice([True, False]),
            x,
            y,
            self.on_transition
        )

        self.cells = [ [cell(x, y) for x in self.dim_x] for y in self.dim_y ]

    def __reset_run_metrics(self):
        self.iterations = 0
        self.history = {}

    def __str__(self):
        return "\n".join([
            "".join([ "X" if cell.alive else " " for cell in row ])
            for row in self.cells
        ])


class Cell:
    def __init__(self, grid: Grid, alive: bool, x: int, y: int, on_transition: Callable):
        self.grid = grid
        self.alive = alive
        self.x = x
        self.y = y
        self.on_transition = on_transition

    @property
    def neighbors(self):
        coords = [
            (self.x + x, self.y + y)
            for (x, y) in product([0, 1, -1], repeat=2) if (x, y) != (0, 0)
        ]

        return [ self.grid.cell_at(x,y) for (x,y) in coords ]

    def calculate_next(self):
        living = len([cell for cell in self.neighbors if cell and cell.alive])
        self.next = (self.alive and living in range(2,4)) or living == 3

    def transition(self):
        self.alive = self.next
        self.next = None
        self.on_transition(self)

    def __str__(self):
        return f"CELL({self.x},{self.y},{'A' if self.alive else 'D' })"



def curses_draw_cell(scr, cell: Cell):
    max_y, max_x = scr.getmaxyx()

    if cell.x > max_x-2 or cell.y > max_y:
        return

    display = "X" if cell.alive else " "
    scr.addstr(cell.y, cell.x, display)


def conway(scr):
    grid_y, grid_x = scr.getmaxyx()
    grid = Grid(grid_x-1, grid_y, lambda cell: curses_draw_cell(scr, cell))

    while True:
        grid.update()
        scr.addstr(0,0, f"State: {grid.state}")
        sleep(REFRESH_RATE)
        scr.refresh()

curses.wrapper(conway)
