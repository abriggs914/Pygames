import pygame
import random
from time import sleep
import easygui
from win32api import GetSystemMetrics
from colors import *
from puzzles_list import get_puzzle_n, get_list_of_puzzles
from puzzle import *

###########################################################
##                   Design Vars                         ##
###########################################################

TITLE = "Pixel Puzzle Solver"
SCREEN_WIDTH = int(GetSystemMetrics(0) * 0.95)      # use a modified full screen approach because the pygame version
SCREEN_HEIGHT = int(GetSystemMetrics(1) * 0.9)      # had weird effects on other programs
DEFAULT_GRID_ROWS = 25
DEFAULT_GRID_COLS = 25
GRID_GROUPING = 5                                   # how many grid squares per group
GRID_SPACING = 2                                    # space between grid squares
GRID_SECTOR_SPACING = GRID_SPACING + 4              # space between grid groupings
DEFAULT_GRID_NAME = "Untitled grid"

#  Default sizing vars
DEFAULT_WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DEFAULT_GRID_SIZE = tuple(map(lambda x: x * 0.8, [min(DEFAULT_WINDOW_SIZE) for i in range(2)]))  # Square grid
DEFAULT_GRID_BORDER = tuple(map(lambda x: x * 0.82, [min(DEFAULT_WINDOW_SIZE) for i in range(2)]))  # Square border
DEFAULT_GRID_ATTRS = (DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS)

###########################################################
##                   Game Vars                           ##
###########################################################

DISPLAY = None
GRID = None
GRID_NAME = DEFAULT_GRID_NAME
GRID_SQUARES = None
GRID_HINTS = None                               # list of Rects, and

#  Modes
M_IDLE = "IDLE"
M_CREATION = "CREATION"
M_SAVE = "SAVE"
M_LOAD = "LOAD"
MODES = (M_IDLE, M_CREATION, M_LOAD, M_SAVE)
CURRENT_MODE = MODES[0]


###########################################################
###########################################################

# Get the Rect object that holds the display
def get_display_rect():
    return DISPLAY.get_rect()


# Returns the center of a rect, if no params are given, returns the center of the display.
def get_center(rect=None):
    if rect is None:
        return get_display_rect().center
    else:
        return rect.center


#  If a grid is loaded, then update display variables for drawing.
def init_grid(puzzle_in):
    global GRID, DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, GRID_SQUARES
    GRID = puzzle_in
    DEFAULT_GRID_ROWS = GRID.n_rows
    DEFAULT_GRID_COLS = GRID.n_cols
    GRID_SQUARES = None


# Calculates and returns a Rect object for the grid border. Rect is placed towards the top left of the display.
def get_grid_border_rect():
    border_w, border_h = DEFAULT_GRID_BORDER
    display_rect = get_display_rect()
    border_w_space = display_rect.width - border_w
    border_h_space = display_rect.height - border_h
    border_x = round(display_rect.left + (border_w_space * 0.1))  # left
    border_y = round(display_rect.top + (border_h_space * 0.2))  # top
    return pygame.Rect(border_x, border_y, border_w, border_h)


# Calculates and returns a Rect object for the grid. Rect is placed towards the top left of the display.
def get_grid_rect():
    grid_w, grid_h = DEFAULT_GRID_SIZE
    display_rect = get_display_rect()
    grid_w_space = display_rect.width - grid_w
    grid_h_space = display_rect.height - grid_h
    grid_x = round(display_rect.left + (grid_w_space * 0.1))  # left
    grid_y = round(display_rect.top + (grid_h_space * 0.2))  # top
    return pygame.Rect(grid_x, grid_y, grid_w, grid_h)


# Calculate and create rect objects for each desired cell of the grid. Called once to save on computations.
def calc_grid():
    grid_squares = []
    grid_rect = get_grid_rect()

    rows, cols = DEFAULT_GRID_ATTRS if GRID is None else GRID.get_rows_cols()

    row_sectors, row_rem = divmod(rows, GRID_GROUPING)
    col_sectors, col_rem = divmod(cols, GRID_GROUPING)
    x = grid_rect.left + GRID_SECTOR_SPACING
    y = grid_rect.top + GRID_SECTOR_SPACING
    x_space = (grid_rect.width - (((cols - col_sectors) * GRID_SPACING) + ((col_sectors - 1) * GRID_SECTOR_SPACING))) / cols
    y_space = (grid_rect.height - (((rows - row_sectors) * GRID_SPACING) + ((row_sectors - 1) * GRID_SECTOR_SPACING))) / rows

    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(x, y, x_space, y_space)
            if GRID is None:
                color = WHITE
            else:
                if GRID.is_wrong(r, c):
                    color = LIGHT_RED
                elif GRID.is_marked(r, c):
                    color = LIGHT_GREY
                else:
                    color = GRID.get_square_color(r, c)
            legend_key = GRID.get_legend_key(r, c)
            grid_squares.append((rect, color, legend_key))
            x += x_space
            x += GRID_SECTOR_SPACING if (c + 1) % GRID_GROUPING == 0 else GRID_SPACING
        y += y_space
        y += GRID_SECTOR_SPACING if (r + 1) % GRID_GROUPING == 0 else GRID_SPACING
        x = grid_rect.left + GRID_SECTOR_SPACING
    return grid_squares


# Draw an "x" over a rect space using a proportion of the total space and the given color
def draw_x(rect, color, fill_proportion=1):
    width = rect.width
    height = rect.height
    new_width = round(width * fill_proportion)
    new_height = round(height * fill_proportion)
    new_left = round(rect.left + ((width - new_width) / 2))
    new_top = round(rect.top + ((height - new_height) / 2))
    new_rect = pygame.Rect(new_left, new_top, new_width, new_height)
    top_left = new_rect.topleft
    bottom_right = new_rect.bottomright
    top_right = new_rect.topright
    bottom_left = new_rect.bottomleft
    pygame.draw.line(DISPLAY, color, top_left, bottom_right, 4)
    pygame.draw.line(DISPLAY, color, top_right, bottom_left, 4)


# TODO: remove this counter
h = 0

def draw_grid():
    global GRID_SQUARES, DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, DEFAULT_GRID_ATTRS, h

    # Draw grid border
    border_rect = get_grid_border_rect()
    pygame.draw.rect(DISPLAY, SUB_BACKGROUND_COLOR, border_rect)
    # Draw grid
    grid_rect = get_grid_rect()
    # pygame.draw.rect(DISPLAY, WHITE, grid_rect) # blank white square

    sleep(2)
    init_grid(get_puzzle_n(h))
    GRID_SQUARES = None
    h += 1
    if h == len(get_list_of_puzzles()):
        quit()

    GRID.set_cell_uncovered(0, 0, 1)
    # Populate the grid squares list if it is not initialized
    if GRID_SQUARES is None:
        GRID_SQUARES = calc_grid()


    # Draw each cell
    for square in GRID_SQUARES:
        rect, color, legend_key = square
        pygame.draw.rect(DISPLAY, color, rect)
        if legend_key == LEGEND["wrong"]:
            draw_x(rect, RED, 0.75)
        elif legend_key == LEGEND["marked"]:
            draw_x(rect, GREY, 0.75)


def draw_display():
    DISPLAY.fill(BACKGROUND_COLOR)
    draw_grid()

    pygame.display.update()

# Check if the user clicked the x button, then quit program
def check_quit():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


#  Run game window.
def main_loop():
    while 1:
        check_quit()
        draw_display()


#  Initialize pygame and begin the main_loop
def on_start():
    global DISPLAY
    pygame.init()
    DISPLAY = pygame.display.set_mode(DEFAULT_WINDOW_SIZE)
    pygame.display.set_caption(TITLE)
    draw_display()
    main_loop()


if __name__ == "__main__":
    on_start()
