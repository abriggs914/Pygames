from heapq import heapify, heappop, heappush

LEGEND = {
	"empty": 0,
	"block": 1,
	"start": "s",
	"end": "e",
	"checked": "c",
	"looked_at": "a"
}

class Node:
	
	def __init__(self, idx):
		self.block_idx = idx
		self.f_cost = 0
		self.g_cost = 0
		self.h_cost = 0

	def __repr__(self):
		return "idx: {i}, f: {f}, g: {g}, h: {h}".format(i=self.block_idx, f=self.f_cost, g=self.g_cost, h=self.h_cost)

	def set_path_cost(self, f_cost, g_cost, h_cost):
		self.f_cost = f_cost
		self.g_cost = g_cost
		self.h_cost = h_cost

def empty_grid(rows, cols):
	return [[(LEGEND["empty"], Node((r * c) + c)) for c in range(cols)] for r in range(rows)]

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
		self.status[r][c] = LEGEND["start"], Node(s)
	
	def set_end(self, e):
		r, c = divmod(e, self.cols)
		self.status[r][c] = LEGEND["end"], Node(e)
		
	# convert a single grid number to row and col indices
	# and mark the status of that space as a block
	def set_block(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["block"], Node(i)
		
	def set_empty(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["empty"], Node(i)
		
	def set_checked(self, i, path_cost):
		r, c = self.get_block_r_c(i)
		n = Node(i)
		n.set_path_cost(*path_cost)
		self.status[r][c] = LEGEND["checked"], n

	def get_node_at_index(self, i):
		r, c = self.get_block_r_c(i)
		return self.get_node_at_r_c(r, c)

	def get_node_at_r_c(self, r, c):
		return self.status[r][c][1]
		
	def get_spaces(self, symbol=LEGEND["empty"]):
		squares = []
		for r in range(self.rows):
			for c in range(self.cols):
				if self.status[r][c][0] == symbol:
					squares.append(self.get_block_index(r, c))
		return squares
		
	def reset_search(self):
		for r in range(self.rows):
			for c in range(self.cols):
				i = self.get_block_index(r, c)
				if self.status[r][c][0] == LEGEND["checked"] or self.status[r][c][0] == LEGEND["looked_at"]:
					self.status[r][c] = LEGEND["empty"], Node(i)
				else:
					self.status[r][c] = self.status[r][c][0], Node(i)
					
	def reset_search_blocks(self):
		for r in range(self.rows):
			for c in range(self.cols):
				i = self.get_block_index(r, c)
				if self.status[r][c][0] == LEGEND["checked"] or self.status[r][c][0] == LEGEND["block"] or self.status[r][c][0] == LEGEND["looked_at"]:
					self.status[r][c] = LEGEND["empty"], Node(i)
				else:
					self.status[r][c] = self.status[r][c][0], Node(i)
		
	def reset_clear(self):
		self.status = empty_grid(self.rows, self.cols)

	def set_looked_at(self, i):
		r, c = self.get_block_r_c(i)
		self.status[r][c] = LEGEND["looked_at"], Node(i)
		
class A_Star:
	def __init__(self, grid, EUCLIDEAN=True):
		self.grid = grid
		self.EUCLIDEAN = EUCLIDEAN
		self.solved = False
		self.solvable = None
		self.nodes_considered = []
		self.path_travelled = None
		
	# Calculate the euclidean distance between a node and an end node.
	# Uses the rows and col numbers for distances.
	def euclidean_heuristic(self, start, goal):
		return self.euclidean_distance(start, goal)
	
	# Calculate the path cost of travelling from one node to the next.
	# This corresponds to the euclidean distance between two nodes.
	def euclidean_path_cost(self, start, goal):
		# return self.path_travelled + (2 ** 0.5)
		# return self.euclidean_heuristic(start, goal)
		r, c = self.grid.get_block_r_c(start)
		# print("self.grid.status[r][c][1].path_cost", self.grid.status[r][c][1].path_cost, "\nself.euclidean_heuristic(start, goal)", self.euclidean_heuristic(start, goal))
		return self.grid.status[r][c][1].g_cost + self.euclidean_heuristic(start, goal)
		
	# Calculate the manhattan distance between a node and an end node.
	# Uses the rows and col numbers for distances.
	def manhattan_heuristic(self, start, goal):
		return self.manhattan_distance(start, goal)
	
	# Calculate the path cost of travelling from one node to the next.
	# This corresponds to the manhattan distance between two nodes.
	def manhattan_path_cost(self, start, goal):
		# return self.path_travelled + 1
		# return self.manhattan_heuristic(start, goal)
		r, c = self.grid.get_block_r_c(start)
		return self.grid.status[r][c][1].g_cost + self.manhattan_heuristic(start, goal)
		
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
		
	# def next_node(self, last_node, new_checked):
	# 	best_val = (-1, float("inf"))
	# 	end_spaces = self.grid.get_spaces(LEGEND["end"])
	# 	start_spaces = self.grid.get_spaces(LEGEND["start"])
	# 	exempt = [LEGEND["block"], LEGEND["start"], LEGEND["checked"]]
	# 	for node in new_checked:
	# 		r, c = self.grid.get_block_r_c(node)
	# 		if self.grid.status[r][c][0] in exempt:
	# 			continue
	# 		for goal in end_spaces:
	# 			for start in start_spaces:
	# 				if self.EUCLIDEAN:
	# 					# f_cost = self.euclidean_heuristic(node, goal) + self.euclidean_path_cost(node, start)
	# 					h_cost = self.euclidean_heuristic(node, goal)
	# 					g_cost = self.euclidean_path_cost(node, last_node)
	# 					f_cost = h_cost + g_cost
	# 				else:
	# 					# f_cost = self.manhattan_heuristic(node, goal) + self.manhattan_path_cost(node, start)
	# 					h_cost = self.manhattan_heuristic(node, goal)
	# 					g_cost = self.manhattan_path_cost(node, last_node)
	# 					f_cost = h_cost + g_cost
	# 				n, *cost = best_val
	# 				if f_cost < sum(cost):
	# 					best_val = (node, h_cost, g_cost)
	# 		print("->", node, "n:", n, "f_cost:", f_cost, "cost:", cost, "best:", best_val)
	# 	r, c = self.grid.get_block_r_c(best_val[0])
	# 	self.grid.status[r][c][1].set_path_cost(f_cost, g_cost, h_cost)
	# 	return best_val
		
	# def solve(self):
		# if self.solvable and not self.solved:
			# end_spaces = self.grid.get_spaces(LEGEND["end"])
			# new_checked = []
			# past_checked = self.grid.get_spaces(LEGEND["checked"])
			# past_checked += self.grid.get_spaces(LEGEND["start"])
			# # print("past_checked(", len(past_checked), ")", past_checked)
			# for p_c in past_checked:
				# surrounding = self.get_surrounding_nodes(p_c)
				# # print("p_c:", p_c, ", surrounding:", surrounding)
				# nodes_to_check = []
				# for s in surrounding:
					# if s not in past_checked and s not in new_checked:
						# nodes_to_check.append(s)
				# node_to_check, *cost = self.next_node(p_c, nodes_to_check)
				# new_checked.append(node_to_check)
				# print("\t\tnode_to_check:", node_to_check, "cost:", cost)
			# # node_to_check, *cost = self.next_node(past_checked[-1], new_checked)
			# print("new_checked", new_checked)
			# past_checked += [node_to_check]
			# # print("travelled cost:", self.path_travelled , "cost:", cost)
			# if node_to_check < 0:
				# self.solvable = False
			# elif node_to_check in end_spaces:
				# self.solved = True
						
			# yield node_to_check, cost
			
	def euclidean_distance(self, node_1, node_2):
		s_r, s_c = self.grid.get_block_r_c(node_1)
		g_r, g_c = self.grid.get_block_r_c(node_2)
		return ((g_r - s_r) ** 2 + (g_c - s_c) ** 2) ** 0.5
		
	def manhattan_distance(self, node_1, node_2):
		s_r, s_c = self.grid.get_block_r_c(node_1)
		g_r, g_c = self.grid.get_block_r_c(node_2)
		return abs(g_r - s_r) + abs(g_c - s_c) 


	# Calculate the f_cost of travelling from the previous node to the current node.
	# Returns a tuple of the f_cost, (h_cost, g_cost, previous, current)
	def f_cost(self, previous, current):
		goal_nodes = self.grid.get_spaces(LEGEND["end"])
		prev_r, prev_c = self.grid.get_block_r_c(previous)
		if self.EUCLIDEAN:
			g_cost = self.euclidean_distance(previous, current) + self.grid.status[prev_r][prev_c][1].g_cost
			h_costs = []
			for goal_node in goal_nodes:
				h_costs.append(self.euclidean_heuristic(current, goal_node))
			h_cost = min(h_costs)
		else:
			g_cost = self.manhattan_distance(previous, current) + self.grid.status[prev_r][prev_c][1].g_cost
			h_costs = []
			for goal_node in self.grid.get_spaces(LEGEND["end"]):
				h_costs.append(self.manhattan_heuristic(current, goal_node))
			h_cost = min(h_costs)			
		# print("f:", (h_cost + g_cost), "h:", h_cost, "g:", g_cost, "travelling", previous, "to", current)
		return h_cost + g_cost, (h_cost, g_cost, previous, current)
			
	def solve(self):
		checked_nodes = self.grid.get_spaces(LEGEND["checked"])
		checked_nodes += self.grid.get_spaces(LEGEND["start"])
		exempt = checked_nodes + self.grid.get_spaces(LEGEND["block"])
		to_consider = []
		for checked_node in checked_nodes:
			surrounding = [node for node in self.get_surrounding_nodes(checked_node) if node not in exempt]
			to_consider += [self.f_cost(checked_node, node) for node in surrounding]
		heapify(to_consider)

		# print("to_consider")
		# for t in to_consider:
		# 	print("{0} -> {1} f: {2}, g: {3}, h: {4}".format(t[1][2], t[1][3], t[0], t[1][1], t[1][0]))
			# mark the surrounding...

		for i in range(1, len(to_consider)):
			t = to_consider[i]
			self.grid.set_looked_at(t[1][3])

		if not to_consider:
			self.solvable = False
			yield -1, float("inf")
		f_cost, next_node_vals = heappop(to_consider)
		h_cost, g_cost, current, next_node = next_node_vals
		if h_cost == 0:
			self.solved = True
		self.nodes_considered.append(next_node)
		# print("{n}:\tf:{f},\tg:{g}\th:{h}".format(n=next_node, f=f_cost, g=g_cost, h=h_cost))
		yield next_node, (f_cost, g_cost, h_cost)

	# Because the solve function is a generator, it doesnt solve find the path all in one go.
	# This function calculates the shortest path by working backwards from the end node encountered,
	# traversing each surrounding node that was considered and returning the path found.
	def calculate_path(self):
		# TODO: this doesnt work when going right to left...
		travelled_path = []
		start_nodes = self.grid.get_spaces(LEGEND["start"])
		end_nodes = self.grid.get_spaces(LEGEND["end"])

		# start at the end node
		end_encountered = None
		for i in self.nodes_considered:
			if i in end_nodes:
				end_encountered = i
		cost, block = self.grid.get_node_at_index(end_encountered).g_cost, end_encountered

		# list of tuples for heap purposes; (cost, block)
		path = [(self.grid.get_node_at_index(n).g_cost, n) for n in self.nodes_considered if n != end_encountered]
		heapify(path)
		# dict of the path list where the blocks are keys and costs are values, used to track the blocks looked at
		path_blocks = {e[1]: e[0] for e in path}
		travelled_path.append(block)
		path_found = False

		while not path_found:
			surrounding = self.get_surrounding_nodes(block)
			# creating a list of tuples; (cost, block) of solely the surrounding nodes to be heapified
			surrounding_blocks = [(path_blocks[s], s) for s in surrounding if s in path_blocks]
			# check that a start node isn't already adjacent, since they aren't included in the self.nodes_considered list
			for s in surrounding:
				if s in start_nodes:
					travelled_path.append(s)
					path_found = True
					break
			if not path_found:
				heapify(surrounding_blocks)
				cost, block = heappop(surrounding_blocks)
				travelled_path.append(block)
				# delete surrounding nodes of the smallest-cost block for next iteration
				for b in surrounding_blocks:
					del path_blocks[b[1]]
				if block in start_nodes:
					path_found = True
		return travelled_path

	def get_path(self):
		if self.solved and self.solvable:
			if self.path_travelled is None:
				self.path_travelled = self.calculate_path()
			return self.path_travelled
