hints = [1,5,1]
a = [0,0,0,0,0,0,0,0,0,0]
b = [0,1,0,0,0,0,0,0,0,0]
c = [0,1,0,1,1,1,1,1,0,0]
d = [0,1,0,1,1,1,1,1,0,1]
e = [1,0,1,1,1,1,1,0,1,0]

def space():
    return [0 for i in range(20)]
    
hints_2 = [6,6,6]

def len_hints(arr):
    return sum(arr) + len(arr) - 1
    
def how_many_counted(arr):
    seen = False
    blanks = 0
    for el in arr:
        if el == 0:
            if not seen:
                blanks += 1
        else:
            if not seen:
                blanks += 1
            seen = True
    # print('returning blanks:',blanks)
    return blanks
    
def usable_space(space):
    res = []
    space_sum = sum(space)
    if space_sum == 0:
        return space, space_sum
    i = len(space) - 1
    while i in range(len(space)):
        if space[i] == 1:
            i += 1
            break
        i -= 1
    if i >= 0:
        i += 1
    space_sum += how_many_counted(space[:i + 1])
    # print('returning i:',i)
    # print(space[i:])
    return space[i:], space_sum
        
    
def calc_diff(arr, space, index):
    length = len(arr)
    if length <= index:
        # print('already finished!')
        return -1
    print('fitting ' + str(arr) + ' into ' + str(space) + ' starting at ' + str(arr[index]))
    new_space, space_to_remove = usable_space(space)
    spaces_len = len(new_space)
    v = (sum(arr[:index]))
    # print('v',v)
    covered_space = sum(space)
    to_be_covered = sum(arr)
    space_left_to_cover = len_hints(arr[index:])
    arr_len = space_left_to_cover
    if covered_space == to_be_covered:
        # print('base')
        return -1
    # print('new_space',new_space)
    # print('space_to_remove',space_to_remove)
    # print('spaces_len',spaces_len)
    # print('arr_len',arr_len)
    return spaces_len - arr_len
    
def calc_buffer_size(arr, space, index):
    pass

hints_length = len_hints(hints)
# print(hints_length)

print('a_diff:', calc_diff(hints, a, 0) == 1)
# print('\n')
print('b_diff:', calc_diff(hints, b, 1) == 0)
# print('\n')
print('c_diff:', calc_diff(hints, c, 2) == 0)
# print('\n')
print('d_diff:', calc_diff(hints, d, 2) == -1)
# print('\n')
print('e_diff:', calc_diff(hints, e, 3) == -1)
# print('\n')
print('large_diff:', calc_diff(hints_2, space(), 0) == 0)
# print('\n')
print('large_diff:', calc_diff([18], space(), 0) == 2)
# print('\n')
print('large_diff:', calc_diff([5,5,5], space(), 0) == 3)
# print('\n')

ten_ones = [1 for i in range(10)]
print('large_diff:', calc_diff([10,4,4], (ten_ones + space()[:-10]), 1) == 0)

def fill_row(row, hints, index, buff):
    hint = hints[index]
    new_row = row#.copy()
    left_hints = hints[:index]
    right_hints = hints[index:]
    left_space = len_hints(left_hints) + 1
    right_space = len_hints(right_hints)
    left_puzzle_sum = sum(row[:left_space])
    if left_puzzle_sum == 0:
        buff -= left_space
    # right_puzzle_sum = sum(row[right_space:])
    # print('left_hints:',left_hints,' right_hints:',right_hints,' left_space:',left_space,' right_space:', right_space,' buff:',buff)
    i = 0
    while i in range(len(new_row)):
        #print(new_row[i])
        left = left_space + buff
        right = (len(new_row) - (right_space + buff)) + hint
        # print('left:',left,' right',right)
        if hint > 0 and hint > buff:
            if i >= left and i < right: # or ((i) == left == right == buff):
                new_row[i] = 1
        i += 1
    # print('new_row:',new_row)
    return new_row

def horizontal_row_fill(puzzle_row, hints):
    i = 0
    temp_row = puzzle_row.copy()
    while i in range(len(hints)):
        buffer_space = calc_diff(hints, puzzle_row, i)
        # print('buffer_space:',buffer_space)
        temp_row = fill_row(puzzle_row, hints, i, buffer_space)
        
        i += 1
        # if i == len(hints):
        #     return temp_row
    return temp_row
    
def ten_space():
    return [0 for i in range(10)]
print()
print(horizontal_row_fill(space(), hints_2) == [1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1])
print(horizontal_row_fill(space(), [5,5,5]) == [0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0])
print(horizontal_row_fill(space(), [18]) == [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0])
print(horizontal_row_fill(ten_space(), hints) == [0,0,0,1,1,1,1,0,0,0])
print(horizontal_row_fill(ten_space(), [1]) == ten_space())
print(horizontal_row_fill(ten_space(), [6]) == [0,0,0,0,1,1,0,0,0,0])
print(horizontal_row_fill(ten_space(), [4,5]) == [1,1,1,1,0,1,1,1,1,1])
print(horizontal_row_fill(ten_space(), [7]) == [0,0,0,1,1,1,1,0,0,0])

sample_smiley = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                 [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]
sample_smiley_h_hints = [[0],[11],[1,1],[1,3,3,1],[1,3,3,1],[1,1],[1,9,1],[1,7,1],[2,2],[11]]
                 
count_index = 0
new_puzzle = [[0 for i in range(17)] for j in range(len(sample_smiley_h_hints))]
while count_index in range(len(sample_smiley_h_hints)):
    new_puzzle[count_index] = horizontal_row_fill(new_puzzle[count_index], sample_smiley_h_hints[count_index])
    count_index += 1
print(new_puzzle)

def printA(arr):
    for row in arr:
        print(row)
printA(new_puzzle)
    
    