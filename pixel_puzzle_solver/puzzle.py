from colors import *

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

LEGEND = {
    "blank": 0,         # default setting before any cell is filled in
    "marked": 2,        # user marked a cell as "blank"
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

        if v_hints_in is None:
            # entire puzzle was given in the puzzle param, need to decipher the hints. These puzzles may be in color
            self.puzzle_in = puzzle
            self.h_hints_in = self.gen_horizontal_hints()
            self.v_hints_in = self.gen_vertical_hints()
        else:
            # puzzle hints were given, need to construct the puzzle itself. These puzzles are default black and white
            self.puzzle_in = None
            self.h_hints_in = puzzle
            self.v_hints_in = v_hints_in

        self.n_rows = len(self.h_hints_in)
        self.n_cols = len(self.v_hints_in)

        # Status list containing information aboput the solving status of the grid.
        self.solving_status = [[LEGEND["blank"] for i in range(self.n_cols)] for j in range(self.n_rows)]

    def __repr__(self):
        return "<Puzzle object: n: " + str(self.name) + " (" + str(self.n_rows) + "x" + str(self.n_cols) + ")>"

    def set_cell_marked(self, r, c):
        self.solving_status[r][c] = LEGEND["marked"]

    def set_cell_uncovered(self, r, c, legend_color):
        # TODO remove the none checks on puzzle_in, because it should be solved at some point
        if self.puzzle_in is None:
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
