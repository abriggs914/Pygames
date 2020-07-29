
    #     r = 0
    #     c = 0
    #     while r in range(len(h_hints)):
    #         row_hint = h_hints[r]
    #         curr_puzzle_row = board[r]
    #         row_spaces = self.determine_row_spaces(board[r])
    #         num_row_pixels = self.count_num_pixels(row_hint)
    #         num_row_occupied = num_row_pixels + len(row_hint) - 1
    #         row_hint_tracker = 0
    #         for hint in row_hint:
    #             col_index = 0
    #             for space in row_spaces:
    #                 diff = space - num_row_occupied
    #                 print('r:',r,', hint:',hint,', space:',space, ', num_row_p', num_row_pixels, ', num_row_occ:', num_row_occupied,', diff',diff, ', row_hint_tracker:',row_hint_tracker)
    #                 if hint > diff:
    #                     temp_row = self.sim_row_horizontal_filling(curr_puzzle_row, row_hint, hint, row_hint_tracker, n_cols)
    #                     temp_row_row = temp_row[0]
    #                     temp_row_sum_left = 0 if temp_row[1] == 0 else temp_row[1] + 1
    #                     temp_row_sum_right = 0 if temp_row[2] == 0 else temp_row[2] + 1
    #                     buffer = self.determine_row_spaces(temp_row_row)
    #                     check_var = buffer[0] - hint
    #                     offset_space = 0 if check_var <= 0 else check_var  # (buffer[0] - 1) - hint  #+ temp_row_sum_left + temp_row_sum_right - hint
    #                     space_to_fill = (hint - (space - num_row_pixels)) // 2
    #                     # index = col_index + buffer[0]
    #                     i = 0
    #                     print('\tbuffer',buffer,'temp_row', temp_row, 'col_index', col_index, 'offset_space', offset_space)
    #                     low_bound = -1
    #                     up_bound = -1
    #                     while i in range(len(temp_row_row)):
    #                         if ((buffer[0] - len(row_hint) - 1) // 2) <= (hint - 1):
    #                             low_bound = temp_row_sum_left + offset_space
    #                             x = (temp_row_sum_right + offset_space)
    #                             up_bound = (n_cols - x)
    #                             if low_bound <= i < up_bound:
    #                                 print('\t\tfilling i:', i)
    #                                 board[r][i] = 1
    #                                 print('\t\tlow_bound:',low_bound, ', up_bound:',up_bound, ', board[r]:',board[r])
    #                         i += 1
    #                     # if low_bound > -1 and up_bound > -1:
    #
    #             row_hint_tracker += 1
    #                     # if col_index < n_cols - 2:
    #                     #     board[r][col_index + buffer[0]] = 9
    #                     #
    #         row_hint_tracker = 0
    #         r += 1
    #         # print('\nrow:', r, 'row_hint:', row_hint, ',row_spaces', row_spaces, ',num_row_pixels', num_row_pixels,
    #         #       ',num_row_occupied:', num_row_occupied)
    #         # if num_row_occupied > (n_cols // 2):
    #         #     for i in range(len(row_hint)):
    #         #         hint = row_hint[i]
    #         #         if 0 < r < len(row_hint) - 1:
    #         #             hint += 2
    #         #         left_over = num_row_occupied - hint
    #         #         print('fitting hint:', hint, ',left_over:', left_over)
    #         #         c_index = 0
    #         #         for space in row_spaces:
    #         #             offset = 0 if space % 2 == 0 else 1
    #         #             offset += ((space - 1) // 2) - 1
    #         #             rest_of_row = self.rest_hint_vals(row_hint, hint)
    #         #             print('space:', space, ',c_index', c_index, ',offset:',offset, 'rest_row:', rest_of_row)
    #         #             rest_of_row = self.rest_hint_vals(row_hint, hint)
    #         #             if left_over <= (space - rest_of_row) and hint > offset:
    #         #                 index = c_index + (space // 2)
    #         #                 space_to_fill = (index - offset, index + offset)
    #         #                 print('\tindex', index, 'space_to_fill:' ,space_to_fill)
    #         #                 board[r][index] = 1
    #         #                 if space % 2 == 0:
    #         #                     board[r][index - 1] = 1
    #         #             if 0 < c_index < n_cols:
    #         #                 c_index += 2
    #         #             c_index += space
    #         #         temp = hint // 2
    #         # r += 1
    #
    #         # row_spaces = self.determine_row_spaces(board[r])
    #         # num_row_pixels = self.count_num_pixels(row_hint)
    #         # num_row_occupied = num_row_pixels + len(row_hint) - 1
    #         # print('row:', r, 'row_hint:', row_hint, ',row_spaces', row_spaces, ',num_row_pixels',num_row_pixels, ',num_row_occupied:', num_row_occupied)
    #
    #     # while r in range(n_rows):
    #     #     row_spaces = self.determine_row_spaces(board[r])
    #     #     num_row_pixels = self.count_num_pixels(h_hints[r])
    #     #     num_row_occupied = num_row_pixels + len(h_hints[r]) - 1
    #     #     print('\tnum_row_pixels',num_row_pixels, ',num_row_occupied:', num_row_occupied)
    #     #     print('\trow_spaces', row_spaces)
    #     #     for space in row_spaces:
    #     #         col_tracker = 0
    #     #         for val in h_hints[r]:
    #     #             added_one = False
    #     #             if col_tracker > 0 and col_tracker < len(h_hints[r]) - 1:
    #     #                 val += 2
    #     #                 added_one = True
    #     #                 if len(h_hints[r]) < 3:
    #     #                     val -= 1
    #     #                     added_one = False
    #     #                 #space -= 2
    #     #             # if 0 < val < len(h_hints[r]) - 1:
    #     #             #     val += 2
    #     #             row_space_without_val = num_row_occupied - val
    #     #             print('row_space_without_val',row_space_without_val)
    #     #             diff = space - val
    #     #             buffer = 0
    #     #             if added_one:
    #     #                 if diff % 2 == 1:
    #     #                     diff += 1
    #     #                 buffer = diff
    #     #             #else:
    #     #
    #     #             # print('row_spaces', row_spaces, ',r', r, ',col_tracker', col_tracker, ',space:', space, ',val:', val, ',diff:', diff, 'buffer', buffer, ',h_hints[r]',
    #     #             #       h_hints[r])
    #     #             #if 0 <= x < y:
    #     #             if diff < val:
    #     #                 # space = n_cols - sum_rest_lst(h_hints[r], val)
    #     #                 mid_space_index = space // 2
    #     #                 if space % 2 == 0:
    #     #                     mid_space_index -= 1
    #     #                 buffer = mid_space_index - (diff - 1 if diff > 0 else 0)
    #     #                 print('color in space,', 'mid_space_index', mid_space_index, 'buffer:', buffer)
    #     #                 print('row_spaces', row_spaces, ',r', r, ',col_tracker', col_tracker, ',space:', space, ',val:', val, ',diff:', diff, 'buffer', buffer, ',h_hints[r]',h_hints[r])
    #     #                 # divide col_tracker /2
    #     #                 board[r][mid_space_index] = 1
    #     #                 count = 1
    #     #                 while buffer > 1:
    #     #                     if buffer < 3:
    #     #                         # print('mid_space_index - buffer', mid_space_index - buffer)
    #     #                         board[r][mid_space_index - buffer] = 9
    #     #                     # elif buffer <= 2:
    #     #                     # print('mid_space_index + buffer', mid_space_index + buffer)
    #     #                     # print('mid_space_index - buffer', mid_space_index - buffer)
    #     #                     board[r][mid_space_index + buffer] = 9
    #     #                     board[r][mid_space_index - buffer] = 9
    #     #                     buffer -= 1
    #     #                     count += 1
    #     #             col_tracker += 1
    #     #
    #     #     r += 1
    #
    #     # while c in range(c_cols):
    #     printA('board:', board)
    #     return 1
    #
    # def look_horizontal(self):
    #     pass
    #
    # def determine_row_spaces(self, row):
    #     res = []
    #     curr_count = 0
    #     for el in range(len(row)):
    #         # print('row[el]:',row[el])
    #         if row[el] == 0:
    #             curr_count += 1
    #         else:
    #             if curr_count > 0:
    #                 res.append(curr_count)
    #             curr_count = 0
    #     res.append(curr_count)
    #     if len(res) > 1 and res[-1] == 0:
    #         res.pop()
    #     return res
    #
    # def rest_hint_vals(self, row, hint):
    #     res = 0
    #     seen = False
    #     for i in range(len(row)):
    #         if 0 < i < len(row) - 1:
    #             res += 1
    #         if row[i] != hint or seen:
    #             res += row[i]
    #         else:
    #             seen = True
    #     return res
    #
    # def get_name(self):
    #     return self.name

    # def sim_row_horizontal_filling(self, puzzle_row, row_hint, hint, index, orig_cols):
    #     orig_puzzle = puzzle_row
    #     puzzle_row, counted = self.row_trim(puzzle_row)
    #     print('trim_row:',puzzle_row,', counted:', counted)
    #     n_cols = len(puzzle_row)
    #     x = n_cols - counted
    #     if x < 0:
    #         x = 0
    #     new_row = [1 if puzzle_row[i] == 1 else 0 for i in range(x)]
    #     i = 0
    #     mid_index = n_cols // 2
    #     hint_space = hint // 2
    #     offset = 0 if n_cols % 2 == 0 else 1
    #     bounds = [i for i in range((mid_index - hint_space), (mid_index + hint_space + offset))]
    #     sum_left = 0
    #     sum_right = 0
    #     left_side = []
    #     right_side = []
    #     if len(row_hint) == 1 or counted >= len(puzzle_row):
    #         return (new_row, sum_left, sum_right)
    #     elif len(row_hint) == 2:
    #         order_placement = row_hint[index]  #row_hint.index(hint)
    #         other_index = 1 if index == 0 else 0
    #         print('order_placement',order_placement,'other_index',other_index)
    #         other_hint = row_hint[other_index]
    #         size = len(new_row)
    #         if index < other_index:
    #             right_side = [row_hint[1]]
    #             sum_right = row_hint[1] + 1
    #         else:
    #             left_side = [row_hint[0]]
    #             sum_left = row_hint[0] + 1
    #         # sum_left = 0 if index < other_index else row_hint[0]
    #         # sum_right = row_hint[1] if index < other_index else 0
    #         if n_cols != orig_cols:
    #             i = orig_cols - n_cols + 1
    #             if i < 0:
    #                 i = 0
    #         while i in range(size):
    #             if order_placement > other_index:
    #                 if n_cols - i - 1 <= other_hint:
    #                     new_row[i] = -2
    #             else:
    #                 if i < other_hint:
    #                     new_row[i] = -3
    #             i += 1
    #     else:
    #         order_placement = row_hint.index(hint)
    #         left_side = row_hint[:order_placement]
    #         right_side = row_hint[order_placement + 1:]
    #         sum_left = self.rest_hint_vals(left_side, 0)
    #         sum_right = self.rest_hint_vals(right_side, 0)
    #         size = len(new_row)
    #         if n_cols != orig_cols:
    #             i = orig_cols - n_cols
    #             if i < 0:
    #                 i = 0
    #         while i in range(size):
    #             if sum_left > 0 and i <= sum_left:
    #                 new_row[i] = -4
    #             elif sum_right > 0 and (n_cols - i - 1) <= sum_right:
    #                 print('i',i)
    #                 new_row[i] = -5
    #             i += 1
    #     print('row_hint:',row_hint,', left_side:',left_side,', sum_left:',sum_left,', right_side:',right_side,', sum_right:',sum_right)
    #     print('new_row', new_row)
    #     if n_cols != orig_cols:
    #         new_row = orig_puzzle[:len(new_row) + 1] + new_row
    #     res = (new_row, sum_left, sum_right)
    #     return res

    # def row_trim(self, puzzle_row):
    #     print('puzzle_row:', puzzle_row)
    #     temp = []
    #     i = 0
    #     while i in range(len(puzzle_row)):
    #         if puzzle_row[i] == 1:
    #             i += 1
    #             print('\n\n\n\n\n\n\n\n\n\nn\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    #             continue
    #         else:
    #             return puzzle_row[i:], i + (0 if i == 0 else 2)
    #     return puzzle_row, i  #  + (0 if i == 0 else 2)