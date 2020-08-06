import pygame
import random
from time import sleep
import easygui
from win32api import GetSystemMetrics
from colors import *
from puzzles_list import get_puzzle_n, get_puzzle_id, get_list_of_puzzles
from puzzle import *

###########################################################
##                   Design Vars                         ##
###########################################################

TITLE = "Pixel Puzzle Solver"
SCREEN_WIDTH = int(GetSystemMetrics(0) * 0.95)  # use a modified full screen approach because the pygame version
SCREEN_HEIGHT = int(GetSystemMetrics(1) * 0.9)  # had weird effects on other programs
DEFAULT_GRID_ROWS = 25
DEFAULT_GRID_COLS = 25
GRID_GROUPING = 5  # how many grid squares per group
GRID_SPACING = 2  # space between grid squares
GRID_SECTOR_SPACING = GRID_SPACING + 4  # space between grid groupings
DEFAULT_GRID_NAME = "Untitled grid"

#  Default sizing vars
DEFAULT_WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DEFAULT_GRID_SIZE = tuple(map(lambda x: x * 0.85, [min(DEFAULT_WINDOW_SIZE) for i in range(2)]))  # Square grid
DEFAULT_GRID_BORDER = tuple(map(lambda x: x * 0.87, [min(DEFAULT_WINDOW_SIZE) for i in range(2)]))  # Square border
DEFAULT_GRID_ATTRS = (DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS)

###########################################################
##                   Game Vars                           ##
###########################################################

DISPLAY = None
GRID = None                                 # Puzzle object, initialized in init_grid
GRID_NAME = DEFAULT_GRID_NAME
GRID_SQUARES = None                         # List of Rects for grid cells
GRID_HINTS = None                           # List of text objects for hints

#  Modes
M_IDLE = "IDLE"
M_CREATION = "CREATION"
M_SAVE = "SAVE"
M_LOAD = "LOAD"
MODES = (M_IDLE, M_CREATION, M_LOAD, M_SAVE)
CURRENT_MODE = MODES[0]


###########################################################
###########################################################


# Create and return text objects for blitting
def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# Get the Rect object that holds the display
def get_display_rect():
    return DISPLAY.get_rect()


# Returns the center of a rect, if no params are given, returns the center of the display.
def get_center(rect=None):
    if rect is None:
        return get_display_rect().center
    else:
        return rect.center


# If a grid is loaded, then update display variables for drawing.
def init_grid(puzzle_in):
    global GRID, GRID_NAME, DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, GRID_SQUARES, GRID_HINTS
    print("puzzle_in:", puzzle_in)
    GRID = puzzle_in
    GRID_NAME = GRID.name
    DEFAULT_GRID_ROWS = GRID.n_rows
    DEFAULT_GRID_COLS = GRID.n_cols
    GRID_SQUARES = calc_grid()
    GRID_HINTS = init_hints()


# Calculates and returns a Rect object for the grid border. Rect is placed towards the top left of the display.
def get_grid_border_rect():
    border_w, border_h = DEFAULT_GRID_BORDER
    display_rect = get_display_rect()
    border_w_space = display_rect.width - border_w
    border_h_space = display_rect.height - border_h
    # border_x = round(display_rect.left + (border_w_space * 0.2))  # left
    # border_y = round(display_rect.top + (border_h_space * 0.9))  # top
    border_x = round(display_rect.left + (display_rect.width * 0.12))  # left
    border_y = round(display_rect.top + (display_rect.height * 0.12))  # top
    return pygame.Rect(border_x, border_y, border_w, border_h)


# Calculates and returns a Rect object for the grid. Rect is placed towards the top left of the display.
def get_grid_rect():
    grid_w, grid_h = DEFAULT_GRID_SIZE
    display_rect = get_display_rect()
    grid_w_space = display_rect.width - grid_w
    grid_h_space = display_rect.height - grid_h
    # grid_x = round(display_rect.left + (grid_w_space * 0.2))  # left
    # grid_y = round(display_rect.top + (grid_h_space * 0.9))  # top
    grid_x = round(display_rect.left + (display_rect.width * 0.12))  # left
    grid_y = round(display_rect.top + (display_rect.height * 0.12))  # top
    return pygame.Rect(grid_x, grid_y, grid_w, grid_h)


def get_vertical_hints_rect():
    display_rect = get_display_rect()
    grid_rect = get_grid_border_rect()
    top = 0
    left = grid_rect.left
    width = grid_rect.width
    height = grid_rect.top - display_rect.top
    return pygame.Rect(left, top, width, height)


def get_horizontal_hints_rect():
    display_rect = get_display_rect()
    grid_rect = get_grid_border_rect()
    top = grid_rect.top
    left = 0
    width = grid_rect.left - display_rect.left
    height = grid_rect.height
    return pygame.Rect(left, top, width, height)


# Calculate and create rect objects for each desired cell of the grid. Called once to save on computations.
def calc_grid():
    grid_squares = []
    grid_rect = get_grid_rect()

    rows, cols = DEFAULT_GRID_ATTRS if GRID is None else GRID.get_rows_cols()

    row_sectors, row_rem = divmod(rows, GRID_GROUPING)
    col_sectors, col_rem = divmod(cols, GRID_GROUPING)
    x = grid_rect.left + GRID_SECTOR_SPACING
    y = grid_rect.top + GRID_SECTOR_SPACING
    x_space = (grid_rect.width - (
                ((cols - col_sectors - 1) * GRID_SPACING) + ((col_sectors) * GRID_SECTOR_SPACING))) / cols
    y_space = (grid_rect.height - (
                ((rows - row_sectors - 1) * GRID_SPACING) + ((row_sectors) * GRID_SECTOR_SPACING))) / rows

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
def draw_x(rect, color, fill_proportion=1.0):
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


# Round about way of calculating the correct size font for hints.
# Since the font size parameter is a bit confusing
def get_right_size_hint_font(max_size):
    f = pygame.font.SysFont("arial", max_size)
    for i in range(25, 8, -1):
        f = pygame.font.SysFont("arial", i)
        w, h = f.size("000")
        if w <= max_size and h <= max_size:
            break
    return f


def init_hints():
    h_hints_rect = get_horizontal_hints_rect()
    v_hints_rect = get_vertical_hints_rect()
    h_hints = GRID.h_hints_in
    v_hints = GRID.v_hints_in
    max_hints = max(GRID.max_n_v_hints(), GRID.max_n_h_hints())
    # text_space = round(min(25, max(15, min(v_hints_rect.width / max_hints, v_hints_rect.height / max_hints))))
    text_space = round((min([v_hints_rect.width, v_hints_rect.height, h_hints_rect.width, h_hints_rect.height]) / max_hints) - GRID_SPACING)
    font = get_right_size_hint_font(text_space)
    print("".join(["\n" for i in range(3)]))
    print("text_space:", text_space, "max_hints:", max_hints)
    print("h_hints_rect:", h_hints_rect)
    print("v_hints_rect:", v_hints_rect)
    print("v_hints_rect.width / max_hints:", (v_hints_rect.width / max_hints))
    print("v_hints_rect.height / max_hints:", (v_hints_rect.height / max_hints))
    print("h_hints_rect.width / max_hints:", (h_hints_rect.width / max_hints))
    print("h_hints_rect.height / max_hints:", (h_hints_rect.height / max_hints))
    print("len(GRID_SQUARES):", len(GRID_SQUARES), "n_rows:", GRID.n_rows, "n_cols:", GRID.n_cols)
    print("len(h_hints):", len(h_hints), "len(v_hints):", len(v_hints))
    hint_surf_rect = []

    for i, square in enumerate(GRID_SQUARES):
        rect, color, legend_key = square
        if i < GRID.n_cols:
            # top row
            hints = v_hints[i]
            for h in range(len(hints) - 1, -1, -1):
                msg = str(hints[h]).rjust(2, " ")
                text_surf, text_rect = text_objects(msg, font, RED)
                # text_rect.center = ((rect.x + (rect.width / 2)), ((v_hints_rect.bottom - ((len(hints) - h - 1) * text_space)) - (rect.height / 2)))
                text_rect.center = ((rect.x + (rect.width / 2)), (v_hints_rect.bottom - ((len(hints) - h - 1) * text_space) - (rect.height / 2)))
                hint_surf_rect.append((text_surf, text_rect))

        if i % GRID.n_cols == 0:
            # left column
            hints = h_hints[(i // GRID.n_cols)]
            for h in range(len(hints) - 1, -1, -1):
                msg = str(hints[h]).rjust(2, " ")
                text_surf, text_rect = text_objects(msg, font, RED)
                # text_rect.center = (((h_hints_rect.right - ((len(hints) - h - 1) * text_space)) - (rect.width / 2)), (rect.y + (rect.height / 2)))
                text_rect.center = ((h_hints_rect.right - ((len(hints) - h - 1) * text_space) - (rect.width / 2)), (rect.y + (rect.height / 2)))
                hint_surf_rect.append((text_surf, text_rect))
    return hint_surf_rect


# TODO: remove this counter
h = 0


def cycle_all_puzzles():
    global GRID_SQUARES, h
    sleep(4)
    init_grid(get_puzzle_n(h))
    h += 1
    if h == len(get_list_of_puzzles()):
        quit()


# Function marks a grid cell, then updates the GRID_SQUARES list.
def mark_grid(r, c, s=1):
    global GRID_SQUARES
    if GRID.is_uncovered(r, c):
        return
    GRID.set_cell_uncovered(r, c, s)
    GRID_SQUARES = calc_grid()

# Blit the grid's ID in the top left corner of the display.
# Do not blit the name, since it will be a hint to the solution
def draw_grid_name():
    v_hints_rect = get_vertical_hints_rect()
    h_hints_rect = get_horizontal_hints_rect()
    id_rect = pygame.Rect(v_hints_rect.top, h_hints_rect.left, h_hints_rect.width, v_hints_rect.height)
    msg = "Puzzle #" + str(GRID.id_num)
    font = pygame.font.SysFont("arial", 18)
    text_surf, text_rect = text_objects(msg, font)
    text_rect.center = id_rect.center
    DISPLAY.blit(text_surf, text_rect)


def draw_grid():
    global GRID, GRID_SQUARES, DEFAULT_GRID_ROWS, DEFAULT_GRID_COLS, DEFAULT_GRID_ATTRS

    draw_grid_name()

    # Draw grid border
    border_rect = get_grid_border_rect()
    pygame.draw.rect(DISPLAY, SUB_BACKGROUND_COLOR, border_rect)
    # Draw grid
    grid_rect = get_grid_rect()
    # pygame.draw.rect(DISPLAY, WHITE, grid_rect) # blank white square

    # cycle_all_puzzles()

    # GRID.set_cell_uncovered(0, 0, 1)
    # GRID.set_cell_uncovered(0, 1, 1)
    # GRID.set_cell_uncovered(1, 0, 1)
    # GRID.set_cell_uncovered(1, 1, 1)
    for r in range(len(GRID.puzzle_in)):
        for c in range(len(GRID.puzzle_in[r])):
            mark_grid(r, c, LEGEND["correct"])

    # Draw each cell
    for square in GRID_SQUARES:
        rect, color, legend_key = square
        pygame.draw.rect(DISPLAY, color, rect)
        if legend_key == LEGEND["wrong"]:
            draw_x(rect, RED, 0.75)
        elif legend_key == LEGEND["marked"]:
            draw_x(rect, GREY, 0.75)

    pygame.draw.rect(DISPLAY, SUB_BACKGROUND_COLOR, get_horizontal_hints_rect())
    pygame.draw.rect(DISPLAY, SUB_BACKGROUND_COLOR, get_vertical_hints_rect())

    for hint in GRID_HINTS:
        text_surf, text_rect = hint
        DISPLAY.blit(text_surf, text_rect)


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

# Begin the main loop.
def on_start():
    draw_display()
    main_loop()

# Initialize pygame
def init_display():
    global DISPLAY
    pygame.init()
    DISPLAY = pygame.display.set_mode(DEFAULT_WINDOW_SIZE)
    pygame.display.set_caption(TITLE)


if __name__ == "__main__":
    init_display()
    # init_grid(get_puzzle_id(6))  # this puzzle is very large and the hints are displayed too small
    # init_grid(get_puzzle_id(14))  # this puzzle is needs to be solved before drawn
    init_grid(get_puzzle_id(20))  # this puzzle is needs to be solved before drawn, duplicate of puzzle 14, but bigger
    # init_grid(get_puzzle_n(0))  # default testing grid
    on_start()
