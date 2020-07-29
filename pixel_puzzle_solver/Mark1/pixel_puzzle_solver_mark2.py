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
    
def transpose_puzzle(board):
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
        

def space(n):
    n = n if 5 <= n <=100 else 5
    return [0 for i in range(n)]
    
hint_1 = [4,7,4]
hint_2 = [1]
hint_3 = [6,6,6]
hint_4 = [6, 11]

def len_hints(hints):
    return sum(hints) + len(hints) - 1
    
def gen_rest_possibilities(space, hints, delta):
    if delta < 1:
        return []
    else:
        res = []
        i = 1
        while (i - 1) in range(delta):
            temp = space[-i:] + space[0: len(space) - i]
            print('temp:\t', temp)
            i += 1
            res.append(temp)
        # printA('res',res)
        return res
        
def space_hints(space, hints):
    if len_hints(hints) > len(space):
        print('hint size is too large')
        return
    else:
        curr_space_index = 0
        last_space_index = curr_space_index
        delta = len(space) - len_hints(hints)
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
        print('space:\t', space)
        res += gen_rest_possibilities(space, hints, delta)
        # res += [rev]
        # print('rev:\t', rev)
        return res
        
def guess_row(space, hints):
    print('Fitting', hints, 'into space size', len(space), ',', space)
    rows = space_hints(space, hints)
    # print('rows:', rows)
    delta = len(space) - len_hints(hints)
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
    print('res:\t',res)
    return res
    
print('\n  =>\t',guess_row(space(20), hint_1))
print('\n  =>\t',guess_row(space(20), hint_2))
print('\n  =>\t',guess_row(space(20), hint_3))
print('\n  =>\t',guess_row(space(20), hint_4))
print('\n  =>\t',guess_row(space(25), hint_3))
print('\n  =>\t',guess_row(space(20), [18,1]))

def guess_puzzle(puzzle_in):
    puzzle_name = puzzle_in[0]
    puzzle_id = puzzle_in[1]
    puzzle_h_hints = puzzle_in[2]
    puzzle_v_hints = puzzle_in[3]
    board = [[0 for i in range(len(puzzle_v_hints))] for j in range(len(puzzle_h_hints))]
    guessed_h_rows = [guess_row(space(len(puzzle_v_hints)), row_hints) for row_hints in puzzle_h_hints]
    printA('guessed_h_rows:', guessed_h_rows)
    guessed_v_rows = [guess_row(space(len(puzzle_h_hints)), row_hints) for row_hints in puzzle_v_hints]
    # printA('guessed_v_rows:', guessed_v_rows)
    guessed_v_rows = transpose_puzzle(guessed_v_rows)
    printA('guessed_v_rows:', guessed_v_rows)
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

puzzle_15 = ['puzzle_15', 15, \
            [[25], [12, 12], [11, 11], [10, 1, 10], [9, 2, 9], [8, 3, 8], [7, 4, 7], [6, 6, 6], [5, 8, 5], [4, 10, 4], [3, 12, 3], [2, 14, 2], [1, 16, 1], [18], [25]],
            [[13, 1], [12, 1], [11, 1], [10, 1], [9, 1], [8, 2], [7, 3], [6, 4], [5, 5], [4, 6], [3, 7], [2, 8], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7], [7, 6], [8, 5], [9, 4], [10, 3], [11, 2], [12, 1], [13, 1]]]
puzzle_15_answer = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                              [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
                              [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                              [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
print('\n\n\n\n\n\n\n')
soln = guess_puzzle(puzzle_15)
printA('guessing star shape puzzle', soln)
print('\n\tCheck:', puzzle_15_answer == soln)

mushroom_puzzle_v_hints = [[8], [6, 4], [1, 3, 6], [1, 6, 4], [1, 15], [7, 9], [6, 10], [6, 5, 2], [6, 3, 2],
                           [1, 4, 3, 1], [2, 3, 3, 1], [7, 4, 1], [1, 12, 1], [1, 10, 1], [1, 11, 2], [1, 2, 8, 1],
                           [1, 2, 2, 6], [3, 2, 3], [2, 5], [7]]
mushroom_puzzle_h_hints = [[11], [6, 2, 1], [2, 5, 1, 1], [1, 10, 3], [2, 16], [16, 1], [6, 4, 1], [5, 3, 1],
                           [1, 2, 4, 1], [2, 1, 8], [2, 3, 9], [16, 2], [18], [17], [6, 1, 4], [4, 2], [3, 1], [3, 1],
                           [4, 2], [9]]
sample_mushroom_puzzle = ['sample_mushroom_puzzle', 14, mushroom_puzzle_h_hints, mushroom_puzzle_v_hints]

soln = guess_puzzle(sample_mushroom_puzzle)
printA('guessing sample_mushroom_puzzle', soln)

puzzle14 = ['pirate flag', 14, \
            [[1, 14, 1], [5, 4], [3, 2], [2, 1, 2], [3, 3], [4, 4], [5, 1, 1, 4], [5, 3, 3, 4], [5, 4], [5, 1, 4],
             [6, 5], [7, 6], [9, 1, 8], [5, 5, 4], [4, 1, 1, 1, 1, 1, 3], [3, 1, 1, 2], [11], [1, 13],
             [2, 13, 1], [2, 13, 1]], \
            [[1, 13, 3], [13, 2], [12], [2, 10], [3, 8, 3], [4, 3, 4], [3, 1, 2, 6], [2, 2, 1, 4], [1, 1, 3, 4],
             [1, 1, 4], [1, 1, 3, 4], [1, 1, 4], [1, 1, 3, 4], [2, 2, 1, 4], [3, 1, 2, 6], [3, 3, 4], [3, 9, 3], [11],
             [13], [1, 13, 2]]]

soln = guess_puzzle(puzzle14)
printA('guessing pirate_flag_puzzle', soln)

p = input('hey type something')