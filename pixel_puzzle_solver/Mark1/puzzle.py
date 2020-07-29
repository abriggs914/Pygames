class Puzzle:
    def __init__(self, name, id, puzzle, v_hints_in = None):
        if not verify(puzzle, v_hints_in):
            print('Error Invalid puzzle dimensions')
            puzzle = self.pad_puzzle(puzzle)
            # raise ValueError('Error Invalid puzzle dimensions')
        # else:
        #     print('else')
        # print('puzzle_in:',puzzle)
        self.name = name.title()
        self.id = id
        self.solved = False
        self.solving_history = None
        if v_hints_in is not None:
            self.rows = len(puzzle)
            self.cols = len(v_hints_in)
            self.horizontal_hints = puzzle
            self.vertical_hints = v_hints_in
            sum_puzzle = sum([sum(puzzle[i]) for i in range(len(puzzle))])
            self.num_pixels = sum_puzzle # number of pixels coloured in pixel
            puzzle = self.gen_solved_puzzle()  # stores the parameter value
            self.puzzle_board = puzzle
            self.solved_puzzle_board = puzzle
            self.given_solution = False
        else:
            self.puzzle_board = puzzle  # stores the parameter value
            self.rows = len(puzzle)  # num rows in puzzle
            self.cols = len(puzzle[0])  # num cols in puzzle
            self.horizontal_hints = self.gen_horizontal_hints()  # list of lists containing the h_hints to puzzle
            self.vertical_hints = self.gen_vertical_hints()  # list of lists containing the v_hints to puzzle
            self.num_pixels = self.count_num_pixels(puzzle)  # number of pixels coloured in pixel
            # self.solved_puzzle_board = self.gen_solved_puzzle()
            self.given_solution = True

        self.vertical_divider = self.gen_vertical_divider()
        self.vertical_hints_height = self.get_vertical_height()
        self.horizontal_spacer = self.gen_horizontal_spacer()  # string storing space based on max len of sublists in h_hints
        self.solution_board = self.gen_solution_board()

    def __repr__(self):
        # self.print_history(self.solving_history)
        return self.solution_board

    def get_name(self):
        return self.name

    def gen_solution_board(self):
        board = self.presentify()
        name = self.name
        id = self.id
        res = '\n\tPuzzle: ' + name + ', id: ' + str(id) + '\n\t\t\t' + str(self.rows) + ' X ' + str(self.cols) + '\n'
        if not self.solved:
            res += '\n\t-- UNSOLVED PRINTING SOLUTION --\n'
            if not self.given_solution:
                res += '\t-- *BEST AVAILABLE SOLUTION* --\n'
        res += self.vertical_hint_presentation()
        h_hints = self.horizontal_hint_presentation()
        length = len(self.horizontal_spacer)
        for i in range(len(board)):
            # print('self.height', self.vertical_hints_height)
            hint = h_hints[i]
            string = ''
            # print('length', length, ' len(hint', len(hint))
            string += hint + ' '
            line = board[i]
            for val in line:
                string += str(val)
            res += string + ' |\n'
        # bottom line
        line = '|'
        for i in range(length - 1):
            line += '_'
        res += line + '|' + self.vertical_divider + '|'
        res += '\n'
        return res

    def pad_puzzle(self, puzzle):
        # new_puzzle = []
        # rows = 0
        # cols = 0
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
                        p = row_len - j
                        # print('i:', i, ', j:', j, ', row_len:', row_len, ', p:', p)
                        if j < row_len:
                            new_puzzle[i][j] = puzzle[i][j]
                            # using { if p < row_len: new_puzzle[i][j] = puzzle[i][p] }
                            # instead of the above will horizontally flip the puzzle
                        j -= 1
                    i -= 1
                    j = cols - 1
                # print('new_puzzle', new_puzzle)
            else:
                new_puzzle = sample_smiley
        else:
            new_puzzle = sample_smiley
        return new_puzzle

    def gen_vertical_hints(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
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
        print('v_hints', res)
        return res

    def gen_horizontal_hints(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
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
        print('h_hints', res)
        return res

    def presentify(self):
        board = self.puzzle_board
        rows = self.rows
        cols = self.cols
        res = [[] for i in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 1:
                    res[r].append('#')
                else:
                    res[r].append(' ')
        return res

    def vertical_hint_presentation(self):
        hints = self.vertical_hints
        cols = self.cols
        # size = max([len(hints[x]) for x in range(cols)])
        size = self.vertical_hints_height
        divider = self.vertical_divider
        # Top line of vertical hints
        string = '  ' + self.horizontal_spacer[:-1] + divider + '\n'
        length = len(self.horizontal_spacer)
        line = ' '
        for i in range(length - 1):
            line += '_'
        hint_table = [[None for j in range(size)] for i in range(cols)]
        single_digit_hints = []
        for r in range(len(hint_table)):
            lst = hints[r]
            new_lst = []
            for c in range(len(lst)):
                el = lst[c]
                # print('el',el)
                if type(el) == int and el // 10 > 0:
                    # print('el:',el,', el // 10:', (el // 10))
                    first_digit = el // 10
                    second_digit = el % 10
                    new_lst += ['_', first_digit, second_digit, '_']
                    # print('sub_a', sub_a, ', sub_b:', sub_b)
                elif type(el) != int or (type(el) == int and el // 10 <= 0):
                    new_lst.append(el)
            new_lst.reverse()
            single_digit_hints.append(new_lst)
        # print('single_digits_hints', single_digit_hints)
        hints = single_digit_hints
        # print('hint_table', hint_table)
        c = 0
        while c in range(cols):
            # print('c', c)
            string += ' ' + self.horizontal_spacer
            for t in range(cols):
                # print('double_digit', double_digit)
                # print('hints[t]:', hints[t], ' t: ', t)
                if t == 0 and size > 0:
                    string += ' '
                if len(hints[t]) > 0 and len(hints[t]) == size:
                    string += str(hints[t][size - 1])
                    if len(hints[t]) != 1:
                        hints[t].pop()
                elif size != 0:
                    string += ' '
                if (t == cols - 1) and size >= 1:
                    string += ' |\n'
            size -= 1
            # print('size', size)
            if size < 1:
                break
        # left cover of horizontal hint table
        string += line + '|' + divider + '|\n'
        return string

    # def vertical_hint_presectation_rec(self, size):
    #     cols = self.cols
    def gen_horizontal_spacer(self):
        hints = self.horizontal_hints
        width = max([((len(hints[x]) + 3) * 2) for x in range(len(hints))])
        res = ' '
        for i in range(width):
            res += ' '
        res += ' |'
        # print('\tres:', len(res))
        return res

    def gen_vertical_divider(self):
        cols = self.cols + 2
        divider = ''
        for i in range(cols):
            divider += '_'
        return divider

    def get_vertical_height(self):
        hints = self.vertical_hints
        cols = self.cols
        size = max([len(hints[x]) for x in range(cols)])
        new_hints = [max(hints[y]) for y in range(len(hints))]
        new_hints = [4 if ((new_hints[x] // 10) > 0) else 1 for x in range(len(new_hints))]
        max_run = max(new_hints)
        max_run_index = new_hints.index(max_run)
        max_run += len(hints[max_run_index])
        # print('new_hints', new_hints, ' size', size, ' max_run', max_run)
        size = max(size, max_run)
        return size

    def horizontal_hint_presentation(self):
        hints = self.horizontal_hints
        res = []
        for row in hints:
            # res.append(str(row) + '\n')
            string = self.stringify_list(row)  # + '\n'
            length = len(string)
            ab = '|'
            # print('len', len(self.horizontal_spacer), ' len', length)
            while ((len(self.horizontal_spacer) - length) - 3) > 0:
                length += 1
                ab += ' '
            res.append(ab + string + '  |')
        return res

    def stringify_list(self, row):
        res = '|'
        for el in row:
            res += str(el) + '|'
        return res

    def count_num_pixels(self, puzzle):
        num_pixels = 0
        for i in range(len(puzzle)):
            # print('val',val)
            if type(puzzle[i]) != list:
                # print('puzzle[i]',puzzle[i])
                num_pixels += puzzle[i]
            else:
                for j in range(len(puzzle[i])):
                    num_pixels += puzzle[i][j]
        return num_pixels

    def transpose_puzzle(self, board):
        r = 0
        c = 0
        new_board = [[0 for c in range(len(board))] for r in range(len(board[r]))]
        # printA('board',board)
        while r in range(len(board)):
            while c in range(len(board[r])):
                new_board[c][r] = board[r][c]
                c += 1
            r += 1
            c = 0
        # printA('newBoard', new_board)
        return new_board

    def space(self, n):
        n = n if 0 <= n <= 100 else 5
        return [0 for i in range(n)]

    # hint_1 = [4, 7, 4]
    # hint_2 = [1]
    # hint_3 = [6, 6, 6]
    # hint_4 = [6, 11]

    def len_hints(self, hints):
        return sum(hints) + len(hints) - 1

    def gen_rest_possibilities(self, space, hints, delta):
        if delta < 1:
            return []
        else:
            res = []
            i = 1
            while (i - 1) in range(delta):
                temp = space[-i:] + space[0: len(space) - i]
                # print('temp:\t', temp)
                i += 1
                res.append(temp)
            # printA('res',res)
            return res

    def space_hints(self, space, hints):
        if self.len_hints(hints) > len(space):
            print('hint size is too large')
            return
        else:
            curr_space_index = 0
            last_space_index = curr_space_index
            delta = len(space) - self.len_hints(hints)
            for hint in hints:
                curr_space_index += hint
                i = last_space_index
                # print('i:',i,'last_space_index:',last_space_index,'curr_space_index:',curr_space_index)
                while i in range(last_space_index, curr_space_index):
                    space[i] = 1
                    i += 1
                if hints.index(hint) < len(hints) - 1:
                    curr_space_index += 1
                last_space_index = curr_space_index
            # rev = space.copy()
            # rev.reverse()
            res = [space]
            # print('space:\t', space)
            res += self.gen_rest_possibilities(space, hints, delta)
            # res += [rev]
            # print('rev:\t', rev)
            return res

    def guess_row(self, space, hints):
        # print('Fitting', hints, 'into space size', len(space), ',', space)
        rows = self.space_hints(space, hints)
        # print('rows:', rows)
        delta = len(space) - self.len_hints(hints)
        if delta == 0:
            res = [1 if rows[0][i] == 1 else 9 for i in range(len(rows[0]))]
            return res
        col = 0
        res = []
        while col in range(len(rows[0])):
            fill_in = True
            valid = False
            j = 0
            while j in range(len(rows)):
                if rows[j][col] == 0:
                    fill_in = False
                else:
                    valid |= True
                j += 1
            if fill_in:
                res.append(1)
            elif not valid:
                res.append(9)
            else:
                res.append(0)
            col += 1
        # print('res:\t', res)
        return res

    def guess_puzzle(self, puzzle_in):
        puzzle_name = self.name # puzzle_in[0]
        puzzle_id = self.id # puzzle_in[1]
        puzzle_h_hints = puzzle_in[0]
        puzzle_v_hints = puzzle_in[1]
        board = [[0 for i in range(len(puzzle_v_hints))] for j in range(len(puzzle_h_hints))]
        guessed_h_rows = [self.guess_row(self.space(len(puzzle_v_hints)), row_hints) for row_hints in puzzle_h_hints]
        # printA('guessed_h_rows:', guessed_h_rows)
        self.solving_history['level_1']['horizontal_board'] = guessed_h_rows.copy()
        guessed_v_rows = [self.guess_row(self.space(len(puzzle_h_hints)), row_hints) for row_hints in puzzle_v_hints]
        # printA('guessed_v_rows:', guessed_v_rows)
        guessed_v_rows = self.transpose_puzzle(guessed_v_rows)
        self.solving_history['level_1']['vertical_board'] = guessed_v_rows.copy()
        # printA('guessed_v_rows:', guessed_v_rows)
        i, j = 0, 0
        while i in range(len(guessed_v_rows)):
            j = 0
            while j in range(len(guessed_v_rows[i])):
                if guessed_h_rows[i][j] == 1 or guessed_v_rows[i][j] == 1:
                    board[i][j] = 1
                elif guessed_h_rows[i][j] == 9 or guessed_v_rows[i][j] == 9:
                    board[i][j] = 0
                # print('i:',i,'j:',j)
                j += 1
            i += 1
        # print(board)
        return board

    # def check_solved_status(self, board):

    def gen_solved_puzzle(self):
        print('\n\tLevel 1 Solving\n')
        solving_history = {'stats': {}, 'level_1': {}}
        self.solving_history = solving_history
        n_rows = self.rows
        n_cols = self.cols
        v_hints = self.vertical_hints
        h_hints = self.horizontal_hints
        solving_history['stats']['n_rows'] = n_rows
        solving_history['stats']['n_cols'] = n_cols
        solving_history['stats']['v_hints'] = v_hints
        solving_history['stats']['h_hints'] = h_hints
        # num_pixels = self.count_num_pixels(self.puzzle_board)
        # print('n_rows:', n_rows, ', n_cols:', n_cols)  # , ', num_pixels:', num_pixels)
        # printA('v_hints:', v_hints)
        # printA('h_hints:', h_hints)


        # board = [[0 for i in range(n_cols)] for x in range(n_rows)]
        # t_board = self.transpose_puzzle(board.copy())
        # i = 0
        # while i in range(len(board)):
        #     # print('using hints:',h_hints)
        #     board[i] = self.horizontal_row_fill(board[i], h_hints[i])
        #     i += 1
        # solving_history['level_1']['horizontal_board'] = board.copy()
        # printA('horizontal_board', board)
        # i = 0
        # while i in range(len(t_board)):
        #     # print('using hints:',v_hints)
        #     t_board[i] = self.horizontal_row_fill(t_board[i], v_hints[i])
        #     i += 1
        # t_board = self.transpose_puzzle(t_board)
        # solving_history['level_1']['vertical_board'] = t_board.copy()
        # printA('vertical_board', t_board)
        # i = 0
        # j = 0
        # while i in range(len(board)):
        #     while j in range(len(board[i])):
        #         if t_board[i][j] == 1:
        #             board[i][j] = 1
        #         j += 1
        #     j = 0
        #     i += 1
        board = self.guess_puzzle([h_hints, v_hints])


        printA('resulting board',board)
        solving_history['level_1']['resulting_board'] = board.copy()
        if self.check_board(board):
            self.solving_history = solving_history
            return board



        i = 0
        j = 0
        while i in range(len(board)):
            board[i] = self.row_continuity(board[i], h_hints, i)
            i += 1

        printA('row_continuity',board)
        solving_history['level_1']['row_continuity'] = board.copy()
        if self.check_board(board):
            self.solving_history = solving_history
            return board

        i = 0
        j = 0
        t_board = self.transpose_puzzle(board)
        while i in range(len(t_board)):
            t_board[i] = self.row_continuity(t_board[i], v_hints, i)
            i += 1

        board = self.transpose_puzzle(t_board)
        printA('col_continuity',board)
        solving_history['level_1']['col_continuity'] = board.copy()
        if self.check_board(board):
            self.solving_history = solving_history
            return board

        self.solving_history = solving_history
        
        board = self.solve_level_2(board)
        printA('returned advanced board', board)
        status = self.check_board(board)
        print("status: " + str(status))
        return board

    def solve_level_2(self, board):
        n_rows = self.rows
        n_cols = self.cols
        v_hints = self.vertical_hints
        h_hints = self.horizontal_hints
        new_h_board, new_h_hints, h_cut_idxs, new_v_board, new_v_hints, v_cut_idxs = self.shrink(board, h_hints, v_hints)
        # printA("new_h_board ", new_h_board)
        # printA("new_v_board ", new_v_board)
        # print("new_h_hints " + str(new_h_hints) + ", h_cut_idxs: " + str(h_cut_idxs))
        # print("new_v_hints " + str(new_v_hints) + ", v_cut_idxs: " + str(v_cut_idxs))
        new_board = self.cut_board(board, h_cut_idxs, v_cut_idxs)
        # printA("New Board IN", new_board)

        new_board = self.solving_level_2(new_board, new_h_hints, new_v_hints)
        # printA("New Board OUT", new_board)

        new_board = self.pad_board(board, new_board, h_cut_idxs, v_cut_idxs)
        # printA("New Board AFTER Pad", new_board)
        return new_board


    def solving_level_2(self, board, h_hints, v_hints):
        # printA("BOARD IN", board)
        # print("BOARD: " + str(board))
        n_rows = len(board)
        n_cols = 0 if (len(board) == 0) else len(board[0])
        # print("Solving horizontal")
        for i in range(len(h_hints)):
            hint = h_hints[i]
            row = board[i]
            # print("i: " + str(i) + ", n_cols: " + str(n_cols) + ", row: " + str(row) + ", hint: " + str(hint))
            self.fill_row(row, hint)
        board = self.transpose_puzzle(board)
        # printA("after horizontal", board)
        # print("Solving vertical")
        for i in range(len(v_hints)):
            hint = v_hints[i]
            col = board[i]
            # print("i: " + str(i) + ", n_rows: " + str(n_rows) + ", col: " + str(col) + ", hint: " + str(hint))
            self.fill_row(col, hint)
        board = self.transpose_puzzle(board)
        # printA("BOARD OUT", board)
        return board

    def pad_board(self, board, small_board, h_cuts, v_cuts):
        temp = []
        c1 = h_cuts[0]
        c2 = h_cuts[1]
        r1 = v_cuts[0]
        r2 = v_cuts[1]
        for r in range(len(board)):
            row = []
            for c in range(len(board[r])):
                if r > r1 and r < r2 and c > c1 and c < c2 :
                    # print("r(" + str(r) + ") - r1(" + str(r1) + ") + 1: " + str(r - (r1 + 1)) + ", c(" + str(c) + ") - c1(" + str(c1) + ") + 1: " + str(c - (c1 + 1)))
                    row.append(small_board[r - (r1 + 1)][c - (c1 + 1)])
                else:
                    row.append(board[r][c])
            temp.append(row)

        # printA("temp", temp)
        return temp


        # print("temp: " + str(temp) + ", new_board: " + str(small_board) + ", h_cuts: " + str(h_cuts) + ", v_cuts: " + str(v_cuts))
        # print("temp[:h_cuts[0] + 1]: " + str(temp[:h_cuts[0] + 1]) + ", flatten_list(temp[:h_cuts[0] + 1]): " + str(flatten_list(temp[:h_cuts[0] + 1])))
        # new_board = flatten_list(temp[:h_cuts[0] + 1])[v_cuts[0] : v_cuts[1]] + small_board + flatten_list(temp[h_cuts[1]:])[v_cuts[0] + 1 : v_cuts[1] + 1]
        # return new_board

    def cut_board(self, board, h_cuts, v_cuts):
        new_board = board.copy()
        new_board = new_board[h_cuts[0] + 1 : h_cuts[1]]
        new_board = self.transpose_puzzle(new_board)
        new_board = new_board[v_cuts[0] + 1 : v_cuts[1]]
        return new_board

    def fill_row(self, row, hints):
        if len(row) == 0 or (len(hints) == 1 and hints[0] == 0):
            # base case
            return
        num_to_cover = sum(hints)
        num_covered = sum(row)
        if num_covered == num_to_cover:
            return
        space = len(row)
        hint_to_place = hints[0]
        rest_hints = sum(hints[1:])
        rest_space = (len(hints) - 1) + rest_hints
        new_space = space - rest_space
        diff = new_space - hint_to_place
        begin_idx = max(0, diff)
        end_idx = max(0, min(diff, space - 1))
        if begin_idx <= end_idx:
            # do colour
            if diff == 0:
                begin_idx = 0
                end_idx = hint_to_place - 1
            for i in range(begin_idx, end_idx + 1):
                # m = "\t(B,E)=(" + str(begin_idx) + ", " + str(end_idx) + "), i=(" + str(i) + "), row=(" + str(row) + "), hints=(" + str(hints) + "), hint(" + str(hint_to_place) + "), diff=(" + str(diff) + "), new_space=(" + str(new_space) + "), space=(" + str(space) + "), rest_space=(" + str(rest_space) + ")"
                row[i] = 1
                # m += "\n=>\t\t" + "(B,E)=(" + str(begin_idx) + ", " + str(end_idx) + "), i=(" + str(i) + "), row=(" + str(row) + "), hints=(" + str(hints) + "), hint(" + str(hint_to_place) + "), rest_hints=(" + str(hints[1:]) + "), rest_list=(" + str(row[1:]) + ")"
                # print(m)
        else:
            # print("\tNOT (B,E)=(" + str(begin_idx) + ", " + str(end_idx) + ")")
            pass
        if rest_hints > 0:
            self.fill_row(row[end_idx:], hints[1:])


    # def len_hints(self, arr):
    #     return sum(arr) + len(arr) - 1

    # def how_many_counted(self, arr):
    #     seen = False
    #     blanks = 0
    #     for el in arr:
    #         if el == 0:
    #             if not seen:
    #                 blanks += 1
    #         else:
    #             if not seen:
    #                 blanks += 1
    #             seen = True
    #     # print('returning blanks:',blanks)
    #     return blanks

    # def usable_space(self, space):
    #     res = []
    #     space_sum = sum(space)
    #     if space_sum == 0:
    #         return space, space_sum
    #     i = len(space) - 1
    #     while i in range(len(space)):
    #         if space[i] == 1:
    #             i += 1
    #             break
    #         i -= 1
    #     if i >= 0:
    #         i += 1
    #     space_sum += self.how_many_counted(space[:i + 1])
    #     # print('returning i:',i)
    #     # print(space[i:])
    #     return space[i:], space_sum

    # def calc_diff(self, arr, space, index):
    #     length = len(arr)
    #     if length <= index:
    #         # print('already finished!')
    #         return -1
    #     print('fitting ' + str(arr) + ' into ' + str(space) + ' starting at ' + str(arr[index]))
    #     new_space, space_to_remove = self.usable_space(space)
    #     spaces_len = len(new_space)
    #     v = (sum(arr[:index]))
    #     # print('v',v)
    #     covered_space = sum(space)
    #     to_be_covered = sum(arr)
    #     space_left_to_cover = self.len_hints(arr[index:])
    #     arr_len = space_left_to_cover
    #     if covered_space == to_be_covered:
    #         # print('base')
    #         return -1
    #     # print('new_space',new_space)
    #     # print('space_to_remove',space_to_remove)
    #     # print('spaces_len',spaces_len)
    #     # print('arr_len',arr_len)
    #     return spaces_len - arr_len

    # def fill_row(self, row, hints, index, ext_buff):
    #     hint = hints[index]
    #     new_row = row  # .copy()
    #     left_hints = hints[:index]
    #     right_hints = hints[index + 1:]
    #     left = self.len_hints(left_hints) + 1
    #     right = self.len_hints(right_hints) + 1
    #     remainder = len(row)
    #     start = -1
    #     end = -1
    #     if index == 0:
    #         if hint > ext_buff:
    #             remainder = hint - ext_buff
    #             start = ext_buff
    #             end = ext_buff + remainder
    #     elif index == (len(hints) - 1):
    #         if hint > ext_buff:
    #             remainder = hint - ext_buff
    #             start = len(row) - remainder - ext_buff
    #             end = len(row) - ext_buff
    #     else:
    #         remainder = len(row) - left - right - hint
    #         if hint > remainder:
    #             start = left + remainder
    #             end = len(row) - right - remainder
    #     # print('left_hints:',left_hints,' right_hints:',right_hints,' left:',left,' right:', right, ' remainder:',remainder)
    #     i = 0
    #     # print('start:',start,'end:',end)
    #     while i in range(len(row)):
    #         if start <= i < end:
    #             new_row[i] = 1
    #         i += 1
    #     return new_row

    # def horizontal_row_fill(self, puzzle_row, hints):
    #     i = 0
    #     temp_row = puzzle_row.copy()
    #     while i in range(len(hints)):
    #         ext_buffer = len(puzzle_row) - self.len_hints(hints)  # calc_diff(hints, puzzle_row, i)
    #         print('fitting ' + str(hints) + ' into ' + str(puzzle_row) + ' starting at ' + str(
    #             hints[i]) + ' buffer_space: ' + str(ext_buffer))
    #         temp_row = self.fill_row(puzzle_row, hints, i, ext_buffer)
    #         i += 1
    #     return temp_row

    def row_continuity(self, row, hints, index):
        n_cols = len(row)
        row_sum = sum(row)
        hints_sum = sum([sum(hints[i]) for i in range(len(hints))])
        if row_sum == hints_sum:
            return row
        c = 0
        curr_hint = 0
        while c in range(n_cols):
            # print('c',c)
            if row[c] == 1:
                if c == 0:
                    # print('ends')
                    t = c
                    seen = False
                    while t in range(hints[index][curr_hint]):
                        if row[t] == 0:
                            # print('adding', t)
                            seen = True
                        row[t] = 1
                        if c == n_cols - 1:
                            t -= 1
                        else:
                            t += 1
                    c = t
                    curr_hint += 1
                    if seen:
                        # print('to', c)
                        seen = False
                elif c == n_cols - 1:
                    # print('ends')
                    t = c
                    seen = False
                    hint = hints[index][-1]
                    # print('hint',hint)
                    while (len(row) - t) in range(hints[index][-1]):
                        if row[t] == 0:
                            # print('adding',t)
                            seen = True
                        row[t - 1] = 1
                        if c == n_cols - 1:
                            t -= 1
                        else:
                            t += 1
                    curr_hint += 1
                    if seen:
                        # print('to',c)
                        seen = False
            c += 1
        # print('row:',row)
        return row

    def zero_rows_and_cols(self, board, token=None):
        h_hints = self.horizontal_hints
        v_hints = self.vertical_hints
        dims = (self.rows, self.cols)
        r = 0
        c = 0
        while r in range(dims[0]):
            if sum(h_hints[r]) == 0:
                while c in range(dims[1]):
                    board[r][c] = token
                    c += 1
            r += 1
            c = 0
        board = self.transpose_puzzle(board)
        r = 0
        c = 0
        while r in range(dims[1]):
            if sum(v_hints[r]) == 0:
                while c in range(dims[0]):
                    board[r][c] = token
                    c += 1
            r += 1
            c = 0
        board = self.transpose_puzzle(board)
        return board

    def advanced_solving(self, board):
        print('\n\tLevel 2 Solving\n')

        printA('\n\n\n\n\n\nboard',board)
        h_hints = self.horizontal_hints
        v_hints = self.vertical_hints
        # level_2 = {}
        r = 0
        c = 0
        cuts = {}
        temp = (None,None)
        param_board = board.copy()
        board = self.zero_rows_and_cols(board, 0)
        t_board = board.copy()
        x_board, temp = self.shrink_board(board, h_hints, v_hints, 'row')
        cuts['top_row_cut'] = temp[0] if temp[0] > 0 else 1 if temp[0] == 0 else 0 # this causes an error when indexing later in pad_shrunken_board
        cuts['bottom_row_cut'] = temp[1]
        # printA('row_shrunk',board)
        # board = self.transpose_puzzle(board)
        t_board, temp = self.shrink_board(t_board, h_hints, v_hints, 'col')
        cuts['left_col_cut'] = temp[0] if temp[0] > 0 else 1 if temp[0] == 0 else 0
        cuts['right_col_cut'] = temp[1]
        print('top_cut:',cuts['top_row_cut'],'bottom_cut:',cuts['bottom_row_cut'])
        print('left_cut:',cuts['left_col_cut'],'right_cut:',cuts['right_col_cut'])
        printA('level 2 CURR BOARD (param-board):', param_board)
        res_cut_board = param_board[cuts['top_row_cut']: cuts['bottom_row_cut']]
        printA('level 2 CURR BOARD (res-cut-board):', res_cut_board)
        res_cut_board = [res_cut_board[i][cuts['left_col_cut']: cuts['right_col_cut']] for i in range(len(res_cut_board))]
        printA('level 2 CURR Shrunk BOARD:', res_cut_board)
        new_v_hints = self.vertical_hints_adjustment(v_hints, param_board, res_cut_board, cuts)
        new_h_hints = self.horizontal_hints_adjustment(h_hints, param_board, res_cut_board, cuts)
        print('v_hints:', v_hints)
        print('new_v_hints:', new_v_hints)
        print('h_hints:', h_hints)
        print('new_h_hints:', new_h_hints)
        # board = self.adjust_board(board, t_board, cuts)
        # # board = self.transpose_puzzle(board)
        # printA('col_shrunk',board)
        # # while r in range(len(param_board))
        # printA('advanced_solving', board)
        # n_rows = len(board)
        # n_cols = len(board[0])
        # v_hints = self.vertical_hints_adjustment(v_hints, param_board, board)
        # h_hints = self.horizontal_hints_adjustment(h_hints, param_board, board)
        # num_pixels = self.num_pixels
        # print('n_rows:', n_rows, ', n_cols:', n_cols, ', num_pixels:', num_pixels)
        # # printA('v_hints:', v_hints)
        # # printA('h_hints:', h_hints)
        # board = [[0 for i in range(n_cols)] for x in range(n_rows)]
        # t_board = self.transpose_puzzle(board.copy())
        # i = 0
        # while i in range(len(board)):
        #     # print('using hints:',h_hints)
        #     board[i] = self.horizontal_row_fill(board[i], h_hints[i])
        #     i += 1
        # printA('advanced_horizontal_board', board)
        # i = 0
        # while i in range(len(t_board)):
        #     # print('using hints:',v_hints)
        #     t_board[i] = self.horizontal_row_fill(t_board[i], v_hints[i])
        #     i += 1
        # board = self.transpose_puzzle(t_board)
        # printA('advanced_vertical_board', board)
        # i = 0
        # j = 0
        # # while i in range(len(board)):
        # #     while j in range(len(board[i])):
        # #         if t_board[i][j] == 1:
        # #             board[i][j] = 1
        # #         j += 1
        # #     j = 0
        # #     i += 1
        # # printA('advanced_resulting board', board)
        # if self.check_board(self.pad_shrunken_board(board, param_board, cuts)):
        #     return board
        #
        # i = 0
        # j = 0
        # while i in range(len(board)):
        #     board[i] = self.row_continuity(board[i], h_hints, i)
        #     i += 1
        #
        # printA('advanced_row_continuity', board)
        # if self.check_board(board):
        #     return board
        #
        # i = 0
        # j = 0
        # t_board = self.transpose_puzzle(board)
        # while i in range(len(t_board)):
        #     t_board[i] = self.row_continuity(t_board[i], v_hints, i)
        #     i += 1
        #
        # board = self.transpose_puzzle(t_board)
        # printA('advanced_col_continuity', board)
        if self.check_board(self.pad_shrunken_board(res_cut_board, param_board, cuts)):
            return board
        print('\n\nNEEDS LEVEL 3\n\n')
        return board

    def shrink(self, board, v_hints, h_hints):
        new_h_board, new_h_hints, h_cut_idxs = self.shrink_board(board, h_hints, v_hints, "")
        new_v_board, new_v_hints, v_cut_idxs = self.shrink_board(board, h_hints, v_hints, "col")
        return new_h_board, new_h_hints, h_cut_idxs, new_v_board, new_v_hints, v_cut_idxs

    def shrink_board(self, board, h_hints, v_hints, how):
        # h_hints = self.horizontal_hints
        # v_hints = self.vertical_hints
        # dims = [self.rows, self.cols]
        dims = [len(board[0]), len(board)]
        print("Before dims: " + str(dims) + ", h_hints: " + str(h_hints) + ", v_hints: " + str(v_hints))
        if how == 'col':
            temp = dims[0]
            dims[0] = dims[1]
            dims[1] = temp
            board = self.transpose_puzzle(board.copy())
        # do something
        new_board = []
        r = 0
        c = 0
        print("AFTER dims: " + str(dims) + ", h_hints: " + str(h_hints) + ", v_hints: " + str(v_hints))
        printA('board_used_for_cutting', board)
        reverse = False
        top_row_cut = -1
        bottom_row_cut = -1
        while r in range(dims[0]):
            sum_row = sum_ones(board[r])
            if how == 'col':
                hint_sum = sum(v_hints[r])
            else:
                hint_sum = sum(h_hints[r])
            if sum_row < hint_sum: # and 9 not in board[r]:
                print('sum_row:',sum_row,'hint_sum:',hint_sum)
                if not reverse:
                    top_row_cut = r - 1 if r >= 0 else 0
                    reverse = True
                    r = dims[0]
                else:
                    bottom_row_cut = r + 1
                    break
            r += 1
            if reverse:
                r -= 2
            print('r:',r, 'reverse', reverse)
        cut_board = board[top_row_cut + 1: bottom_row_cut]
        if how == 'col':
            board = self.transpose_puzzle(cut_board.copy())
            res_hints = v_hints[top_row_cut + 1 : bottom_row_cut]
        else:
            board = cut_board.copy()
            res_hints = h_hints[top_row_cut + 1 : bottom_row_cut]
        print('shrink_board',board)
        print('shrink_cut_board',cut_board)
        print('(top_row_cut, bottom_row_cut)',(top_row_cut, bottom_row_cut))
        return board, res_hints, (top_row_cut, bottom_row_cut)

    def vertical_hints_adjustment(self, v_hints, param_board, board, cuts):
        board = self.transpose_puzzle(board)
        param_board = self.transpose_puzzle(param_board)
        print('len(v_hints):',len(v_hints))
        print('v_hints', v_hints)
        print('len(board):',len(board))
        printA('board_transpose',board)
        print('len(param_board):',len(param_board))
        printA('param_board',param_board)
        new_v_hints = v_hints[cuts['top_row_cut']: cuts['bottom_row_cut']]
        r = 0
        c = 0
        reverse = False
        start = -1
        end = -1
        while r in range(len(param_board)):
            hints = v_hints[r]
            consec_space = 0
            colored_space = 0
            counting = True
            lst = flatten_list(param_board[r])
            print('r:',r,'board arr:',lst)
            if len(lst) == 2 and sum(hints) == 0:
                pass
                # new_v_hints.append(hints)
                # do something
            else:
                if reverse:
                    end = r + 1
                    break
                else:
                    start = r - 1
                    r = len(param_board)
                    reverse = True
            # while c in range(len(param_board[r])):
            #     pixel = param_board[r][c]
            #     if counting:
            #         if pixel == 1:
            #             start = c
            #             while pixel == 1 and c < len(param_board[r]):
            #                 c += 1
            #                 pixel = param_board[r][c]
            #             end = c
            #     else:
            #         if pixel == 0:
            #
            #     c += 1
            #     if reverse:
            #         c -= 2
            r += 1
            if reverse:
                r -= 2
            c = 0
        new_v_hints = v_hints[start + 1: end]
        top_cut = param_board[0:start]
        r = 0
        c = 0
        while r in range(len(top_cut)):
            hint = v_hints[r]
            print('hint:',hint,'top_cut[r='+str(r)+']:',':',top_cut[r])
            # while c in range(len(top_cut[r])):
            #
            #     c += 1
            r += 1
        bottom_cut = param_board[end:len(v_hints)]
        # print('new_v_hints:',new_v_hints, 'start:',start,'end:',end)
        board = self.transpose_puzzle(board)
        param_board = self.transpose_puzzle(param_board)
        return new_v_hints

    def horizontal_hints_adjustment(self, h_hints, param_board, board, cuts):
        # board = self.transpose_puzzle(board)
        # param_board = self.transpose_puzzle(param_board)
        print('len(h_hints):',len(h_hints))
        print('h_hints', h_hints)
        print('len(board):',len(board))
        printA('board',board)
        print('len(param_board):',len(param_board))
        printA('param_board',param_board)
        new_h_hints = []
        r = 0
        c = 0
        reverse = False
        start = -1
        end = -1
        while r in range(len(board)):
            hints = h_hints[r]
            consec_space = 0
            colored_space = 0
            counting = True
            lst = flatten_list(board[r])
            print('r:',r,'board arr:',lst)
            if len(lst) == 2 and sum(hints) == 0:
                continue
                # new_v_hints.append(hints)
                # do something
            else:
                if reverse:
                    end = r
                    break
                else:
                    start = r
                    r = len(board)
                    reverse = True
            # while c in range(len(param_board[r])):
            #     pixel = param_board[r][c]
            #     if counting:
            #         if pixel == 1:
            #             start = c
            #             while pixel == 1 and c < len(param_board[r]):
            #                 c += 1
            #                 pixel = param_board[r][c]
            #             end = c
            #     else:
            #         if pixel == 0:
            #
            #     c += 1
            #     if reverse:
            #         c -= 2
            r += 1
            if reverse:
                r -= 2
            c = 0
        new_h_hints = h_hints[start + 1: end]
        left_cut = param_board[0:start]
        r = 0
        c = 0
        while r in range(len(left_cut)):
            hint = h_hints[r]
            print('hint:',hint,'top_cut[r='+str(r)+']:',':',left_cut[r])
            # while c in range(len(top_cut[r])):
            #
            #     c += 1
            r += 1
        right_cut = param_board[end:len(h_hints)]
        # print('new_h_hints:',new_h_hints, 'start:',start,'end:',end)
        # board = self.transpose_puzzle(board)
        # param_board = self.transpose_puzzle(param_board)
        return new_h_hints

    def pad_shrunken_board(self, board, param_board, cuts):
        print(cuts)
        top_rows_cut = re_space(param_board[:cuts['top_row_cut'] + 1])
        bottom_rows_cut = re_space(param_board[cuts['bottom_row_cut']:])
        param_board = self.transpose_puzzle(param_board)
        left_cols_cut = re_space(param_board[:cuts['left_col_cut'] + 1])
        right_cols_cut = re_space(param_board[cuts['right_col_cut']:])
        param_board = self.transpose_puzzle(param_board)
        print('top_rows_cut:',top_rows_cut)
        print('bottom_rows_cut:',bottom_rows_cut)
        print('left_cols_cut:',left_cols_cut)
        print('right_cols_cut:',right_cols_cut)
        # for key, val in cuts.items():
        #     print('key:',key,',val:',val)

        result_board = []
        result_board += top_rows_cut
        i = len(top_rows_cut)
        # print('i:',i)
        # print('len(param_board):',len(param_board))
        # print('len(top_rows_cut):',len(top_rows_cut))
        # print('len(bottom_rows_cut):',len(bottom_rows_cut))
        while i in range(len(param_board) - len(bottom_rows_cut)):
            print('i:',i,param_board[i])
            row = board[i - len(top_rows_cut)]
            if len(row) < len(param_board[i]):
                x = (len(param_board[i]) - len(row))
                space = x // 2
                fill_space = [0 for i in range(space)]
                row_t = row.copy()
                row = fill_space.copy()
                if x == 1:
                    row += [0]
                for el in row_t:
                    row.append(el)
                row += fill_space
                print('space:',space, 'x:', x, 'fill_space:',fill_space,'row_t:',row_t,'row:',row)
            result_board += [row]
            i += 1
        result_board += bottom_rows_cut
        print('pad_shrunk_board_result', result_board)
        printA('pad_shrunk_board_result', result_board)
        return result_board

    def check_board(self, board):
        print('checking...')
        printA('board', board)
        if self.solved:
            if board == self.puzzle_board:
                print('\n\nfinished puzzle!\n\n')
                self.solved = True
                return True
        sum_pixels = sum([sum(board[i]) for i in range(len(board))])
        if self.num_pixels == sum_pixels:
            print('\n\nfinished puzzle!\n\n')
            self.solved = True
            return True
        print('\n\t-- CHECK FAILED --\nplaced: {0} out of {1}'.format(sum_pixels, self.num_pixels))
        return False

    def print_history(self, solving_history):
        spacing = '\t'
        details = False
        for key in solving_history:
            print(key)
            for key, val in solving_history[key].items():
                if details:
                    if type(val) is list:
                        printA(spacing + key + ':', val)
                    else:
                        print(spacing, key + ':', val)
                else:
                    print(spacing, key + ':', val)


    # def surround_shrunken_board(self, puzzle):
    #     n_cols = self.cols

    def adjust_board(self, board, t_board, cuts):
        printA('board_param_adjusting', board)
        printA('t_board_param_adjusting', t_board)
        res = []
        i = 0
        j = 0
        print('cuts_A',cuts['top_row_cut'])
        print('cuts_B',cuts['bottom_row_cut'])
        print('cuts_C',cuts['left_col_cut'])
        print('cuts_D',cuts['right_col_cut'])

        a = max([len(t_board[i]) for i in range(len(t_board))])
        b = len(t_board)
        r_calc = max(a, b)
        c = max([len(board[i]) for i in range(len(board))])
        d = len(board)
        c_calc = max(c, d)
        puzzle_dims = [r_calc, c_calc]
        e = (puzzle_dims[0] - min(len(t_board[0]), len(t_board)))
        row_buffer = 1 if e == 1 else e // 2
        f = (puzzle_dims[1] - min(len(board[0]), len(board)))
        col_buffer = 1 if f == 1 else f // 2
        print('puzzle_dims:', puzzle_dims,'row_buffer:',row_buffer,'col_buffer:',col_buffer,'r_calc:',r_calc,'c_calc:',c_calc)
        print('a:',a,'b:',b,'c:',c,'d:',d,'e:',e,'f:',f)

        while i in range(puzzle_dims[0]):
            if row_buffer < i <= (puzzle_dims[0] - row_buffer):
                row = []
                while j in range(puzzle_dims[1]):
                    if col_buffer < j <= (puzzle_dims[1] - col_buffer):
                        x = i - (2 * row_buffer) if i - (2 * row_buffer) >= 0 else 0
                        y = j - (2 * col_buffer) if j - (2 * col_buffer) >= 0 else 0
                        print('\ti:',i,'j:',j,'x:',x,',y:',y)
                        # x += cuts['top_row_cut']
                        # y += cuts['left_col_cut']
                        # print('upgraded: x:',x,', y:',y)
                        row.append(max(board[x][y], t_board[x][y]))
                    j += 1
                j = 0
                print('\t\ti:',i,', j:',j,', row:',row)
                res.append(row)
            i += 1
        printA('row_combined_shrunk:',res)
        return res
        # while i in range(max(len(board), len(t_board))):
        #     j = 0
        #     row = []
        #     while j in range(max_array_rows(board, t_board, i)):
        #         if i in range(len(board)):
        #             if i in range(len(t_board)):
        #                 if j in range(len(board[i])):
        #                     if j in range(len(t_board[i])):
        #                         if board[i][j] != 9 and t_board[i][j] != 9:
        #                             row.append(max(board[i][j], t_board[i][j]))
        #                     else:
        #                         if board[i][j] != 9:
        #                             row.append(board[i][j])
        #                 else:
        #                     if t_board[i][j] != 9:
        #                         row.append(t_board[i][j])
        #             else:
        #                 if board[i][j] != 9:
        #                     row.append(board[i][j])
        #         else:
        #             if t_board[i][j] != 9:
        #                 row.append(t_board[i][j])
        #         j += 1
        #     i += 1
        #     res.append(row)


# def sum_rest_lst(lst, val):
#     res = 0
#     for i in range(len(lst)):
#         if lst[i] != val:
#             res += lst[i]
#     return res


def puzzleify(list_of_puzzles):
    new_list = {}
    for puzzle in list_of_puzzles:
        # print('a:',puzzle,'b',list_of_puzzles[puzzle][1],'c:',list_of_puzzles[puzzle][2])
        # print('list_of_puzzles', list_of_puzzles)
        if len(list_of_puzzles[puzzle]) == 4:
            print('list_of_puzzles', list_of_puzzles)
            temp = Puzzle(puzzle, list_of_puzzles[puzzle][1], list_of_puzzles[puzzle][2], list_of_puzzles[puzzle][3])
        else:
            temp = Puzzle(puzzle, list_of_puzzles[puzzle][1], list_of_puzzles[puzzle][2])
        print(temp)
        print('\n---------------------------------------------------------------------------------------------------------\n\n')
        new_list[temp.get_name()] = temp
    return new_list


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


def printA(name='arrIn', arr=None):
    if arr is None or len(arr) <= 1:
        arr = [[]]
        print('nothing given to print {', name, ' : ', arr, '}')
        return
    string = name + '\n\t    '
    for i in range(len(arr[0])):
        b = (i + 1) % 5
        if i > 0 and i % 5 == 0:
            string += ' ' + str((i + 1) // 5)
        else:
            string += ' '
    string += '\n['
    for i in range(len(arr)):
        in_string = '\t' + str(i) + ':\t['
        for j in range(len(arr[i])):
            if j < len(arr[i]) - 1:
                in_string += str(arr[i][j])  # + ', '
            else:
                in_string += str(arr[i][j])
            if j > 0 and (j + 1) % 5 == 0:
                in_string += '|'
        if i < len(arr) - 1:
            in_string += '],\n'
        else:
            in_string += ']'
        string += in_string
    string += ']\n'
    print(string)


def truthy_list(lst):
    if type(lst) == list and len(lst) > 0:
        b = 0
        for el in lst:
            # print('el',el, 'lst', lst)
            if type(el) != list:
                return False
            if len(el) > b:
                b = len(el)
            for val in el:
                if type(val) != int:
                    return False
        return True and b != 0
    return False


def sum_ones(arr):
    curr_sum = 0
    for el in arr:
        if el != 9:
            curr_sum += el
    return curr_sum


def flatten_list(arr):
    new_arr = []
    colored = 0
    spaces = 0
    i = 0
    # print('arr:', arr)
    while i in range(len(arr)):
        if arr[i] == 1:
            if colored == 0:
                if i == 0:
                    new_arr.append(1)
                else:
                    new_arr.append(spaces)
                spaces = 0
            colored += 1
        elif arr[i] == 0:
            if spaces == 0:
                if i == 0:
                    new_arr.append(0)
                else:
                    new_arr.append(colored)
                colored = 0
            spaces += 1
        i += 1
    new_arr.append(max(spaces, colored))
    # print('colored:', colored, 'spaces', spaces)
    return new_arr


def re_space(arr):
    new_arr = []
    # print('re_space(arr):',arr)
    for lst in arr:
        i = 0
        temp = []
        while i in range(len(lst)):
            if lst[i] == 9:
                temp.append(0)
            else:
                temp.append(lst[i])
            i += 1
        new_arr.append(temp)
    return new_arr

def max_array_rows(board, t_board, index):
    if index in range(len(board)):
        if index in range(len(t_board)):
            return max(len(board[index]), len(t_board[index]))
        return len(board[index])
    return len(t_board[index])






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

# sample_smiley_puzzle = Puzzle('sample_smiley', 0, sample_smiley)