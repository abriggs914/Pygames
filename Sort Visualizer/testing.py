import math

# Orientations
NORTH = 0
NORTH_EAST = 1
EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7

class Rect:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.top = y
		self.left = x
		self.bottom = y + h
		self.right = x + w
		self.center = x + (w / 2), y + (h / 2)
		self.top_left = x, y
		self.top_right = x + w, y
		self.bottom_left = x, y + h
		self.bottom_right = x + w, y + h
		
	def __repr__(self):
		return "<rect(" + ", ".join(list(map(str, [self.x, self.y, self.width, self.height]))) + ")>"

# Rotate a 2D point about the origin a given amount of degrees
def rotate_on_origin(px, py, theta):
	# x′ = x * cos(θ) - y * sin(θ)
    # y′ = x * sin(θ) + y * cos(θ)
	t = math.radians(theta)
	x = (px * math.cos(t)) - (py * math.sin(t))
	y = (px * math.sin(t)) + (py * math.cos(t))
	return x, y
	
def rotate_point(cx, cy, px, py, theta):
	xd = 0 - cx
	yd = 0 - cy
	rx, ry = rotate_on_origin(px + xd, py + yd, theta)
	print("cx:", cx, "cy:", cy, "\npx:", px, "py:", py, "\npx - xd:", px - xd, "py - yd:", py - yd, "\nxd:", xd, "yd:", yd, "\nrx:", rx, "ry:", ry, "\nrx - xd:", rx - xd, "ry - yd", ry - yd, "\ntheta:", theta)
	return rx - xd, ry - yd
	

def draw_arrow(r, p, o, c, w):
	# p1 - tip
	# p2 - first wing
	# p3 - second wing
	p1x = r.center[0]
	p1y = r.center[1] + (r.height * p)
	p2x = r.center[0] - (r.width * p)
	p2y = r.center[1] - (r.height * p)
	p3x = r.center[0] + (r.width * p)
	p3y = r.center[1] - (r.height * p)
	points = [rotate_point(*r.center, *pt, o * 45) for pt in [(p1x, p1y), (p2x, p2y), (p3x, p3y)]]
	return points


#######################################################################################################################

def run_tests(func, test_set):
	failed_tests = []
	longest_name = max([len(name) for name in test_set])
	longest_test = max([len(str(test_list)) for test_list in test_set.values() if test_list])
	print("\n\n\t\tTesting:", func, "\n")
	num_tests = len(test_set)
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
	
	num_failed = len(failed_tests)
	print("\n\tFailed Tests\t" + str(num_failed) + " / " + str(num_tests) + "\n-\t" + "\n-\t".join(test for test in failed_tests) + "\n")
	return failed_tests
	
	
def run_multiple_tests(tests_to_run):
	failed_tests = {}
	num_tests = 0
	num_failed = 0
	for test in tests_to_run:
		func, test_set = test
		num_tests += len(test_set)
		test_results = run_tests(func, test_set)
		if test_results:
			failed_tests[str(func)] = test_results
			num_failed += len(test_results)
		
	print("\n\t\t\tFailed Tests\t" + str(num_failed) + " / " + str(num_tests) + "\n")
	for func, failed_test_results in failed_tests.items():
		print("\n-\tFunc:", func, "\n\t-\t", "\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")
		# for test in failed_test_results:
		# print("failed_test_results:", failed_test_results, "test:", test)
		# print("\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")
		
#######################################################################################################################

r1 = Rect(50, 50, 150, 150)

draw_arrow_test_set = {
	"north": [
		[r1, 0.2, NORTH, (0, 0, 0), 3],
		[(125.0, 155.0), (95.0, 95.0), (155.0, 95.0)]
	]
}
tests_to_run = [
	(draw_arrow, draw_arrow_test_set)
]
run_multiple_tests(tests_to_run)