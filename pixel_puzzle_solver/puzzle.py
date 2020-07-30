# Class to represent a puzzle. Contains status information including the color of each square, title, n_rows, and n_cols


class Puzzle:

    def __init__(self, name, id_num, legend, puzzle, v_hints_in=None):
        self.name = name
        self.id_num = id_num
        self.legend = legend

        if v_hints_in is None:
            # entire puzzle was given in the puzzle param, need to decipher the hints. These puzzles may be in color
            self.puzzle_in = puzzle
            self.h_hints_in = None
            self.v_hints_in = None
        else:
            # puzzle hints were given, need to construct the puzzle itself. These puzzles are default black and white
            self.puzzle_in = None
            self.h_hints_in = puzzle
            self.v_hints_in = v_hints_in

        self.n_rows = len(self.h_hints_in)
        self.n_cols = len(self.v_hints_in)

    def get_rows_cols(self):
        return self.n_rows, self.n_cols