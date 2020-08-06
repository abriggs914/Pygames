import numpy as np
from sys import maxsize


def combine_rows(row_1, row_2):
	for i in range(min(len(row_1), len(row_2))):
		if row_2[i] == 1:
			row_1[i] = row_2[i]
	return row_1
	
# r_1 = [0,1,0,1,1,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0]
# r_2 = [1,1,1,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,0,1,0]

# print(combine_rows(r_1, r_2))

def shrink_hints(chunk, hints_in, top_left):
	idx = 0 if top_left else -1
	
	for r, row in enumerate(chunk):
		for c, val in enumerate(row):
			if val == 1:
				# print("r:", r, "c:", c, "val:", val, "row:", row, "hints_in[c]", hints_in[c])
				hints_in[c][idx] -= 1
				if hints_in[c][idx] == 0:
					hints_in[c].remove(0)
	
def deep_copy(arr):
	return [r.copy() if type(r) is list else r for r in arr]
	
def closest_rows(lst):
	i, j = 0, 1
	while j < len(lst) - 1:
		diff = abs(lst[i] - lst[j])
		if diff != 1:
			break
		i += 1
		j += 1
	print("closest: (", i, ",", j, "):", lst[i], ",", lst[j])
	# min_v = maxsize
	# min_i = (0, 0)
	# rev_lst = lst.copy()
	# rev_lst.reverse()
	# for i, v_low in enumerate(lst):
		# for j, v_high in enumerate(rev_lst):
			# diff = abs(v_high - v_low)
			# if diff < min_v:
				# min_v = diff
				# min_i = (v_low, v_high)
	# print("min_v:", min_v, "min_i:", min_i)
	

def cut_puzzle(solved_puzzle, h_hints_in, v_hints_in, top_cut, bottom_cut, left_cut, right_cut):
	# print("Cut puzzle: top[",top_cut,"], bottom[",bottom_cut,"], left[",left_cut,"], right[",right_cut,"]")
	# Copy the parameter lists to avoid modification
	solved_puzzle = deep_copy(solved_puzzle)
	h_hints_in = deep_copy(h_hints_in)
	v_hints_in = deep_copy(v_hints_in)
	
	top_chunk = solved_puzzle[:top_cut + 1]
	bottom_chunk = solved_puzzle[bottom_cut:]
	left_chunk = [row[:left_cut + 1] for row in solved_puzzle]
	right_chunk = [row[right_cut:] for row in solved_puzzle]
	# print("\n\ttop_chunk:\n", top_chunk)
	# print("\n\tbottom_chunk:\n", bottom_chunk)
	# print("\n\tleft_chunk:\n", left_chunk)
	# print("\n\tright_chunk:\n", right_chunk)
	
	shrink_hints(top_chunk, v_hints_in, True)
	shrink_hints(bottom_chunk, v_hints_in, False)
	
	left_chunk = np.transpose(left_chunk)
	right_chunk = np.transpose(right_chunk)
	h_hints_in = np.transpose(np.array(h_hints_in, dtype=object))  # non-uniform size lists as ndarrays is deprecated 
	
	shrink_hints(left_chunk, h_hints_in, True)
	shrink_hints(right_chunk, h_hints_in, False)
	h_hints_in = h_hints_in.tolist()
	
	h_hints_in = h_hints_in[top_cut + 1: bottom_cut]
	v_hints_in = v_hints_in[left_cut + 1: right_cut]
				
	return [row[left_cut + 1: right_cut].copy() for row in solved_puzzle[top_cut + 1: bottom_cut]], h_hints_in, v_hints_in
	
puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]
				 

v_hints = [[], [5], [1,2], [1,2], [1,2,1,1], [1,2,2,1], [1,2,2,1], [1,2,1], [1,2,1], [1,2,1], [1,2,2,1], [1,2,2,1], [1,2,2,1], [1,2], [1,2], [5], []]
h_hints = [[], [11], [1,1], [1,3,3,1], [1,3,3,1], [1,1], [1,9,1], [2,7,2], [2,2], [11]]
top_cut = 1
bottom_cut = len(h_hints) - 4
left_cut = 1
right_cut = len(v_hints) - 2
print("\n\tCut puzzle:\n", cut_puzzle(puzzle, h_hints, v_hints, top_cut, bottom_cut, left_cut, right_cut))