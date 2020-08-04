from colors import *
import numpy as np

# sample smiley grid, used as the go to default puzzle
sample_smiley = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

# This legend contains cell status information.
LEGEND = {
    "blank": 0,         # default setting before any cell is filled in
    "marked": -2,       # user marked a cell as "blank"
    "correct": 1,       # user marked with a pixel, and it is correct
    "wrong": -1         # user marked with a pixel, but it is incorrect
}


# Class to represent a puzzle. Contains status information including the color of each square, title, n_rows, and n_cols
class Puzzle:

    def __init__(self, name, id_num, legend, puzzle, v_hints_in=None):
        if not verify(puzzle, v_hints_in):
            print('Error Invalid puzzle dimensions')
            puzzle = pad_puzzle(puzzle)

        self.name = name
        self.id_num = id_num
        self.legend = legend

        # TODO current hint calculations only account for 1 color puzzles.
        # Need to convert to a dict that will record hint color information as well
        if v_hints_in is None:
            # entire puzzle was given in the puzzle param, need to decipher the hints. These puzzles may be in color
            self.puzzle_in = puzzle
            self.h_hints_in = self.gen_horizontal_hints()
            self.v_hints_in = self.gen_vertical_hints()
        else:
            # puzzle hints were given, need to construct the puzzle itself. These puzzles are default black and white
            self.h_hints_in = puzzle
            self.v_hints_in = v_hints_in
            self.puzzle_in = self.solve_b_w_puzzle()

        self.n_rows = len(self.h_hints_in)
        self.n_cols = len(self.v_hints_in)

        # Status list containing information aboput the solving status of the grid.
        self.solving_status = [[LEGEND["blank"] for i in range(self.n_cols)] for j in range(self.n_rows)]

    def __repr__(self):
        return "<Puzzle object: n: " + str(self.name) + " (" + str(self.n_rows) + "x" + str(self.n_cols) + ")>"

    # Loops a list of hints and attempts to place even a portion of the colored cell on the grid.
    def place_hints(self, solved_puzzle, hints_in, space):
        for r, hints in enumerate(hints_in):
            print("\n\t\trow", r)
            sum_hints = sum(hints)
            buffer = space - sum_hints - (len(hints) - 1)  # acts as +/- for colored sections
            remaining_space = space
            for h, hint in enumerate(hints):
                rest_hints = hints[:h] + hints[h + 1:]
                space_confirmed = hint - buffer
                s = space - remaining_space + buffer
                print("\th:", h, ",hint:", hint, ",rest:", rest_hints, ",r:", remaining_space, ",l", buffer, ",c:", space_confirmed, ",s:", s, ",st:", s + space_confirmed)
                # Can fill in at least one cell
                if 0 < space_confirmed <= hint:
                    for i in range(s, s + space_confirmed):
                        print("placing at [", r, "][", i, "]")
                        solved_puzzle[r][i] = 1
                remaining_space -= (hint + 1)

    def fill_border_hints(self, solved_puzzle, hints_in):
        for r, row_hints in enumerate(zip(solved_puzzle, hints_in)):
            row, hints = row_hints
            # Check left to right
            if row[0] == 1:
                print("row", r, "is marked in the first column")
                hint = hints[0]
                for i in range(len(row)):
                    if i < hint:
                        solved_puzzle[r][i] = 1
                    else:
                        break
            # Check right to left
            if row[-1] == 1:
                print("row", r, "is marked in the last column")
                hint = hints[-1]
                for i in range(len(row) - 1, -1, -1):
                    if i > len(row) - 1 - hint:
                        solved_puzzle[r][i] = 1
                    else:
                        break

    # Solves black and white puzzles only.
    def solve_b_w_puzzle(self):
        rows = len(self.h_hints_in)
        cols = len(self.v_hints_in)
        solved_puzzle = [[LEGEND["blank"] for c in range(cols)] for r in range(rows)]

        # Make a first pass of the puzzle and attempt to place any hints that are occupy a row or column
        # with a smell enough buffer space.

        # Loop horizontal hints
        self.place_hints(solved_puzzle, self.h_hints_in, cols)
        solved_puzzle = np.transpose(solved_puzzle)
        # Loop vertical hints
        self.place_hints(solved_puzzle, self.v_hints_in, rows)
        solved_puzzle = np.transpose(solved_puzzle)

        # Iteratively check that that hints placed on the border fill in their entire space.
        # Once the border hints are checked, cut the board and perform another check.
        
        # Check horizontal hints
        self.fill_border_hints(solved_puzzle, self.h_hints_in)
        solved_puzzle = np.transpose(solved_puzzle)
        # Check vertical hints
        self.fill_border_hints(solved_puzzle, self.v_hints_in)
        solved_puzzle = np.transpose(solved_puzzle)

        print("SOLVED PUZZLE\n\n", solved_puzzle)
        return solved_puzzle

    # def calc_hint_attrs(self):
    #     pass

    # What is the max number of hints in the vertical hints list
    def max_n_v_hints(self):
        return max([len(l) for l in self.v_hints_in])

    # What is the max number of hints in the horizontal hints list
    def max_n_h_hints(self):
        return max([len(l) for l in self.h_hints_in])

    def set_cell_marked(self, r, c):
        self.solving_status[r][c] = LEGEND["marked"]

    def set_cell_uncovered(self, r, c, legend_color):
        # TODO remove the none checks on puzzle_in, because it should be solved at some point
        if self.puzzle_in is None:
            print("GRID.puzzle_in is None")
            return
        if self.puzzle_in[r][c] == legend_color:
            self.solving_status[r][c] = LEGEND["correct"]
        else:
            self.solving_status[r][c] = LEGEND["wrong"]

    def get_legend_key(self, r, c):
        return self.solving_status[r][c]

    # Is the grid cell marked in any way?
    def is_uncovered(self, r, c):
        return self.solving_status[r][c] != LEGEND["blank"]

    # Is the grid cell marked?
    def is_marked(self, r, c):
        return self.solving_status[r][c] == LEGEND["marked"]

    # Is the grid_cell marked, but incorrectly?
    def is_wrong(self, r, c):
        return self.solving_status[r][c] == LEGEND["wrong"]

    def gen_horizontal_hints(self):
        board = self.puzzle_in
        rows = len(board)
        cols = len(board[0])
        res = [[] for i in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if (board[r][c] == 1 and c == 0) or (board[r][c] == 1 and board[r][c - 1] == 0):
                    count = 1
                    temp = c
                    while temp < cols - 1 and board[r][temp + 1] == 1:
                        count += 1
                        temp += 1
                    res[r].append(count)
        for r in range(rows):
            if len(res[r]) == 0:
                res[r] = [0]
        # print('h_hints', res)
        return res

    def gen_vertical_hints(self):
        board = self.puzzle_in
        rows = len(board)
        cols = len(board[0])
        res = [[] for i in range(cols)]
        for r in range(rows):
            for c in range(cols):
                if (board[r][c] == 1 and r == 0) or (board[r][c] == 1 and board[r - 1][c] == 0):
                    temp = r
                    count = 1
                    while (r < rows - 1) and (board[r + 1][c] == 1):
                        count += 1
                        r += 1
                    r = temp
                    res[c].append(count)
        for c in range(cols):
            if len(res[c]) == 0:
                res[c] = [0]
        # print('v_hints', res)
        return res

    # Return the number of rows and columns as a tuple.
    def get_rows_cols(self):
        return self.n_rows, self.n_cols

    # Return the color associated with the cell.
    def get_square_color(self, r, c):
        if self.puzzle_in is None:
            return WHITE
        return self.legend[self.puzzle_in[r][c]]


def verify(puzzle, v_hints_in):
    if (type(puzzle) is not list or len(puzzle) == 0 or type(puzzle[0] != list)) and v_hints_in is None:
        print('Error not a puzzle upper')
        return False
    sub_list_lens = [len(puzzle[x]) for x in range(len(puzzle))]
    # print('sub_lst',sub_list_lens)
    lst = list(set(sub_list_lens))
    # print('lst',lst)
    if ((len(lst) > 1) or (lst[0] < 3) or (len(puzzle) < 3)) and v_hints_in is None:
        print('Error not a puzzle lower')
        return False
    return True


# Create a full square of hints if an odd shaped or not full list is given to initialize a puzzle.
# Pads all remaining spaces using zeros.
def pad_puzzle(puzzle):
    if type(puzzle) == list:
        rows = len(puzzle)
        # row_len = len(rows)
        if rows > 2:
            cols = max([len(puzzle[x]) for x in range(rows)])
            new_puzzle = [[0 for y in range(cols)] for x in range(rows)]
            # print('new_puzzle', new_puzzle)
            i = rows - 1
            j = cols - 1
            while i >= 0:
                row_len = len(puzzle[i])
                while j >= 0:
                    # print('i:', i, ', j:', j, ', row_len:', row_len)
                    if j < row_len:
                        new_puzzle[i][j] = puzzle[i][j]
                        # using { if p < row_len: new_puzzle[i][j] = puzzle[i][p] }
                        # instead of the above will horizontally flip the puzzle
                    j -= 1
                i -= 1
                j = cols - 1
            # print("new_puzzle", new_puzzle)
        else:
            new_puzzle = sample_smiley
    else:
        new_puzzle = sample_smiley
    return new_puzzle
