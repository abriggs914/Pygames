
LEGEND = {
	"empty": 0,
	"block": 1,
	"start": "s",
	"end": "e",
	"checked": "c"
}

def empty_grid(rows, cols):
	return [[LEGEND["empty"] for c in range(cols)] for r in range(rows)]

class Map:
	
	def __init__(self, rows, cols, start=None, end=None, blocks=None):
		self.rows = rows
		self.cols = cols
		self.size = rows * cols
		self.status = empty_grid(self.rows, self.cols)
		
		self.set_start_node(start)
		self.set_end_node(end)
		self.set_block_node(blocks)
		
	def __repr__(self):
		return "<Map object, ({r}x{c})>".format(r=self.rows, c=self.cols)
					
	def set_start_node(self, s):
		if not s:
			return
		if type(s) == list:
			for st in s:
				self.set_start(st)
		else:
			self.set_start(s)
					
	def set_end_node(self, e):
		if not e:
			return
		if type(e) == list:
			for ed in e:
				self.set_end(ed)
		else:
			self.set_end(e)
			
	def set_block_node(self, blocks):
		if blocks:
			for block in blocks:
				if type(block) is int:
					self.set_block(block)
				else:
					index = self.set_block_index(*block)
					self.set_block(index)
	
	def get_block_r_c(self, i):
		return divmod(i, self.cols)
		
	# convert row and col indices to single grid number
	# ex: in a 6x5 grid, block 25 is row: 5 col: 0
	def get_block_index(self, r, c):
		return (r * self.cols) + c
			
	def set_start(self, s):
		r, c = divmod(s, self.cols)
		self.status[r][c] = LEGEND["start"]
	
	def set_end(self, e):
		r, c = divmod(e, self.cols)
		self.status[r][c] = LEGEND["end"]
		
	# convert a single grid number to row and col indices
	# and mark the status of that space as a block
	def set_block(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["block"]
		
	def set_empty(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["empty"]
		
	def set_checked(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["checked"]
		
	def get_spaces(self, symbol=LEGEND["empty"]):
		squares = []
		for r in range(self.rows):
			for c in range(self.cols):
				if self.status[r][c] == symbol:
					squares.append(self.get_block_index(r, c))
		return squares
		
	def reset_search(self):
		for r in range(self.rows):
			for c in range(self.cols):
				if self.status[r][c] == LEGEND["checked"]:
					self.status[r][c] = LEGEND["empty"]
					
	def reset_search_blocks(self):
		for r in range(self.rows):
			for c in range(self.cols):
				if self.status[r][c] == LEGEND["checked"] or self.status[r][c] == LEGEND["block"]:
					self.status[r][c] = LEGEND["empty"]
		
	def reset_clear(self):
		self.status = empty_grid(self.rows, self.cols)
		
class A_Star:
	def __init__(self, grid, EUCLIDEAN=True):
		self.grid = grid
		self.EUCLIDEAN = EUCLIDEAN
		self.solved = False
		self.solvable = None
		
	# Calculate the euclidean distance between a node and an end node.
	# Uses the rows and col numbers for distances.
	def euclidean_heuristic(self, start, goal):
		s_r, s_c = self.grid.get_block_r_c(start)
		g_r, g_c = self.grid.get_block_r_c(goal)
		return (((g_r + 1) - (s_r + 1)) ** 2 + ((g_c + 1) - (s_c + 1)) ** 2) ** 0.5
	
	# Calculate the path cost of travelling from one node to the next.
	# This corresponds to the euclidean distance between two nodes.
	def euclidean_path_cost(self, start, goal):
		return self.euclidean_heuristic(start, goal)
		
	# Calculate the manhattan distance between a node and an end node.
	# Uses the rows and col numbers for distances.
	def manhattan_heuristic(self, start, goal):
		s_r, s_c = self.grid.get_block_r_c(start)
		g_r, g_c = self.grid.get_block_r_c(goal)
		return abs((g_r + 1) - (s_r + 1)) + abs((g_c + 1) - (s_c + 1)) 
	
	# Calculate the path cost of travelling from one node to the next.
	# This corresponds to the manhattan distance between two nodes.
	def manhattan_path_cost(self, start, goal):
		return self.manhattan_heuristic(start, goal)
		
	def get_surrounding_nodes(self, i):
		r, c = self.grid.get_block_r_c(i)
		row_range = range(max(0, r - 1), (min(self.grid.rows - 1, r + 1)) + 1)
		col_range = range(max(0, c - 1), min(self.grid.cols - 1, c + 1) + 1)
		# print("surrounding {i}: rows: {rr}, cols: {cr}".format(i=i, rr=row_range, cr=col_range))
		surrounding = []
		for row in row_range:
			for col in col_range:
				index = self.grid.get_block_index(row, col)
				if i is not index:
					surrounding.append(index)
		if not self.EUCLIDEAN:
			manhattan = []
			for s in surrounding:
				row, col = self.grid.get_block_r_c(s)
				if row == r or col == c:
					manhattan.append(s)
			surrounding = manhattan
		return surrounding
		
	# Simply checks that there is at least one start and goal node.
	# No other checks are performed at this time
	def ready_to_solve(self):
		if not self.solved:
			start_spaces =  self.grid.get_spaces(LEGEND["start"])
			end_spaces = self.grid.get_spaces(LEGEND["end"])
			if len(start_spaces) > 0 and len(end_spaces) > 0:
				self.solvable = True
			else:
				self.solvable = False
			return self.solvable
		
	def next_node(self, new_checked):
		best_val = (-1, float("inf"))
		end_spaces = self.grid.get_spaces(LEGEND["end"])
		exempt = [LEGEND["block"], LEGEND["start"]]
		for node in new_checked:
			r, c = self.grid.get_block_r_c(node)
			if self.grid.status[r][c] in exempt:
				continue
			for goal in end_spaces:
				if self.EUCLIDEAN:
					f_cost = self.euclidean_heuristic(node, goal) + self.euclidean_path_cost(node, goal)
				else:
					f_cost = self.manhattan_heuristic(node, goal) + self.manhattan_path_cost(node, goal)
				n, cost = best_val
				if f_cost < cost:
					best_val = (node, f_cost)
		return best_val
		
	def solve(self):
		if self.solvable and not self.solved:
			end_spaces = self.grid.get_spaces(LEGEND["end"])
			new_checked = []
			past_checked = self.grid.get_spaces(LEGEND["checked"])
			past_checked += self.grid.get_spaces(LEGEND["start"])
				
			for p_c in past_checked:
				surrounding = self.get_surrounding_nodes(p_c)
				# print("p_c:", p_c, ", surrounding:", surrounding)
				for s in surrounding:
					if s not in past_checked and s not in new_checked:
						new_checked.append(s)
			node_to_check, cost = self.next_node(new_checked)
			past_checked += [node_to_check]
			if node_to_check < 0:
				self.solvable = False
			elif node_to_check in end_spaces:
				self.solved = True
						
			yield node_to_check