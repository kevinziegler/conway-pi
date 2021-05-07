from time import sleep

from Cell import Cell
from Grid import Grid

from curses import wrapper, use_default_colors

REFRESH_RATE=0.25

def draw_cell(scr, cell: Cell) -> None:
    max_y, max_x = scr.getmaxyx()

    if cell.x > max_x-2 or cell.y > max_y:
        return

    display = "X" if cell.alive else " "
    scr.addstr(cell.y, cell.x, display)

def conway(scr):
    grid_y, grid_x = scr.getmaxyx()
    grid = Grid(
        grid_x-1,
        grid_y,
        lambda cell: draw_cell(scr, cell),
        lambda _ : None
    )

    use_default_colors()

    while True:
        grid.update()
        scr.addstr(0,0, f"State: {grid.state}")
        sleep(REFRESH_RATE)
        scr.refresh()

wrapper(conway)
