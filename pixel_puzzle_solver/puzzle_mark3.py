# Trying to solve the puzzle using only the cut index repeat method, no backtracking

import itertools
import time

from colors import *
import numpy as np
from sys import maxsize

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
    "blank": 0,  # default setting before any cell is filled in
    "marked": -2,  # user marked a cell as "blank"
    "correct": 1,  # user marked with a pixel, and it is correct
    "wrong": -1  # user marked with a pixel, but it is incorrect
}


# Class to represent a puzzle. Contains status information including the color of each square, title, n_rows, and n_cols
class Puzzle:

    def __init__(self, name, id_num, legend, puzzle, v_hints_in=None):
        if not verify(puzzle, v_hints_in):
            print('Error Invalid puzzle dimensions')
            puzzle = pad_puzzle(puzzle)

        # True if only the hints were given at time of puzzle creation, False if the puzzle was given.
        need_to_solve = False

        self.name = name
        self.id_num = id_num
        self.legend = legend
        # self.legend.update({-2: LEGEND["marked"]})

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
            need_to_solve = True

        self.n_rows = len(self.h_hints_in)
        self.n_cols = len(self.v_hints_in)

        # Status list containing information aboput the solving status of the grid.
        self.solving_status = [[LEGEND["blank"] for i in range(self.n_cols)] for j in range(self.n_rows)]

        start_time = time.time()
        if need_to_solve:
            self.puzzle_in = self.solve_b_w_puzzle()
        end_time = time.time()
        how_long = end_time - start_time
        mins, sec = divmod(how_long, 60)
        print("solved in", mins, "m", sec, "sec")
        print("Puzzle -", self.name, "was successfully created!")

    def __repr__(self):
        return "<Puzzle object: n: " + str(self.name) + " (" + str(self.n_rows) + "x" + str(self.n_cols) + ")>"

    # Loops a list of hints and attempts to place even a portion of the colored cell on the grid.
    def place_hints(self, solved_puzzle, hints_in, space):
        print("\n\t\tPLACE HINTS")
        for r, hints in enumerate(hints_in):
            if hints:
                print("\n\t\trow", r)
                sum_hints = sum(hints)
                buffer = space - sum_hints - (len(hints) - 1)  # acts as +/- for colored sections
                remaining_space = space
                for h, hint in enumerate(hints):
                    rest_hints = hints[:h] + hints[h + 1:]
                    space_confirmed = hint - buffer
                    s = space - remaining_space + buffer
                    # print("\th:", h, "hint:", hint, "space", space, "rest:", rest_hints, "rs:", remaining_space, "b",
                    #       buffer, "sc:",
                    #       space_confirmed, "start:", s, "stop:", s + space_confirmed)
                    # Can fill in at least one cell
                    if 0 < space_confirmed <= hint:
                        for i in range(s, s + space_confirmed):
                            print("placing at [", r, "][", i, "]")
                            solved_puzzle[r][i] = 1
                    # if space_confirmed == hint:
                    #     print("\thint:", hint, "s:", s)
                    #     if 0 < s:
                    #         print("placing mark before at [", r, "][", s - 1, "]")
                    #         self.set_cell_marked(r, s - 1)
                    #         solved_puzzle[r][s - 1] = -2
                    #     if s + space_confirmed < len(solved_puzzle[r]):
                    #         print("placing mark after at [", r, "][", s + space_confirmed + 1, "]")
                    #         self.set_cell_marked(r, s + space_confirmed + 1)
                    #         solved_puzzle[r][s + space_confirmed + 1] = -2

                    remaining_space -= (hint + 1)
        print("solved puzzle:\n", solved_puzzle)

    def fill_border_hints(self, solved_puzzle, hints_in, offsets):
        print("\n\t\tFILL BORDER HINTS")
        col_offset, row_offset = offsets
        print("col_offset:", col_offset, "row_offset:", row_offset)
        for r, row_hints in enumerate(zip(solved_puzzle, hints_in)):
            row, hints = row_hints
            if hints:
                # Check left to right
                if row[0] == 1:
                    # print("row", r, "is marked in the first column")
                    hint = hints[0]
                    for i in range(len(row)):
                        if i < hint:
                            solved_puzzle[r][i] = 1
                            print("placing at [", r, "][", i, "]")
                        elif i == hint:
                            # print("border at r:", r, "i", i)
                            self.set_cell_marked(r + row_offset, i + col_offset)
                            solved_puzzle[r][i] = -2
                        else:
                            break
                # Check right to left
                if row[-1] == 1:
                    # print("row", r, "is marked in the last column")
                    hint = hints[-1]
                    for i in range(len(row) - 1, -1, -1):
                        if i > len(row) - 1 - hint:
                            solved_puzzle[r][i] = 1
                            print("placing at [", r, "][", i, "]")
                        elif i == len(row) - 1 - hint:
                            # print("border at r:", r + row_offset, "i:", i + col_offset)
                            self.set_cell_marked(r + row_offset, i + col_offset)
                            solved_puzzle[r][i] = -2
                        else:
                            break
        print_puzzle(solved_puzzle)

    # Place markers at all other positions in a filled row. A filled row is comprised of a puzzle
    # row that is marked for as many spaces as the sum of all the row hints.
    def fill_complete_rows(self, solved_puzzle, completed_rows, is_transposed, offsets):
        print("\n\t\tFILL_COMPLETE_ROWS")
        col_offset, row_offset = offsets
        print("col_offset:", col_offset, "row_offset:", row_offset)
        for r in completed_rows:
            row = solved_puzzle[r]
            for c, val in enumerate(row):
                if val == 0:
                    # if is_transposed:
                    #     print("border at r:", c + col_offset, "i:", r + row_offset)
                    # else:
                    #     print("border at r:", r + row_offset, "i:", c + col_offset)
                    self.set_cell_marked(c + col_offset, r + row_offset) if is_transposed else self.set_cell_marked(
                        r + row_offset, c + col_offset)
                    solved_puzzle[r][c] = -2

    def fill_spaces(self, solved_puzzle, hints_in, is_transposed, offsets):
        print("\n\t\tFILL_SPACES")
        col_offset, row_offset = offsets
        print("col_offset:", col_offset, "row_offset:", row_offset)
        remaining_spaces = self.remaining_spaces(solved_puzzle)
        # print("remaining spaces:")
        # print_puzzle(remaining_spaces)
        for row, spaces in enumerate(remaining_spaces):
            # print("\nrow", row)
            size = len(solved_puzzle[row])
            free_spaces = sum([y - x for x, y in spaces])
            covered_spaces = size - free_spaces
            spacer = len(hints_in[row]) - 1
            hint_spaces = sum(hints_in[row]) + spacer
            num_spacers_left = ((size - hint_spaces) + spacer) - np_count(solved_puzzle[row], -2)
            spaces_left = size - (covered_spaces + num_spacers_left)  # (free_spaces + covered_spaces) - size
            # print("\thint:", hints_in[row], "in:", solved_puzzle[row])
            # print("\tsize:", size, "free_spaces:", free_spaces, "covered_spaces:", covered_spaces, "hint_spaces:",
            #       hint_spaces, "num_spacers_left:", num_spacers_left, "spacer:", spacer, "spaces_left:", spaces_left)
            if spaces_left == free_spaces:
                for col in range(len(solved_puzzle[row])):
                    if solved_puzzle[row][col] == 0:
                        solved_puzzle[row][col] = 1
            elif spaces_left > 0:
                min_hint = min(hints_in[row])
                for i, space in enumerate(spaces):
                    # print("r:", row, "spaces:", spaces, "i:", i, "space:", space)
                    start, stop = space
                    cl_a = start == 0
                    cl_b = True if cl_a else solved_puzzle[row][start - 1] == -2
                    cl_c = stop == len(solved_puzzle[row])
                    cl_d = True if cl_c else solved_puzzle[row][stop] == -2
                    closed_in = (cl_a or cl_b) and (cl_c or cl_d)
                    # print("\t\tclosed_in:", closed_in)
                    # print("\t\tstart == 0", cl_a, "solved_puzzle[row][start] == -2:", cl_b, "a or b:", (cl_a or cl_b))
                    # print("\t\tstop == len(solved_puzzle[row]):", cl_c, "solved_puzzle[row][stop] == -2:", cl_d, "c or d:", (cl_c or cl_d))
                    if (stop - start) < min_hint and closed_in:
                        for j in range(*space):
                            solved_puzzle[row][j] = -2
                            self.set_cell_marked(j + col_offset,
                                                 row + row_offset) if is_transposed else self.set_cell_marked(
                                row + row_offset, j + col_offset)

    def shrink_hints(self, chunk, hints_in, top_left):
        idx = 0 if top_left else -1
        # print("chunk:")
        # print_puzzle(chunk)
        before = deep_copy(hints_in)
        # print("hints_in:")
        # print_puzzle(hints_in)
        # print("\nchunk:", chunk, "hints_in:", hints_in)
        for r, row in enumerate(chunk):
            # print("\tr: " + str(r) + " row: " + str(row))
            skipped = []
            for c, val in enumerate(row):
                if val == 1:
                    # msg = "\t\tc: " + str(c) + " idx: " + str(idx) + " val: " + str(val) + " hints_in[c]: " + str(
                    #     hints_in[c])
                    hints_in[c][idx] -= 1
                    if hints_in[c][idx] == 0:
                        hints_in[c].remove(0)
                    if not hints_in[c]:
                        hints_in[c] = [0]
                # msg += " after: " + str(hints_in[c])
                # print(msg)
                else:
                    skipped.append(c)
        # print("\t\t\tskipped:", skipped)
        # print("shrunk to")
        # print_puzzle(hints_in)

    # msg = "no change" if before == hints_in else "changed"
    # print(msg)

    # Cut a given puzzle by the given cut indices. Cut indices are excluded in resulting puzzle.
    def cut_puzzle(self, solved_puzzle, h_hints_in, v_hints_in, top_cut, bottom_cut, left_cut, right_cut):
        # print("cut solved_puzzle:", solved_puzzle)
        bottom_cut = top_cut + 1 if top_cut == bottom_cut else bottom_cut
        right_cut = left_cut + 1 if left_cut == right_cut else right_cut
        print("Cut puzzle: top[", top_cut, "], bottom[", bottom_cut, "], left[", left_cut, "], right[", right_cut, "]")
        cut_visual(solved_puzzle.tolist(), top_cut, bottom_cut, left_cut, right_cut)
        # print("Cut puzzle: top[",top_cut,"], bottom[",bottom_cut,"], left[",left_cut,"], right[",right_cut,"]")
        # Copy the parameter lists to avoid modification
        solved_puzzle = deep_copy(solved_puzzle)
        h_hints_in = deep_copy(h_hints_in)
        v_hints_in = deep_copy(v_hints_in)

        top_chunk = solved_puzzle[:top_cut + 1]
        bottom_chunk = solved_puzzle[bottom_cut:]
        left_chunk = [row[:left_cut + 1] for row in solved_puzzle]
        right_chunk = [row[right_cut:] for row in solved_puzzle]

        new_puzzle = [row[left_cut + 1: right_cut].copy() for row in solved_puzzle[top_cut + 1: bottom_cut]]
        # print("\n\ttop_chunk:\n", top_chunk)
        # print("\n\tbottom_chunk:\n", bottom_chunk)
        # print("\n\tleft_chunk:\n", left_chunk)
        # print("\n\tright_chunk:\n", right_chunk)

        self.shrink_hints(top_chunk, v_hints_in, True)
        self.shrink_hints(bottom_chunk, v_hints_in, False)

        left_chunk = np.transpose(left_chunk)
        right_chunk = np.transpose(right_chunk)
        h_hints_in = np.transpose(
            np.array(h_hints_in, dtype=object))  # non-uniform size lists as ndarrays is deprecated

        self.shrink_hints(left_chunk, h_hints_in, True)
        self.shrink_hints(right_chunk, h_hints_in, False)

        h_hints_in = h_hints_in[top_cut + 1: bottom_cut]
        v_hints_in = v_hints_in[left_cut + 1: right_cut]

        return new_puzzle, h_hints_in, v_hints_in, (top_chunk, bottom_chunk, left_chunk, right_chunk)

    # print("cut solved_puzzle:", solved_puzzle)
    # print("Cut puzzle: top[", top_cut, "], bottom[", bottom_cut, "], left[", left_cut, "], right[", right_cut, "]")
    # # Copy the parameter lists to avoid modification
    # solved_puzzle = deep_copy(solved_puzzle)
    # h_hints_in = deep_copy(h_hints_in)
    # v_hints_in = deep_copy(v_hints_in)
    #
    # top_chunk = solved_puzzle[:top_cut + 1]
    # bottom_chunk = solved_puzzle[bottom_cut:]
    # left_chunk = [row[:left_cut + 1] for row in solved_puzzle]
    # right_chunk = [row[right_cut:] for row in solved_puzzle]
    # print("\ttop_chunk (", len(top_chunk), "), (", len(top_chunk[0]), "):\n", top_chunk)
    # print("\tbottom_chunk (", len(bottom_chunk), "), (", len(bottom_chunk[0]), "):\n", bottom_chunk)
    # print("\tleft_chunk (", len(left_chunk), "), (", len(left_chunk[0]), "):\n", left_chunk)
    # print("\tright_chunk (", len(right_chunk), "), (", len(right_chunk[0]), "):\n", right_chunk)
    #
    # self.shrink_hints(top_chunk, v_hints_in, True)
    # self.shrink_hints(bottom_chunk, v_hints_in, False)
    #
    # left_chunk = np.transpose(left_chunk)
    # right_chunk = np.transpose(right_chunk)
    # h_hints_in = np.transpose(
    #     np.array(h_hints_in, dtype=object))  # non-uniform size lists as ndarrays is deprecated
    #
    # self.shrink_hints(left_chunk, h_hints_in, True)
    # self.shrink_hints(right_chunk, h_hints_in, False)
    # h_hints_in = h_hints_in.tolist()
    #
    # h_hints_in = h_hints_in[top_cut + 1: bottom_cut]
    # v_hints_in = v_hints_in[left_cut + 1: right_cut]
    #
    # left_chunk = np.transpose(left_chunk).tolist()
    # right_chunk = np.transpose(right_chunk).tolist()
    # result = [row[left_cut + 1: right_cut].copy() for row in
    #           solved_puzzle[top_cut + 1: bottom_cut]]
    # print("cut result:", result)
    # return result, h_hints_in, v_hints_in, top_chunk, bottom_chunk, left_chunk, right_chunk

    # Return a list of rows in the puzzle that are complete.
    def completed_rows(self, solved_puzzle, hints_in):
        complete_rows = []
        for r, hints in enumerate(hints_in):
            hint_sum = sum(hints)
            placed_sum = np_count(solved_puzzle[r], 1)
            # unique, counts = np.unique(solved_puzzle[r], return_counts=True)
            # values = dict(zip(unique, counts))
            # placed_sum = 0 if 1 not in values else values[1]
            if hint_sum == placed_sum:
                complete_rows.append(r)
        return complete_rows

    def solve_b_w_recursive(self, solved_puzzle, h_hints, v_hints, chunks_list=None):
        print("\n\t\tSOLVE_B_W_RECURSIVE")
        print("chunks_list:", chunks_list)
        sum_hints = sum([sum(hints) for hints in v_hints])
        sum_placed = [row.count(1) for row in solved_puzzle].count(1)
        if sum_hints == sum_placed:
            if chunks_list is not None:
                chunks_list.reverse()
                for chunk in chunks_list:
                    solved_puzzle = self.pad_puzzle(solved_puzzle, chunk)
            return solved_puzzle
        # rows = len(h_hints)
        # cols = len(v_hints)
        solved_status = [row.copy() for row in solved_puzzle]

        complete_horizontal_rows = self.completed_rows(solved_status, h_hints)
        solved_status = np.transpose(solved_status)
        complete_vertical_rows = self.completed_rows(solved_status, v_hints)
        solved_status = np.transpose(solved_status)

        if not complete_horizontal_rows or not complete_vertical_rows:
            print("No rows have been completed")
            if chunks_list is not None:
                chunks_list.reverse()
                for chunk in chunks_list:
                    solved_puzzle = self.pad_puzzle(solved_puzzle, chunk)
            return solved_puzzle
        top_cut, bottom_cut = outside_indices(complete_horizontal_rows, len(h_hints))
        left_cut, right_cut = outside_indices(complete_vertical_rows, len(v_hints))

        # Mark solved_status with known blank spaces
        # complete_horizontal_rows = self.completed_rows(solved_status, h_hints)
        # for r in complete_horizontal_rows:
        #     for c in range(cols):
        #         if solved_status[r][c] != 1:
        #             solved_status[r][c] = -1

        # solved_status = np.transpose(solved_status)
        # complete_vertical_rows = self.completed_rows(solved_status, h_hints)
        # for r in complete_vertical_rows:
        #     for c in range(cols):
        #         if solved_status[r][c] != 1:
        #             solved_status[r][c] = -1
        # solved_status = np.transpose(solved_status)
        # top_cut, bottom_cut = outside_indices(complete_horizontal_rows)
        # left_cut, right_cut = outside_indices(complete_vertical_rows)

        print("complete_horizontal_rows:", complete_horizontal_rows)
        print("complete_vertical_rows:", complete_vertical_rows)
        print("top_cut:", top_cut, "bottom_cut:", bottom_cut, "left_cut:", left_cut, "right_cut:", right_cut)
        new_puzzle, new_h_hints, new_v_hints, *chunks = self.cut_puzzle(solved_puzzle, h_hints, v_hints,
                                                                        *outside_indices(complete_horizontal_rows,
                                                                                         len(h_hints)),
                                                                        *outside_indices(complete_vertical_rows,
                                                                                         len(v_hints)))
        # print("\n\tnew_puzzle: r:(", len(new_puzzle), "), c:(", len(new_puzzle[0]), ")\n", new_puzzle)
        # print("\n\tnew_h_hints: r:(", len(new_h_hints), "), c:(", len(new_h_hints[0]), ")\n", new_h_hints)
        # print("\n\tnew_v_hints: r:(", len(new_v_hints), "), c:(", len(new_v_hints[0]), ")\n", new_v_hints)
        # Loop horizontal hints
        self.place_hints(new_puzzle, new_h_hints, len(new_v_hints))
        new_puzzle = np.transpose(new_puzzle).tolist()
        # Loop vertical hints
        self.place_hints(new_puzzle, new_v_hints, len(new_h_hints))
        new_puzzle = np.transpose(new_puzzle).tolist()

        # Check horizontal hints
        self.fill_border_hints(new_puzzle, self.h_hints_in)
        new_puzzle = np.transpose(new_puzzle).tolist()
        self.solving_status = np.transpose(self.solving_status).tolist()
        # Check vertical hints
        self.fill_border_hints(new_puzzle, self.v_hints_in)
        new_puzzle = np.transpose(new_puzzle).tolist()
        self.solving_status = np.transpose(self.solving_status).tolist()

        # for r, hints in enumerate(h_hints):
        #     hint_sum = sum(hints)
        #     unique, counts = np.unique(solved_status[r], return_counts=True)
        #     values = dict(zip(unique, counts))
        #     print(values)
        #     placed_sum = 0 if 1 not in values else values[1]
        #     print("r:", r, "hint_sum:", hint_sum, "placed_sum:", placed_sum, "hints:", hints, "row", solved_status[r])
        #     # Row is completed
        #     if hint_sum == placed_sum:
        #         for c in range(cols):
        #             if solved_status[r][c] != 1:
        #                 print("\tFilling c:", c)
        #                 solved_status[r][c] = -1
        #     else:
        #         if solved_status[r][0] == 1:
        #             solved_status[r][hints[0]] = -1
        #             print("\thints[0]:", hints[0])
        #         if solved_status[r][-1] == 1:
        #             solved_status[r][(cols - 1) - hints[-1]] = -1
        #             print("\t-1 * (cols - hints[-1])", (cols - 1) - hints[-1])

        # new_puzzle = self.pad_puzzle(new_puzzle, chunks)
        # print("\nsolve_b_w_recursive:\n")
        print("NEW PUZZLE")
        print_puzzle(new_puzzle)
        # print("SOLVED PUZZLE")
        # print_puzzle(solved_puzzle)

        chunks_list = [chunks] if chunks_list is None else chunks_list + [chunks]
        return self.solve_b_w_recursive(new_puzzle, new_h_hints, new_v_hints, chunks_list)

    # Solves black and white puzzles only.
    def solve_b_w_puzzle(self):
        print("\n\t\tSOLVE_B_W_PUZZLE")
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

        # solved_puzzle = self.solve_b_w_recursive(solved_puzzle.tolist(), self.h_hints_in, self.v_hints_in)

        # Reference copy to break out of the iteration
        prev = deep_copy(solved_puzzle.tolist())
        once = True  # To ensure that the loop is executed at least once

        cut_chunks = []
        cut_offsets = (0, 0)
        h_hints = self.h_hints_in
        v_hints = self.v_hints_in
        iter = 0
        # Iteratively check that that hints placed on the border fill in their entire space.
        while solved_puzzle.any() and once or prev != solved_puzzle.tolist():
            print("\n\n\tITERATION", iter,"\t")
            iter += 1
            if iter == 8:
                break

            # Update the reference copy for next iteration
            prev = deep_copy(solved_puzzle.tolist())

            # Check horizontal hints
            self.fill_border_hints(solved_puzzle, h_hints, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)
            self.solving_status = np.transpose(self.solving_status).tolist()
            # Check vertical hints
            self.fill_border_hints(solved_puzzle, v_hints, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)
            self.solving_status = np.transpose(self.solving_status).tolist()

            # Fill in completed rows and cols
            completed_rows = self.completed_rows(solved_puzzle, h_hints)
            self.fill_complete_rows(solved_puzzle, completed_rows, False, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)
            completed_rows = self.completed_rows(solved_puzzle, v_hints)
            self.fill_complete_rows(solved_puzzle, completed_rows, True, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)

            # Check spaces between colored sections and fill with marks or color in
            self.fill_spaces(solved_puzzle, h_hints, False, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)
            self.fill_spaces(solved_puzzle, v_hints, True, cut_offsets)
            solved_puzzle = np.transpose(solved_puzzle)
            once = False  # Only needs to be checked once, reference copy is used to break iterations

            # Perform a round of cutting if the puzzle did not change in the last iteration of
            # fill_border_hints, fill_complete_rows, and fill_spaces.
            if prev == solved_puzzle.tolist():
                completed_rows = self.completed_rows(solved_puzzle, h_hints)
                print("completed_rows", completed_rows)
                top_cut, bottom_cut = outside_indices(completed_rows, len(v_hints))
                solved_puzzle = np.transpose(solved_puzzle)
                completed_rows = self.completed_rows(solved_puzzle, v_hints)
                print("completed_cols", completed_rows)
                left_cut, right_cut = outside_indices(completed_rows, len(h_hints))
                solved_puzzle = np.transpose(solved_puzzle)
                print("top_cut", top_cut, "bottom_cut:", bottom_cut, "diff:", (bottom_cut - top_cut))
                print("left_cut", left_cut, "right_cut:", right_cut, "diff:", (right_cut - left_cut))
                if (right_cut - left_cut) == 1 or (bottom_cut - top_cut) == 1:
                    print("DIFF IS 1")
                    break
                if None in [top_cut, bottom_cut, left_cut, right_cut]:
                    print("Unsafe cut, not enough completed rows")
                    # begin back-tracking at this point. The puzzle and it's hints are cuurently cut as small as
                    # can be done safely.
                    solved_puzzle = self.bt_solve(solved_puzzle, h_hints, v_hints)
                    break
                solved_puzzle, h_hints, v_hints, *chunks = self.cut_puzzle(solved_puzzle, h_hints, v_hints, top_cut,
                                                                           bottom_cut, left_cut, right_cut)
                cut_chunks.append(chunks)
                col_offset, row_offset = cut_offsets
                col_offset += left_cut + 1
                row_offset += top_cut + 1
                cut_offsets = (col_offset, row_offset)

                self.place_hints(solved_puzzle, h_hints, len(v_hints))
                solved_puzzle = np.transpose(solved_puzzle)
                # Loop vertical hints
                self.place_hints(solved_puzzle, v_hints, len(h_hints))
                solved_puzzle = np.transpose(solved_puzzle)

            if isinstance(solved_puzzle, list):
                solved_puzzle = np.array(solved_puzzle)

        if cut_chunks:
            cut_chunks.reverse()
            for chunk in cut_chunks:
                solved_puzzle = self.pad_puzzle(solved_puzzle, chunk)
        # completed_rows = self.completed_rows(solved_puzzle, self.h_hints_in)
        # top_cut, bottom_cut = outside_indices(completed_rows, len(self.v_hints_in))
        # solved_puzzle = np.transpose(solved_puzzle)
        # completed_rows = self.completed_rows(solved_puzzle, self.v_hints_in)
        # left_cut, right_cut = outside_indices(completed_rows, len(self.v_hints_in))
        # solved_puzzle = np.transpose(solved_puzzle)
        # print("completed_rows", completed_rows)
        # print("top_cut", top_cut, "bottom_cut:", bottom_cut)
        # print("left_cut", left_cut, "right_cut:", right_cut)
        # smaller_puzzle = self.cut_puzzle(solved_puzzle, self.h_hints_in, self.v_hints_in, top_cut, bottom_cut,
        #                                  left_cut, right_cut)
        # print("Smaller puzzle, h_hints:", smaller_puzzle[1], "v_hints:", smaller_puzzle[2])
        # print_puzzle(smaller_puzzle[0])
        print("\n\n\tSOLVED_PUZZLE")
        print_puzzle(solved_puzzle)
        return solved_puzzle

    def bt_solve(self, puzzle, h_hints, v_hints):
        puzzle, h_hints, v_hints = list(map(ensure_list, [puzzle, h_hints, v_hints]))
        print("h_hints:", h_hints)
        print("v_hints:", v_hints)
        print("Backtracking on puzzle:")
        print_puzzle(puzzle)
        total_size = len(h_hints) * len(v_hints)
        total_colored = sum([np_count(row, 1) for row in puzzle])
        desired_colored = sum([sum(hint_row) for hint_row in h_hints])
        total_to_be_colored = int(desired_colored - total_colored)
        unknown_indices = [(x // len(v_hints), x % len(v_hints)) for x in range(total_size) if
                           puzzle[x // len(v_hints)][x % len(v_hints)] == 0]
        print("total left to color:", total_to_be_colored)
        print("unknown indices:")
        print(unknown_indices)
        # permutations_list = permutations(unknown_indices, total_to_be_colored)
        # print("To try:")
        # for perm in permutations_list:
        #     print(perm)

        unknown_rows = []
        to_try = 1
        perm_ranges = []
        perms = {}
        for r, row in enumerate(puzzle):
            # print("\trow:", r)
            desired_row_count = sum(h_hints[r])
            curr_row_count = np_count(row, 1)
            row_count_left = int(desired_row_count - curr_row_count)
            print("\trow:", r, "row_count_left:", row_count_left)
            if row_count_left == 0:
                continue
            else:
                unknown_rows.append(r)
            row_permutations = permutations([indices for indices in unknown_indices if indices[0] == r], row_count_left)
            to_try *= len(row_permutations)
            perm_ranges.append(range(len(row_permutations)))
            perms[r] = row_permutations

            # for perm in row_permutations:
            #     print(perm)
        print("number to try =", to_try)
        print("perms =", perm_ranges)

        # Stores list of indices for perms
        perm_combinations = combinations(perm_ranges)
        p = 0
        cpy = deep_copy(puzzle)
        # Loop until a solution is encountered
        while not check_puzzle_is_solved(cpy, h_hints, v_hints):
            cpy = deep_copy(puzzle)
            permutation = perm_combinations[p]
            # print("p:", p, "permutation:", permutation)
            for i, j in enumerate(permutation):
                r = unknown_rows[i]
                indices = perms[r][j]
                # print("\tr", r, "Indices", indices)
                for row, col in indices:
                    cpy[row][col] = 1
                # print("perms:", perms[i])
                # print("i:", i, "row:", row, "col:", col)
            # print_puzzle(cpy)
            p += 1
            # if p == 10:
            #     quit()
        puzzle = cpy
        return puzzle

    def pad_puzzle(self, puzzle, chunks):
        # print("chunks for padding:", chunks)
        # Ensure that the chunks are in a nested list of lists, no ndarrays are wanted
        chunks_list = [[row.tolist() if isinstance(row, np.ndarray) else row for row in chunk] for chunk in chunks[0]]
        print([type(chunk) for chunk in chunks_list])
        top_chunk, bottom_chunk, left_chunk, right_chunk = chunks_list
        # print("\n\ttop_chunk:\n", top_chunk)
        # print("\n\tbottom_chunk:\n", bottom_chunk)
        # print("\n\tleft_chunk:\n", left_chunk)
        # print("\n\tright_chunk:\n", right_chunk)
        # print("chunks", chunks)
        # print_puzzle(chunks)
        # print("puzzle: rows", len(puzzle), "cols", len(puzzle[0]))
        print("add", len(top_chunk), "rows to the top,", len(bottom_chunk), "rows to the bottom")
        print("add", len(left_chunk), "cols to the left,", len(right_chunk), "cols to the right")
        # print("\ttop_chunk (", len(top_chunk), "), (", len(top_chunk[0]), "):\n", top_chunk)
        # print("\tbottom_chunk (", len(bottom_chunk), "), (", len(bottom_chunk[0]), "):\n", bottom_chunk)
        # print("\tleft_chunk (", len(left_chunk), "), (", len(left_chunk[0]), "):\n", left_chunk)
        # print("\tright_chunk (", len(right_chunk), "), (", len(right_chunk[0]), "):\n", right_chunk)
        # puzzle = [row.tolist() if isinstance(row, np.ndarray) else row for row in puzzle]
        puzzle = ensure_list(puzzle)
        # print("\n\tBEFORE PADDING")
        # print_puzzle(puzzle)
        puzzle = top_chunk + puzzle + bottom_chunk
        for r in range(len(puzzle)):
            if len(top_chunk) <= r < (len(puzzle) - len(bottom_chunk)):
                left = [row[r] for row in left_chunk]
                right = [row[r] for row in right_chunk]
                puzzle[r] = left + puzzle[r] + right
        print("\n\tAFTER PADDING")
        print_puzzle(puzzle)
        return puzzle

    def remaining_spaces(self, solved_puzzle):
        remaining = []
        for r, row in enumerate(solved_puzzle):
            i, j = 0, 1
            remaining_row = []
            while j < len(row):
                if row[i] == 0:
                    while j < len(row):
                        if row[j] != 0:
                            break
                        j += 1
                    remaining_row.append((i, j))
                    i = j
                j += 1
                i += 1
            remaining.append(remaining_row)
        return remaining

    def combine_rows(self, row_1, row_2):
        for i in range(min(len(row_1), len(row_2))):
            if row_2[i] == 1:
                row_1[i] = row_2[i]
        return row_1

    # What is the max number of hints in the vertical hints list
    def max_n_v_hints(self):
        return max([len(l) for l in self.v_hints_in])

    # What is the max number of hints in the horizontal hints list
    def max_n_h_hints(self):
        return max([len(l) for l in self.h_hints_in])

    # Cell is marked but uncovered
    def set_cell_marked(self, r, c):
        print("Puzzle at [" + str(r) + "][" + str(c) + "] is marked")
        self.solving_status[r][c] = LEGEND["marked"]

    # Make a guess and uncover a cell, can be right or wrong
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
        # print("r",c,"c",c,"\tsolving_status:\t\n")
        # print_puzzle(self.solving_status)
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
        elif self.puzzle_in[r][c] == LEGEND["marked"]:
            return LIGHT_GREY
        return self.legend[self.puzzle_in[r][c]]


# Calculate all permutations of r size of a given list of elements,
# then sort the list using the sort_idx.
# TODO Needs to converted to set twice to eliminate duplicates. Once after creation of permutations, then again after sorting them.
def permutations(arr, size=None, sort_idx=None):
    size = len(arr) if size is None else size
    sort_idx = 0 if sort_idx is None else sort_idx
    return sort_tuple(list(set(itertools.combinations(arr, size))), sort_idx)


# Sort a list of tuples using the given idx as the sort key
def sort_tuple(lst, idx):
    if any(lst):
        lst.sort(key=lambda tup: tup[idx])
    return lst


def combinations(ranges):
    comb = []
    if any(ranges):
        comb = [[i] for i in ranges[0]]
        for j, r in enumerate(ranges[1:]):
            for i in r:
                # print("r:", r, "i:", i, "\ncomb:", comb)
                comb += [c + [i] for c in comb if len(c) == j + 1]
    return [c for c in comb if len(c) == len(ranges)]


# Check that the number of colored cells is the same as the total desired
# and the row and col hints calculated match the original.
def check_puzzle_is_solved(puzzle, h_hints, v_hints):
    total_to_be_colored = sum([sum(row) for row in h_hints])
    total_colored = sum([np_count(row, 1) for row in puzzle])
    calc_h_hints = count_hints(puzzle)
    puzzle = np.transpose(puzzle)
    calc_v_hints = count_hints(puzzle)
    puzzle = np.transpose(puzzle)
    # print("total_colored:", total_colored)
    # print("total_to_be_colored:", total_to_be_colored)
    # print("calc_h_hints", calc_h_hints)
    # print("calc_v_hints", calc_v_hints)
    return total_to_be_colored == total_colored and h_hints == calc_h_hints and v_hints == calc_v_hints


# Ensure that all elements of a puzzle are either 0 or 1
def ensure_0_1(puzzle):
    return [[el if el == 1 else 0 for el in r] for r in puzzle]


# This function should only be called with a completed puzzle, as all it
# does is count consecutive marked cells.
def count_hints(puzzle):
    puzz = ensure_0_1(puzzle)
    rows = len(puzz)
    cols = len(puzz[0])
    res = [[] for i in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (puzz[r][c] == 1 and c == 0) or (puzz[r][c] == 1 and puzz[r][c - 1] == 0):
                count = 1
                temp = c
                while temp < cols - 1 and puzz[r][temp + 1] == 1:
                    count += 1
                    temp += 1
                res[r].append(count)
    for r in range(rows):
        if len(res[r]) == 0:
            res[r] = [0]
    # print('h_hints', res)
    return res


def remaining_list(lst, size):
    left_over = []
    for i in range(size):
        if lst and i not in lst:
            left_over.append(i)
    return left_over


def outside_indices(lst, size):
    if not lst or len(lst) == size:
        return None, None
    left_over = remaining_list(lst, size)
    print("lwft_over", left_over)
    print("max(0, left_over[0] - 1)",max(0, left_over[0] - 1), "min(size, left_over[-1] + 1)", min(size, left_over[-1] + 1))
    return max(0, left_over[0] - 1), min(size - 1, left_over[-1] + 1)


def deep_copy(arr):
    return [r.copy() if type(r) is list else r for r in arr]


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


def print_puzzle(puzzle):
    puzzle = ensure_list(puzzle)
    if puzzle:
        print("   " + "".join(list(map(lambda x: str(x).rjust(3), [i for i in range(len(puzzle[0]))]))))
        for i, r in enumerate(puzzle):
            print(str(i).rjust(2), "".join(list(map(lambda x: x.rjust(3), map(str, r)))))
    else:
        print("Puzzle is empty")


def cut_visual(*args):
    puzzle, tc, bc, lc, rc = args
    if not puzzle:
        print("No puzzle given")
        return
    rows = len(puzzle)
    cols = len(puzzle[0])
    border = "\t\t" + "".join(["_" for i in range((cols * 3) + 6)])
    result = "\n\t\t\tCut visual\n\n"
    for r, row in enumerate(puzzle):
        left = row[:lc + 1]
        right = row[rc:]
        row_str = "".join(str(c).rjust(3) for c in left) + " ||" + "".join(
            str(c).rjust(3) for c in row[lc + 1: rc]) + "|| " + "".join(
            str(c).rjust(3) for c in right)
        if r == tc + 1 or r == bc:
            result += border + "\n"
        result += "\t\t" + row_str + "\n"
    print(result)


# Takes a list or ndarray object and returns a list of the elements.
# Works for 2D lists and ndarrys.
def ensure_list(arr):
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    for i, el in enumerate(arr):
        if isinstance(el, np.ndarray):
            arr[i] = el.tolist()
    return arr


# Count elements in a ndarray from the numpy library
def np_count(arr, val):
    unique, counts = np.unique(arr, return_counts=True)
    values = dict(zip(unique, counts))
    return values[val] if val in values else 0
