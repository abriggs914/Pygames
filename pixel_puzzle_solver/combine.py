import itertools
import math
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
	# print("chunk:")
	# print_puzzle(chunk)
	# print("hints_in:")
	# print_puzzle(hints_in)
	# print("\nchunk:", chunk, "hints_in:", hints_in)
	for r, row in enumerate(chunk):
		# print("\tr: " + str(r) + " row: " + str(row))
		skipped = []
		for c, val in enumerate(row):
			if val == 1:
				# msg = "\t\tc: " + str(c) + " idx: " + str(idx) + " val: " + str(val) + " hints_in[c]: " + str(hints_in[c])
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
	
	
def cut_visual(*args):
	puzzle, tc, bc, lc, rc = args
	if not puzzle:
		print("No puzzle given")
		return
	rows = len(puzzle)
	cols = len(puzzle[0])
	border = "\t\t" + "".join(["_" for i in range(cols + 4)])
	result = "\n\t\t\tCut visual\n\n"
	for r, row in enumerate(puzzle):
		left = row[:lc + 1]
		right = row[rc:]
		row_str = "".join(str(c) for c in left) + " |" + "".join(str(c) for c in row[lc + 1: rc]) + "| " + "".join(str(c) for c in right)
		if r == tc + 1 or r == bc:
			result += border + "\n"
		result += "\t\t" + row_str + "\n"
	print(result)
		
	
# Takes a puzzle, it's corresponding h_hints and v_hints, and indices for cutting.
# Returns a newly sized puzzle, new h_hints, new v_hints, and all cut chunks of the
# puzzle in (top, bottom, left, right) order.
# All cuts are made exclusively at the given indices.
def cut_puzzle(solved_puzzle, h_hints_in, v_hints_in, top_cut, bottom_cut, left_cut, right_cut):
	# print("cut solved_puzzle:", solved_puzzle)
	bottom_cut = top_cut + 1 if top_cut == bottom_cut else bottom_cut
	right_cut = left_cut + 1 if left_cut == right_cut else right_cut
	print("Cut puzzle: top[", top_cut, "], bottom[", bottom_cut, "], left[", left_cut, "], right[", right_cut, "]")
	cut_visual(solved_puzzle, top_cut, bottom_cut, left_cut, right_cut)
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
	
	shrink_hints(top_chunk, v_hints_in, True)
	shrink_hints(bottom_chunk, v_hints_in, False)
	
	left_chunk = np.transpose(left_chunk).tolist()
	right_chunk = np.transpose(right_chunk).tolist()
	h_hints_in = np.transpose(np.array(h_hints_in, dtype=object)).tolist()  # non-uniform size lists as ndarrays is deprecated 
	
	shrink_hints(left_chunk, h_hints_in, True)
	shrink_hints(right_chunk, h_hints_in, False)
	
	h_hints_in = h_hints_in[top_cut + 1: bottom_cut]
	v_hints_in = v_hints_in[left_cut + 1: right_cut]
	
	return new_puzzle, h_hints_in, v_hints_in, (top_chunk, bottom_chunk, left_chunk, right_chunk)
	

def pad_puzzle(puzzle, chunks):
	top_chunk, bottom_chunk, left_chunk, right_chunk = chunks
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
	print("\n\tBEFORE PADDING")
	print_puzzle(puzzle)
	puzzle = top_chunk + puzzle + bottom_chunk
	for r in range(len(puzzle)):
		if len(top_chunk) <= r < (len(puzzle) - len(bottom_chunk)):
			left = [row[r] for row in left_chunk]
			right = [row[r] for row in right_chunk]
			puzzle[r] = left + puzzle[r] + right
	print("\n\tAFTER PADDING")
	print_puzzle(puzzle)
	return puzzle
	
	
def print_puzzle(puzzle):
	if puzzle:
		print("     " + "".join(list(map(lambda x: str(x).rjust(3, " "), [i for i in range(len(puzzle[0]))]))))
		print("".join(["_" for i in range(4 + (3 * len(puzzle[0])))]))
		for i, r in enumerate(puzzle):
			print(str(i).rjust(2, " "), "|", "".join(list(map(lambda x: (" " if x == "1" else x).rjust(3, " "), map(str, r)))))
	else:
		print("Puzzle is empty")


def greatest_diff(lst):
	if not lst:
		return None, None
	i, j = 0, 1
	max_idxs = (0, 0)
	max_diff = float("-inf")
	while j < len(lst):
		diff = abs(lst[i] - lst[j])
		# print("diff", diff, "max_diff:", max_diff)
		if diff > max_diff:
			max_diff = diff
			max_idxs = (i, j)
		i += 1
		j += 1
	return lst[max_idxs[0]], lst[max_idxs[1]]
	
	
def remaining_list(lst, size):
	left_over = []
	for i in range(size):
		if lst and i not in lst:
			left_over.append(i)
	return left_over
	
	
def outside_indices(lst, size):
	if not lst:
		return None, None
	left_over = remaining_list(lst, size)
	return max(0, left_over[0] - 1), min(size, left_over[-1] + 1)

# needs some attention
def remaining_spaces(solved_puzzle):
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

# count elements in a ndarray from the numpy library
def np_count(arr, val):
    unique, counts = np.unique(arr, return_counts=True)
    values = dict(zip(unique, counts))
    return values[val] if val in values else 0

	
# Take h_hints and v_hints to a puzzle and invert them
def invert_puzzle(puzzle):
	inverted = []
	for r, row in enumerate(puzzle):
		flipped = [0 if x != 0 else 1 for x in row]
		inverted.append(flipped)
	return inverted
	
	
def check_puzzle_is_solved(puzzle, h_hints, v_hints):
	total_to_be_colored = sum([sum(row) for row in h_hints])
	total_colored = sum([np_count(row, 1) for row in puzzle])
	calc_h_hints = count_hints(puzzle)
	puzzle = np.transpose(puzzle)
	calc_v_hints = count_hints(puzzle)
	puzzle = np.transpose(puzzle)
	print("total_colored:", total_colored)
	print("total_to_be_colored:", total_to_be_colored)
	print("calc_h_hints", calc_h_hints)
	print("calc_v_hints", calc_v_hints)
	return total_to_be_colored == total_colored and h_hints == calc_h_hints and v_hints == calc_v_hints	


# Takes a list or ndarray object and returns a list of the elements.
# Works for 2D lists and ndarrys.
def ensure_list(arr):
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    for i, el in enumerate(arr):
        if isinstance(el, np.ndarray):
            arr[i] = el.tolist()
    return arr	
	
	
# Calculate all permutations of r size of a given list of elements,
# then sort the list using the sort_idx
def permutations(arr, size=None, sort_idx=None):
	size = len(arr) if size is None else size
	sort_idx = 0 if sort_idx is None else sort_idx
	return sort_tuple(list(set(itertools.permutations(arr, size))), sort_idx)
	

# Sort a list of tuples using the given idx as the sort key
def sort_tuple(lst, idx):
	print("lst:", lst, "idx:", idx)
	# lst.sort(key=lambda tup: [tup[i] for i in range(idx, len(tup))])
	lst.sort(key=lambda tup: tup[idx])
	return lst
	

# def recursive_sort(lst,idx):
	# if not any(lst):
		# return lst
	# lst = sort_tuple(lst, idx)
	# for i in range(idx + 1):
		# sublsts = 
	# for i, l in enumerate(lst):
		# print("\ti:", i, "l:", l)
		# lst[i] = l[i][:idx + 1] + sort_tuple(list(l[idx + 1:]), idx + 1)
		
		
def cominations(ranges):
	comb = []
	if any(ranges):
		comb = [[i] for i in ranges[0]]
		for j, r in enumerate(ranges[1:]):
			for i in r:
				# print("r:", r, "i:", i, "\ncomb:", comb)
				comb += [c + [i] for c in comb if len(c) == j + 1]
	return [c for c in comb if len(c) == len(ranges)]
	
	
def n_combinations(n, r):
	return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))
		

def n_permutations(n, r):
	return math.factorial(n) / math.factorial(n - r)


#######################################################################################################################

def run_tests(func, test_set):
	failed_tests = []
	longest_name = max([len(name) for name in test_set])
	longest_test = max([len(str(test_list)) for test_list in test_set.values() if test_list])
	print("\n\n\t\tTesting:", func, "\n")
	for name, test_args in test_set.items():
	
		args = test_args[0]
		desired_answer = test_args[1]
		result = func(*args)
		is_desired_result = result == desired_answer
		
		test_name = "\n\t\t" + name.ljust(longest_name, " ") + "\n"
		args_str = "args:\t\t" + str(args).rjust(longest_test, " ") + "\n"
		desired_str = "desired:\t" + str(desired_answer).rjust(longest_test, " ") + "\n"
		result_str = "\t\t->\t" + str(result).ljust(len(args_str), " ")
		border = "".join(["#" for i in range(max([len(s) + 10 for s in [test_name, args_str, desired_str, result_str]]))])
		
		print(border + test_name + args_str + desired_str + result_str + "\n\tcorrect:\t" + str(is_desired_result) + "\n" + border)
		
		if not is_desired_result:
			failed_tests.append(name)
	
	# print("\n\tFailed Tests\n-\t", "\n-\t".join(test for test in failed_tests) + "\n")
	return failed_tests
	
	
def run_multiple_tests(tests_to_run):
	failed_tests = {}
	for test in tests_to_run:
		func, test_set = test
		test_results = run_tests(func, test_set)
		if test_results:
			failed_tests[str(func)] = test_results
		
	print("\n\t\t\tFailed Tests\n")
	for func, failed_test_results in failed_tests.items():
		print("\n-\tFunc:", func, "\n\t-\t", "\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")
		# for test in failed_test_results:
		# print("failed_test_results:", failed_test_results, "test:", test)
		# print("\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")
		
		
#######################################################################################################################

# Sample smiley puzzle for testing
puzzle_test_1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                 [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
                 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]
				 
v_hints_test_1 = [[0], [5], [1,2], [1,2], [1,2,1,1], [1,2,2,1], [1,2,2,1], [1,2,1], [1,2,1], [1,2,1], [1,2,2,1], [1,2,2,1], [1,2,1,1], [1,2], [1,2], [5], [0]]
h_hints_test_1 = [[0], [11], [1,1], [1,3,3,1], [1,3,3,1], [1,1], [1,9,1], [2,7,2], [2,2], [11]]
top_cut_test_1 = 1
bottom_cut_test_1 = len(h_hints_test_1) - 4
left_cut_test_1 = 1
right_cut_test_1 = len(v_hints_test_1) - 2


cut_puzzle_test_set = {
	"test_1": [
		[
			puzzle_test_1,
			h_hints_test_1,
			v_hints_test_1,
			top_cut_test_1,
			bottom_cut_test_1,
			left_cut_test_1,
			right_cut_test_1
		],
		(
			[ # new puzzle
				[1,0,0,0,0,0,0,0,0,0,0,0,1],
				[0,0,1,1,1,0,0,0,1,1,1,0,0],
				[0,0,1,1,1,0,0,0,1,1,1,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,]
			],
			[ # new h_hints
				[1, 1], [3, 3], [3, 3], [0]
			],
			[ # new v_hints
				[1], [0], [2], [2], [2], [0], [0], [0], [2], [2], [2], [0], [1]
			],
			( # chunks
				[ # top chunk
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
				],
				[ # bottom chunk
					[0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
					[0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
					[0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
					[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
				],
				[ # left chunk
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 1, 1, 1, 1, 1, 0, 0]
				],
				[ # right chunk
					[0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				]
			)
		)
	],
	"empty puzzle, preserving hints": [
		[
			[ # puzzle
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0]
			],
			[ # h_hints
				[0], [3], [1,1], [3], [0]
			],
			[ # v_hints
				[0], [3], [1,1], [3], [0]
			],
			0, # top cut
			5, # bottom cut
			0, # left cut
			5 # right cut
		],
		(
			[ # new puzzle
				[0,0,0,0],
				[0,0,0,0],
				[0,0,0,0],
				[0,0,0,0]
			],
			[ # new h_hints
				[3], [1,1], [3], [0]
			],
			[ # new v_hints
				[3], [1,1], [3], [0]
			],
			( # chunks
				[ # top chunk
					[0,0,0,0,0]
				],
				[ # bottom chunk
				],
				[ # left chunk
					[0, 0, 0, 0, 0]
				],
				[ # right chunk
				]
			)
		)
	],
	"indices too large, return nothing": [
		[
			[ # puzzle
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0]
			],
			[ # h_hints
				[0], [3], [1,1], [3], [0]
			],
			[ # v_hints
				[0], [3], [1,1], [3], [0]
			],
			7, # top cut
			8, # bottom cut
			7, # left cut
			8 # right cut
		],
		(
			[], # new puzzle
			[], # new h_hints
			[], # new v_hints
			( # chunks
				[ # top chunk
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0]
				],
				[], # bottom chunk
				[ # left chunk
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0]
				],
				[] # right chunk
			)
		)
	],
	"cut whole puzzle, return nothing": [
		[
			[ # puzzle
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0]
			],
			[ # h_hints
				[0], [3], [1,1], [3], [0]
			],
			[ # v_hints
				[0], [3], [1,1], [3], [0]
			],
			0, # top cut
			0, # bottom cut
			0, # left cut
			0 # right cut
		],
		(
			[], # new puzzle
			[], # new h_hints
			[], # new v_hints
			( # chunks
				[ # top chunk
					[0,0,0,0,0]
				],
				[ # bottom chunk
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0]
				],
				
				[ # left chunk
					[0,0,0,0,0]
				],
				[ # right chunk
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0],
					[0,0,0,0,0]
				]
			)
		)
	]
}

cut_smiley, cut_smiley_h_hints, cut_smiley_v_hints, cut_smiley_chunks = cut_puzzle(
	puzzle_test_1,
	h_hints_test_1,
	v_hints_test_1,
	top_cut_test_1,
	bottom_cut_test_1,
	left_cut_test_1 + 3,
	right_cut_test_1
)

pad_puzzle_test_set = {
	"cut_smiley": [
		[
			cut_smiley,
			cut_smiley_chunks
		],
		puzzle_test_1
	],
	"test_1": [
				[
					[ # cut puzzle
						[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
						[0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
						[0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0],
						[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
						[0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
						[0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0],
						[0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
						[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
					],	
					[ # chunks
						[ # top chunk
							[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
						],
						[], # bottom chunk
						[], # left chunk
						[] # right chunk
					]
				],
				puzzle_test_1
			]
}
			
greatest_diff_test_set = {
	"none": [[None], (None, None)],
	"none list": [[[]], (None, None)],
	"1 element list": [[[1]], (1, 1)],
	"test_1": [[[2, 4, 5, 8, 10, 11, 12, 16]], (12, 16)],
	"test_2": [[[1, 2, 8, 10, 11, 12, 16]], (2, 8)]
}	
	
remaining_list_test_set = {
	"none": [[None, 1], []],
	"none list, 5 size": [[[], 5], []],
	"1 element, 0 size": [[[1], 0], []],
	"test_1, 15 size": [[[2, 4, 5, 8, 10, 11, 12, 16], 15], [0, 1, 3, 6, 7, 9, 13, 14]],
	"test_2, 25 size": [[[1, 2, 8, 10, 11, 12, 16], 25], [0, 3, 4, 5, 6, 7, 9, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24]],
	"no overlap": [[[12, 13, 14, 15, 16, 17], 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
}

outside_indices_test_set = {
	"no overlap": [[[12, 13, 14, 15, 16, 17], 10], (0, 10)],
	"encompasses entire list": [[[1, 2, 8, 10, 11, 12, 16], 25], (0, 25)],
	"canter indices": [[[0, 1, 2, 8, 10, 11, 12, 16], 16], (2, 16)],
	"no list, so nothing to return": [[[], 5], (None, None)]
}

remaining_spaces_test_set = {
	"test_1": [
		[
			[
				[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0]
			]
		],
		[
			[(0, 4), (16, 20)]
		]
	],
	"test_2": [
		[
			[
				[0,0,0,0,1,1,1,1,-2,-2,-2,-2,-2,1,1,1,0,0,0,0]
			]
		],
		[
			[(0, 4), (16, 20)]
		]
	],
	"test_3": [
		[
			[
				[0,0,0,0,1,1,1,-2,0,0,0,0,0,-2,1,1,0,0,0,0],
				[1,1,-2,0,-2,1,-2,0,0,0,0,0,0,0,-2,-2,0,0,0,0],
				[1,1,1,-2,0,-2,0,0,0,0,0,0,0,0,0,0,-2,1,1,1],
				[1,1,1,1,-2,0,0,0,0,0,0,0,0,0,0,-2,1,1,1,1],
				[1,1,1,1,1,-2,0,0,0,0,0,0,0,0,0,-2,1,1,1,1]
			]
		],
		[
			[(0, 4), (8, 13), (16, 20)],
			[(3, 4), (7, 14), (16, 20)],
			[(4, 5), (6, 16)],
			[(5, 15)],
			[(6, 15)]
		]
	],
	"test_4": [
		[	
			[   #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
				[1, 1, 1, 1, 1,-2, 0, 0, 1, 0, 0, 0, 1, 0, 0,-2, 1, 1, 1, 1], 
				[1, 1, 1, 1, 1,-2, 0, 0, 0, 0, 0, 0, 0, 0, 0,-2, 1, 1, 1, 1], 
				[1, 1, 1, 1, 1,-2, 0, 0, 0, 0, 0, 0, 0, 0, 0,-2, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 1,-2, 0, 0, 0, 0, 0, 0, 0,-2, 1, 1, 1, 1, 1], 
				[1, 1, 1, 1, 1, 1, 1,-2, 0, 0, 0, 0, 0,-2, 1, 1, 1, 1, 1, 1], 
				[1, 1, 1, 1, 1, 1, 1, 1, 1,-2, 1,-2, 1, 1, 1, 1, 1, 1, 1, 1], 
				[1, 1, 1, 1, 1,-2,-2, 0, 0, 0, 1, 0, 0, 0,-2,-2, 1, 1, 1, 1], 
				[1, 1, 1, 1,-2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,-2, 1, 1, 1], 
				[0, 0, 0, 0, 0,-2, 1,-2,-2,-2,-2,-2,-2,-2, 1,-2, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
				[1,-2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
				[1, 1,-2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
			]
		],
		[
			[(6,8), (9, 12), (13, 15)],
			[(6, 15)],
			[(6, 15)],
			[(7, 14)],
			[(8, 13)],
			[],
			[(7, 10), (11, 14)],
			[(5, 6), (7, 14), (15, 16)],
			[(0, 5), (16, 20)],
			[(0, 5), (16, 20)],
			[(2, 5), (16, 20)],
			[(3, 5), (16, 20)],
			[(0, 5), (16, 20)]
		]
	]
}

np_count_test_set = {
	"test_1": [
		[
			[1,1,-2,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
			-2
		],
		1
	],
	"test_2": [
		[
			[1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
			-2
		],
		0
	]
}

invert_puzzle_test_set = {
	"test_1": [
		[
			puzzle_test_1
		],
		[
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
			[1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
			[1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
			[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
			[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
			[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
			[1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
			[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
		]
	],
	"test_2": [
		[
			[
				[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
				[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
				[1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
				[1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
				[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
				[1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
				[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
				[1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
				[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
			]
		],
		puzzle_test_1
	]
}

check_puzzle_is_solved_test_set = {
	"test_1": [
		[puzzle_test_1, h_hints_test_1, v_hints_test_1],
		True
	],
	"test_2": [
		[
			[[0,1,0],[0,1,0],[0,1,0]],
			[[1],[1],[1]],
			[[0],[3],[0]]
		],
		True
	],
	"test_3": [
		[
			[[0,1,0],[0,1,0],[0,1,0]],
			[[1],[1],[0]],
			[[0],[3],[0]]
		],
		False
	],
	"test_4": [
		[
			[
				[ 0, 0,-2, 0, 0, 0,-2, 0, 0],
				[ 0, 0, 1, 0, 0, 0, 1, 0, 0],
				[-2,-2,-2,-2,-2,-2,-2,-2,-2],
				[ 0, 0,-2, 0, 0, 0,-2, 0, 0],
				[-2,-2,-2,-2,-2,-2,-2,-2,-2],
				[ 1,-2,-2,-2,-2,-2,-2,-2, 1],
				[ 1, 1, 1,-2, 1,-2, 1, 1, 1],
				[-2, 0, 1, 0, 1, 0, 1, 0,-2],
				[ 1,-2, 1,-2, 1,-2, 1,-2, 1]
			],
			[[1,1], [3,3], [0], [1], [0], [1,1], [3,1,3], [5], [1,1,1,1,1]],
			[[1,2,1], [2,1], [1,3], [1], [1,3], [1], [1,3], [2,1], [1,2,1]]
		],
		False
	],
	"test_5": [
		[
			[
				[ 0, 1,-2, 0, 0, 0,-2, 1, 0],
				[ 1, 1, 1, 0, 0, 0, 1, 1, 1],
				[-2,-2,-2,-2,-2,-2,-2,-2,-2],
				[ 0, 0,-2, 0, 1, 0,-2, 0, 0],
				[-2,-2,-2,-2, 0,-2,-2,-2,-2],
				[ 1,-2,-2,-2,-2,-2,-2,-2, 1],
				[ 1, 1, 1,-2, 1,-2, 1, 1, 1],
				[-2, 0, 1, 1, 1, 1, 1, 0,-2],
				[ 1,-2, 1,-2, 1,-2, 1,-2, 1]
			],
			[[1,1], [3,3], [0], [1], [0], [1,1], [3,1,3], [5], [1,1,1,1,1]],
			[[1,2,1], [2,1], [1,3], [1], [1,3], [1], [1,3], [2,1], [1,2,1]]
		],
		True
	]
}

ensure_list_test_set = {
	"1D list": [
		[
			[1,2,3,4,5]
		],
		[1,2,3,4,5]
	],
	"2D list": [
		[
			[
				[1,2,3,4,5],
				[5,4,3,2,1],
				[5,5,5,5,5]
			]
		],
		[
			[1,2,3,4,5],
			[5,4,3,2,1],
			[5,5,5,5,5]
		]
	],
	"1D ndarray": [
		[
			np.array([1,2,3,4,5])
		],
		[1,2,3,4,5]
	],
	"2D ndarray": [
		[
			np.array([
				[1,2,3,4,5],
				[5,4,3,2,1],
				[5,5,5,5,5]
			]),
		],
		[
			[1,2,3,4,5],
			[5,4,3,2,1],
			[5,5,5,5,5]
		]
	],
	"2D list with ndarray element": [
		[
			[
				[1,2,3,4,5],
				[5,4,3,2,1],
				np.array([5,5,5,5,5])
			],
		],
		[
			[1,2,3,4,5],
			[5,4,3,2,1],
			[5,5,5,5,5]
		]
	]
}

permutations_test_set = {
	"test_1, sort at idx 0": [
		[
			[1,2,3],
			3,	# r size
			0  # sort_idx
		],
		[(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)]
	],
	"test_2, sort at idx 1": [
		[
			[1,2,3],
			3,	# r size
			1  # sort_idx
		],
		[(3,1,2),(2,1,3),(3,2,1),(1,2,3),(1,3,2),(2,3,1)]
	],
	"test_3, sort at idx 2": [
		[
			[1,2,3],
			3,	# r size
			2  # sort_idx
		],
		[(3,2,1),(2,3,1),(3,1,2),(1,3,2),(1,2,3),(2,1,3)]
	]
}

n_combinations_test_set = {
	"test_1, selceting 4 from 30": [
		[
			30,
			4
		],
		27405
	]
}


#######################################################################################################################


# run_tests(greatest_diff, greatest_diff_test_set)
# run_tests(remaining_list, remaining_list_test_set)
# run_tests(outside_indices, outside_indices_test_set)
# run_tests(cut_puzzle, cut_puzzle_test_set)
# run_tests(pad_puzzle, pad_puzzle_test_set)
# run_tests(remaining_spaces, remaining_spaces_test_set)
# run_tests(np_count, np_count_test_set)
# run_tests(invert_puzzle, invert_puzzle_test_set)
# run_tests(check_puzzle_is_solved, check_puzzle_is_solved_test_set)
# run_tests(ensure_list, ensure_list_test_set)
run_tests(n_combinations, n_combinations_test_set)

tests_to_run = [
	(greatest_diff, greatest_diff_test_set),
	(remaining_list, remaining_list_test_set),
	(outside_indices, outside_indices_test_set),
	(cut_puzzle, cut_puzzle_test_set),
	(pad_puzzle, pad_puzzle_test_set),
	(pad_puzzle, pad_puzzle_test_set),
	(remaining_spaces, remaining_spaces_test_set),
	(np_count, np_count_test_set),
	(invert_puzzle, invert_puzzle_test_set),
	(check_puzzle_is_solved, check_puzzle_is_solved_test_set),
	(ensure_list, ensure_list_test_set),
	(permutations, permutations_test_set),
	(n_combinations, n_combinations_test_set)
]
# run_multiple_tests(tests_to_run)

# lst = permutations([1,2,3])
# print("".join(["#" for i in range(30)]))
# print(recursive_sort(lst, 0))
# c = [range(3), range(3), range(3)]
# c = [range(42), range(840), range(7), range(12)]
# combs = sort_tuple(cominations(c), 0)
# for co in combs:
	# print(co)
# print("len(combs", len(combs))