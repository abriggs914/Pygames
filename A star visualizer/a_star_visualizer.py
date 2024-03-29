import pygame
from time import time
from multiprocessing.pool import ThreadPool
from threading import Thread
from grid import Map, A_Star, LEGEND
from gui_handling import ask_dimens, ask_draw_square, ask_draw_block_indexes, ask_use_full_screen, message_window
from colors import *
from texts import *
from win32api import GetSystemMetrics

# TODO: On finish, report some general statistics about the search

# TODO: majorly increase the search speed. A generator doesnt seem to be doing the trick, maybe a list of decreasing
#  size containing remaining possibilities.. or an asyncronous approach

# Python program using pygame to visualize an A* pathfinding algorithm
# Modeled in part by the visualizer found here: https://qiao.github.io/PathFinding.js/visual/
# And by TechWithTim found here https://github.com/techwithtim/A-Path-Finding-Visualization
#
# July 2020

#################################################
##				   Design vars				   ##
#################################################

DEFAULT_SIZE = (900, 600)
WIDTH = DEFAULT_SIZE[0]
HEIGHT = DEFAULT_SIZE[1]
SCREEN_WIDTH = int(GetSystemMetrics(0) * 0.95)  # use a modified full screen approach because the pygame version
SCREEN_HEIGHT = int(GetSystemMetrics(1) * 0.9)  # had weird effects on other programs
ROWS = 5
COLS = 5
LINE_WIDTH = 1
SELECTION_WIDTH = 5
SCREEN_PROPORTION = 0.95  # Percentage of the display used for drawing
BUTTON_TEXT_FONT = None  # initialized in init_pygame function

#################################################
##				   Game vars				   ##
#################################################

DISPLAY = None
DATA = None
BUTTON_DATA = None
CLOCK = None
POP_UP_THREAD = None
USE_FULL_SCREEN = False
DRAW_SQUARE = True
DRAW_BLOCK_IDX = True
IDLE = "idle"
manhattan = "manhattan"
euclidean = "euclidean"

#################################################
##			    Button listeners			   ##
#################################################

load = "load"  # initialized in init_file_handling must be done there because file_handling uses
save = "save"  # small_pop_up and reset functions defined in this file


def switch_mode():
	mode = DATA["mode"]
	if mode == euclidean:
		button_data = BUTTON_DATA[euclidean]
		del BUTTON_DATA[euclidean]
		button_data[0] = manhattan
		BUTTON_DATA.update({manhattan: button_data})
		mode = manhattan
	elif mode == manhattan:
		button_data = BUTTON_DATA[manhattan]
		del BUTTON_DATA[manhattan]
		button_data[0] = euclidean
		BUTTON_DATA.update({euclidean: button_data})
		mode = euclidean
	DATA["mode"] = mode
	msg = "Switched to " + mode.title() + " mode."
	return small_pop_up, (DATA, DISPLAY, msg, mode, 0.5)


def about_menu():
	w = WIDTH * 0.6
	h = HEIGHT * 0.6
	x = (WIDTH - w) / 2
	y = (HEIGHT - h) / 2
	msg = ABOUT_MESSAGE
	return pop_up, (DATA, DISPLAY, msg, "about", x, y, w, h, None, BLACK, GOLD)


def full_reset():
	print("full reset")
	init()


def reset(click, DATA):
	print("reset")
	l, m, r = click
	print("data(", len(DATA), "):", DATA)
	if "a*" in DATA:
		del DATA["a*"]
	if l:
		DATA["grid"].reset_search()
	if m:
		DATA["grid"].reset_search_blocks()
	if r:
		DATA["grid"].reset_clear()


def get_button_data():
	return {
		"about": ["about", ABOUT_BUTTON_ACTIVE_COLOR, ABOUT_BUTTON_INACTIVE_COLOR, about_menu],
		"save": ["save", SAVE_BUTTON_ACTIVE_COLOR, SAVE_BUTTON_INACTIVE_COLOR, save],
		"load": ["load", LOAD_BUTTON_ACTIVE_COLOR, LOAD_BUTTON_INACTIVE_COLOR, load],
		"start": ["start", START_BUTTON_ACTIVE_COLOR, START_BUTTON_INACTIVE_COLOR],
		"pause": ["pause", PAUSE_BUTTON_ACTIVE_COLOR, PAUSE_BUTTON_INACTIVE_COLOR],
		"stop": ["stop", STOP_BUTTON_ACTIVE_COLOR, STOP_BUTTON_INACTIVE_COLOR],
		"reset": ["reset", RESET_BUTTON_ACTIVE_COLOR, RESET_BUTTON_INACTIVE_COLOR, reset],
		"draw": ["draw", DRAW_BUTTON_ACTIVE_COLOR, DRAW_BUTTON_INACTIVE_COLOR],
		"move_start": ["move_start", MOVE_START_BUTTON_ACTIVE_COLOR, MOVE_START_BUTTON_INACTIVE_COLOR],
		"move_end": ["move_end", MOVE_END_BUTTON_ACTIVE_COLOR, MOVE_END_BUTTON_INACTIVE_COLOR],
		"euclidean": ["euclidean", EUCLIDEAN_BUTTON_ACTIVE_COLOR, EUCLIDEAN_BUTTON_INACTIVE_COLOR, switch_mode]
	}


def kill_pop_up_thread():
	if isinstance(POP_UP_THREAD, Thread):
		if POP_UP_THREAD.is_alive():
			DATA["mode"] = IDLE
			POP_UP_THREAD.join()


# Display a small pop-up window over the middle of the screen
def small_pop_up(DATA, DISPLAY, msg, mode, show_time=float("inf"), bg_c=BLACK, tx_c=WHITE):
	w = WIDTH * 0.6
	h = HEIGHT * 0.2
	x = (WIDTH - w) / 2
	y = (HEIGHT - h) / 2
	pop_up(DATA, DISPLAY, msg, mode, x, y, w, h, show_time, bg_c, tx_c)


# Display a small pop-up window over the middle of the screen
def large_pop_up(DATA, DISPLAY, msg, mode, show_time=float("inf"), bg_c=BLACK, tx_c=WHITE):
	w = WIDTH * 0.6
	h = HEIGHT * 0.5
	x = (WIDTH - w) / 2
	y = (HEIGHT - h) / 2
	pop_up(DATA, DISPLAY, msg, mode, x, y, w, h, show_time, bg_c, tx_c)


def pop_up(DATA, DISPLAY, msg, mode, x, y, w, h, show_time=None, bg_c=BLACK, tx_c=WHITE):
	# DISPLAY.fill(BLACK)
	loop = True
	start_time = time()
	if BUTTON_TEXT_FONT is None:
		init_button_font()
	while DATA["mode"] == mode and loop:
		lines = msg.split("\n")
		r = pygame.Rect(x, y, w, h)
		to_blit = []
		length = max(2, len(lines))
		for i, line in enumerate(lines):
			text_surf, text_rect = text_objects(line, BUTTON_TEXT_FONT, tx_c)
			width, height = BUTTON_TEXT_FONT.size(line)
			text_rect.center = ((x + (w / 2)), (((i * height) + y) + (h / length)))
			to_blit.append((text_surf, text_rect))

		pygame.draw.rect(DISPLAY, bg_c, r)
		DISPLAY.blits(to_blit)
		pygame.display.update()
		# draw_display()
		loop = check_quit()
		if show_time is not None:
			curr_time = time()
			how_long = curr_time - start_time
			if how_long >= show_time:
				loop = False
	DATA["mode"] = IDLE
	DISPLAY.fill(BACKGROUND_COLOR)


def calculate_button_placement():
	x = 0
	y = 0
	max_height = float("-inf")
	for button, attrs in BUTTON_DATA.items():
		text, ac, *ic = attrs
		action = None
		if len(ic) > 1:
			action = ic[1]
			ic = ic[0]
		else:
			ic = ic[0]
		w, h = BUTTON_TEXT_FONT.size(text)
		h *= 2
		w = WIDTH / len(BUTTON_DATA)
		args = [text, x, y, w, h, ic, ac]
		if action:
			args += [action]
		BUTTON_DATA[button] = args
		x += w
		if h > max_height:
			max_height = h
	return WIDTH, max_height


def calculate_buckets():
	grid = DATA["grid"]
	rows = grid.rows
	cols = grid.cols
	width, height = DATA["grid_space"]
	b_width, b_height = DATA["button_space"]
	grid_width = (width / cols) - LINE_WIDTH
	grid_height = (height / rows) - LINE_WIDTH
	space = min(height, width)
	x = 0
	y = b_height + LINE_WIDTH
	if DRAW_SQUARE:
		x = (WIDTH - space) / 2
		grid_width = (space / cols) - LINE_WIDTH
		grid_height = (space / rows) - LINE_WIDTH
	buckets = []
	for r in range(rows):
		bucket_row = []
		for c in range(cols):
			bucket = pygame.Rect(x, y, grid_width, grid_height)
			x += grid_width + LINE_WIDTH
			bucket_row.append(bucket)
		if DRAW_SQUARE:
			x = (WIDTH - space) / 2
		else:
			x = 0
		y += grid_height + LINE_WIDTH
		buckets.append(bucket_row)
	return buckets


def init_file_handling():
	global load, save
	import file_handling
	save = file_handling.save
	load = file_handling.load
	BUTTON_DATA["save"][-1] = save
	BUTTON_DATA["load"][-1] = load


def init_display():
	global DISPLAY, CLOCK, DATA, WIDTH, HEIGHT, ROWS, COLS, DRAW_SQUARE, DRAW_BLOCK_IDX, USE_FULL_SCREEN, BUTTON_DATA, LINE_WIDTH

	# get user input
	USE_FULL_SCREEN = ask_use_full_screen()
	ROWS, COLS = ask_dimens()
	DRAW_SQUARE = ask_draw_square()
	DRAW_BLOCK_IDX = ask_draw_block_indexes()

	WIDTH, HEIGHT = DEFAULT_SIZE
	CLOCK = pygame.time.Clock()
	BUTTON_DATA = get_button_data()
	DATA = {}
	DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
	if USE_FULL_SCREEN:
		DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		WIDTH, HEIGHT = DISPLAY.get_size()

	pygame.display.set_caption(TITLE)
	button_space_width, button_space_height = calculate_button_placement()
	DATA["button_space"] = (button_space_width, button_space_height)
	DATA["grid_space"] = (WIDTH, HEIGHT - button_space_height)
	print("post init_display")


def init_data():
	DATA["grid"] = Map(ROWS, COLS)
	# DATA["grid"].set_start_node([1, 11])
	# DATA["grid"].set_end_node(random.randint(0, (ROWS*COLS)-1))

	DATA["modes"] = list(BUTTON_DATA) + [IDLE]
	DATA["mode"] = DATA["modes"][-1]
	DATA["buckets"] = calculate_buckets()
	init_file_handling()
	init_button_font()
	calc_block_idx_font()


# diaplay a button and listen for it to be clicked.
# acts as a controller to update the program mode as well.
# msg 		- 	button text
# x			-	button x
# y			-	button x
# w			-	button width
# h			-	button height
# ic		-	button color
# ac		-	button color when hovering
# action	-	function to be called on click
def draw_button(msg, x, y, w, h, ic, ac, action=None):
	global POP_UP_THREAD
	mouse = pygame.mouse.get_pos()
	click = tuple(pygame.mouse.get_pressed())

	if msg == DATA["mode"]:
		pygame.draw.rect(DISPLAY, SELECTION_COLOR, (x, y, w, h))
		x += SELECTION_WIDTH
		y += SELECTION_WIDTH
		w -= (2 * SELECTION_WIDTH)
		h -= (2 * SELECTION_WIDTH)

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
		if click[0] == 1:
			DATA["mode"] = msg
			kill_pop_up_thread()
			if action is not None:
				pool = ThreadPool(processes=1)
				print("action:", action)
				if action == reset:
					async_result = pool.apply_async(action, (click, DATA))
				elif action == save or action == load:
					async_result = pool.apply_async(action, (DATA, DISPLAY))
				else:
					async_result = pool.apply_async(action, ())
				f_args = async_result.get()
				if f_args:
					f, arg = f_args
					kill_pop_up_thread()
					POP_UP_THREAD = Thread(target=f, args=arg)
					POP_UP_THREAD.start()
				else:
					print("no function")

				# recalculate buckets on load
				if action == load:
					DATA["buckets"] = calculate_buckets()
					spl = "."
					arg_split = arg[2].split(spl)
					file_name = arg_split[0] + spl + arg_split[1][:4]
					pygame.display.set_caption(TITLE + file_name.rjust(120, " "))
					init_button_font()
					calc_block_idx_font()
				elif action == reset and sum(click) > 1:
					pygame.display.set_caption(TITLE)
					if sum(click) == 3:
						full_reset()

				event = pygame.event.wait()
	else:
		pygame.draw.rect(DISPLAY, ic, (x, y, w, h))

	BUTTON_TEXT_FONT.set_bold(True)
	text_surf, text_rect = text_objects(msg, BUTTON_TEXT_FONT)
	text_rect.center = ((x + (w / 2)), (y + (h / 2)))
	DISPLAY.blit(text_surf, text_rect)


def draw_solved_path():
	a_star = DATA["a*"]
	grid = DATA["grid"]
	buckets = DATA["buckets"]
	path = a_star.get_path()
	points = []
	for i in path:
		# print("block:", block, "cost:", cost)
		r, c = grid.get_block_r_c(i)
		x, y = buckets[r][c].center
		points.append((x, y))
		pygame.draw.circle(DISPLAY, WHITE, (x, y), 2)
	# print(points)
	pygame.draw.lines(DISPLAY, PATH_COLOR, False, points, 4)


# If the current mode is either stop or reset, then begin to wipe the grid
# for the next simulation.
def update_mode():
	m = DATA["mode"]
	if m == "reset":
		DATA["mode"] = IDLE
	if m == "stop":
		DATA["mode"] = "reset"
	if m == "pause":
		if "a*" in DATA and not DATA["a*"].solvable:
			DATA["mode"] = IDLE
	if m == "start":
		if DATA["a*"] and DATA["a*"].solved:
			DATA["mode"] = "pause"


def handle_mode():
	grid = DATA["grid"]
	m = DATA["mode"]
	if m == "start":
		search()
	elif m == "draw":
		bucket_click(symbol=LEGEND["block"], left_click=grid.set_block, right_click=grid.set_empty)
	elif m == "move_start":
		bucket_click(symbol=LEGEND["start"], left_click=grid.set_start, right_click=grid.set_empty)
	elif m == "move_end":
		bucket_click(symbol=LEGEND["end"], left_click=grid.set_end, right_click=grid.set_empty)


def init_a_star(mode):
	if "a*" not in DATA:
		grid = DATA["grid"]
		DATA["a*"] = A_Star(grid, mode)


def search():
	# print("\n\n\n\n\n\t\t\tSTART\n\n\n\n\n\n\n")
	grid = DATA["grid"]
	if manhattan in BUTTON_DATA:
		mode = False
	else:
		mode = True
	init_a_star(mode)
	a_star = DATA["a*"]
	valid = a_star.ready_to_solve() and a_star.solvable
	start_spaces = grid.get_spaces(LEGEND["start"])
	end_spaces = grid.get_spaces(LEGEND["end"])

	if valid and not a_star.solved:
		checked, cost = next(a_star.solve())
		# print("checked:", checked, "cost", cost)
		if checked < 0:
			msg = "No path found."
			a_star.solvable = False
			a_star.solved = True

			small_pop_up(
				DATA,
				DISPLAY,
				msg,
				"start",
				2.5,
				bg_c=PATH_NOT_FOUND_BACKGROUND_COLOR,
				tx_c=PATH_NOT_FOUND_TEXT_COLOR
			)

			return
		if checked not in end_spaces and checked not in start_spaces:
			grid.set_checked(checked, cost)
	else:
		DATA["mode"] = IDLE

	# create pop up message to notify user that path has been found
	if a_star.solved:
		draw_solved_path()
		POP_UP_THREAD = Thread(target=path_found_message, args=())
		POP_UP_THREAD.start()


def path_found_message():
	a_star = DATA["a*"]
	msg = "Path found!\n"
	path = a_star.get_path()
	n_per_line = 15
	split_path = [path[i: i + n_per_line] for i in range(0, len(path), n_per_line)]
	distance = a_star.get_path_distance()

	blocks_traversed = "\nBlocks traversed:"
	blocks_traversed_n = str(len(path) - 1)
	distance_travelled = "\nDistance travelled:"
	distance_travelled_n = "{:.2f}".format(distance)
	blocks = "\nNumber of blocks:"
	blocks_n = str(len(a_star.grid.get_spaces(LEGEND["block"])))
	starts = "\nNumber of start nodes:"
	starts_n = str(len(a_star.grid.get_spaces(LEGEND["start"])))
	ends = "\nNumber of end nodes:"
	ends_n = str(len(a_star.grid.get_spaces(LEGEND["end"])))
	checks = "\nNumber of nodes expanded:"
	checks_n = str(len(a_star.grid.get_spaces(LEGEND["checked"])))
	percentage_traversed = "\nPercentage of graph searched"
	percentage_traversed_n = "{:.2f} %".format(a_star.percentage_searched())  #((int(blocks_traversed_n) + 1) / DATA["grid"].size) * 100)
	path_travelled = "Path Travelled:"
	line_length = max(list(map(len, [blocks_traversed, distance_travelled, path_travelled, percentage_traversed, blocks, starts, ends, checks]))) + max(list(map(len, [blocks_traversed_n, distance_travelled_n, percentage_traversed_n]))) + 20

	blocks_traversed += blocks_traversed_n.rjust(line_length - len(blocks_traversed), " ")
	distance_travelled += distance_travelled_n.rjust(line_length - len(distance_travelled), " ")
	blocks += blocks_n.rjust(line_length - len(blocks), " ")
	starts += starts_n.rjust(line_length - len(starts), " ")
	ends += ends_n.rjust(line_length - len(ends), " ")
	checks += checks_n.rjust(line_length - len(checks), " ")
	percentage_traversed += percentage_traversed_n.rjust(line_length - len(percentage_traversed), " ")
	path_travelled = "\n\n" + path_travelled.rjust((line_length + len(path_travelled)) // 2, " ") + "\n\n"
	for line in split_path:
		path_travelled += ", ".join(list(map(str, line))).strip() + "\n"

	msg = msg.rjust((line_length + len(msg)) // 2, " ")
	msg += blocks_traversed + distance_travelled + blocks + starts + ends + checks + percentage_traversed + path_travelled
	print("results line_length:\n\n" + str(line_length) + "\n", msg + "\n\n")
	message_window(msg, "Results")


# large_pop_up(DATA, DISPLAY, msg, "start", None, bg_c=PATH_FOUND_BACKGROUND_COLOR, tx_c=PATH_FOUND_TEXT_COLOR)


# Handle when the user clicks on the display. If the click is in bounds of a
# grid block then perform the given action based on the click type.
# The right click is reserved for deletion and therefore requires that the block
# clicked matches the given symbol.
def bucket_click(symbol=None, left_click=None, middle_click=None, right_click=None):
	grid = DATA["grid"]
	x, y = pygame.mouse.get_pos()
	l, m, r = pygame.mouse.get_pressed()
	buckets = DATA["buckets"]
	r_i, c_i = None, None
	for row in range(len(buckets)):
		for col in range(len(buckets[row])):
			rect = buckets[row][col]
			if x in range(rect.left, rect.right):
				if y in range(rect.top, rect.bottom):
					r_i = row
					c_i = col
					break
		if r_i is not None and c_i is not None:
			break

	if r_i is not None and c_i is not None:
		i = grid.get_block_index(r_i, c_i)
		if l and left_click:
			left_click(i)
		elif m and middle_click:
			middle_click(i)
		elif r and right_click:
			# only remove the symbol that the user is currently marking
			if grid.status[r_i][c_i][0] == symbol:
				right_click(i)


# Create and return text objects for blitting
def text_objects(text, font, color=BLACK):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()


def draw_grid():
	grid = DATA["grid"]
	status = grid.status
	rows = grid.rows
	cols = grid.cols
	width, height = DATA["grid_space"]
	space = min(width, height)
	b_width, b_height = DATA["button_space"]
	grid_width = (width / cols) - LINE_WIDTH
	grid_height = (height / rows) - LINE_WIDTH
	x = 0
	y = b_height + LINE_WIDTH
	if DRAW_SQUARE:
		x = (WIDTH - space) / 2
		grid_width = (space / cols) - LINE_WIDTH
		grid_height = (space / rows) - LINE_WIDTH
	for r in range(rows):
		for c in range(cols):
			rect = pygame.Rect(x, y, grid_width, grid_height)
			x += grid_width + LINE_WIDTH
			color = GRID_COLOR
			if status[r][c][0] == LEGEND["block"]:
				color = BLOCK_COLOR
			elif status[r][c][0] == LEGEND["start"]:
				color = START_BLOCK_COLOR
			elif status[r][c][0] == LEGEND["end"]:
				color = END_BLOCK_COLOR
			elif status[r][c][0] == LEGEND["checked"]:
				color = CHECKED_BLOCK_COLOR
			elif status[r][c][0] == LEGEND["looked_at"]:
				color = LOOKED_AT_BLOCK_COLOR
			pygame.draw.rect(DISPLAY, color, rect)

			if DRAW_BLOCK_IDX:
				msg = str(grid.get_block_index(r, c))
				smallText = DATA["block_idx_font"]
				textSurf, textRect = text_objects(msg, smallText)
				textRect.center = ((rect.x + (rect.width / 2)), (rect.y + (rect.height / 2)))
				DISPLAY.blit(textSurf, textRect)

		if DRAW_SQUARE:
			x = (WIDTH - space) / 2
		else:
			x = 0
		y += grid_height + LINE_WIDTH

	# draw path if it has been found
	if "a*" in DATA:
		if DATA["a*"].solved and DATA["a*"].solvable:
			draw_solved_path()


def init_button_font():
	global BUTTON_TEXT_FONT
	if BUTTON_TEXT_FONT is None:
		BUTTON_TEXT_FONT = pygame.font.SysFont("arial", 16)


def calc_block_idx_font():
	width, height = DATA["grid_space"]
	rows = DATA["grid"].rows
	cols = DATA["grid"].cols
	grid_height = (height / rows) - LINE_WIDTH
	grid_width = (width / cols) - LINE_WIDTH
	DATA["block_idx_font"] = pygame.font.SysFont("arial", int(min(grid_width, grid_height) * 0.85))


def draw_display():
	DISPLAY.fill(BLACK)
	# draw buttons
	for button, args in BUTTON_DATA.items():
		draw_button(*args)

	# only draw the background when a pop-up isnt being shown
	if isinstance(POP_UP_THREAD, Thread):
		if POP_UP_THREAD.is_alive():
			return

	draw_grid()
	pygame.display.update()


def check_quit(loop=True):
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			loop = False
	if not loop:
		DATA["mode"] = "stop"
		kill_pop_up_thread()
	return loop


def play():
	loop = True
	prev = None
	while loop:
		if DATA["mode"] != prev:
			prev = DATA["mode"]
			print("mode:", prev)

		draw_display()
		handle_mode()
		update_mode()
		CLOCK.tick(20)
		loop = check_quit()

	quit()


def init_pygame():
	print("\n\nINIT PYGAME\n\n")
	global BUTTON_TEXT_FONT
	pygame.init()
	BUTTON_TEXT_FONT = pygame.font.SysFont("arial", 16)


def init():
	if pygame.get_init():
		print("\n\nnQUIT PYGAME\n\n")
		pygame.display.quit()
	# pygame.quit()  # do not quit pygame here
	init_pygame()
	init_display()
	init_data()
	play()


if __name__ == "__main__":
	init()
