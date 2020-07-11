
import pygame
from time import sleep
import random
from grid import Map, A_Star, LEGEND

pygame.init()

# Python program using pygame to visualize an A* pathfinding algorithm

#################################################
##				   Design vars				   ##
#################################################

WIDTH = 900
HEIGHT = 600
ROWS = 50 #75
COLS = 50 #100
LINE_WIDTH = 1
SELECTION_WIDTH = 5
SCREEN_PROPORTION = 0.95								# Percentage of the screen used for drawing
BUTTON_TEXT_FONT = pygame.font.SysFont("arial", 16)

# Colors
BLACK = (0, 0, 0)
SELECTION_COLOR = (207, 150, 8)							# gold
BACKGROUND_COLOR = (0,0,0)								# black
GRID_COLOR = (65, 65, 65)								# dark gray
BLOCK_COLOR = (115, 115, 115)							# light gray
START_BLOCK_COLOR = (127, 237, 17)						# green
END_BLOCK_COLOR = (237, 17, 17)							# red
CHECKED_BLOCK_COLOR = (9, 215, 222)						# cyan
START_BUTTON_ACTIVE_COLOR = (0, 255, 0)					# bright green
START_BUTTON_INACTIVE_COLOR = (0, 185, 0)				# green
PAUSE_BUTTON_ACTIVE_COLOR = (250, 242, 0)				# bright yellow
PAUSE_BUTTON_INACTIVE_COLOR = (255, 198, 13)			# yellow
STOP_BUTTON_ACTIVE_COLOR = (255, 0, 0)					# bright red
STOP_BUTTON_INACTIVE_COLOR = (185, 0, 0)				# red
RESET_BUTTON_ACTIVE_COLOR = (0, 0, 200)					# bright blue
RESET_BUTTON_INACTIVE_COLOR = (0, 0, 135)				# blue
DRAW_BUTTON_ACTIVE_COLOR = (119, 190, 237)				# light blue
DRAW_BUTTON_INACTIVE_COLOR = (65, 171, 242)				# blue
MOVE_START_BUTTON_ACTIVE_COLOR = (165, 242, 65)			# blue
MOVE_START_BUTTON_INACTIVE_COLOR = (136, 242, 65)		# bright green
MOVE_END_BUTTON_ACTIVE_COLOR = (237, 71, 71)			# light red
MOVE_END_BUTTON_INACTIVE_COLOR = (204, 31, 31)			# dark r
ABOUT_BUTTON_ACTIVE_COLOR = (135, 7, 245)				# light purpleed
ABOUT_BUTTON_INACTIVE_COLOR = (94, 5, 171)				# purple
EUCLIDEAN_BUTTON_ACTIVE_COLOR = (255, 124, 18)			# orange
EUCLIDEAN_BUTTON_INACTIVE_COLOR =	(189, 88, 6)		# dark orange

#################################################
##				   Game vars				   ##
#################################################

DISPLAY = None
TITLE = "A* Pathfinding"
DATA = {}
CLOCK = pygame.time.Clock()
manhattan = "manhattan"
euclidean = "euclidean"

#################################################
##			    Button listeners			   ##
#################################################

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

BUTTON_DATA = {
	"about": ["about", ABOUT_BUTTON_ACTIVE_COLOR, ABOUT_BUTTON_INACTIVE_COLOR],
	"start": ["start", START_BUTTON_ACTIVE_COLOR, START_BUTTON_INACTIVE_COLOR],
	"pause": ["pause", PAUSE_BUTTON_ACTIVE_COLOR, PAUSE_BUTTON_INACTIVE_COLOR],
	"stop": ["stop", STOP_BUTTON_ACTIVE_COLOR, STOP_BUTTON_INACTIVE_COLOR],
	"reset": ["reset", RESET_BUTTON_ACTIVE_COLOR, RESET_BUTTON_INACTIVE_COLOR],
	"draw": ["draw", DRAW_BUTTON_ACTIVE_COLOR, DRAW_BUTTON_INACTIVE_COLOR],
	"move_start": ["move_start", MOVE_START_BUTTON_ACTIVE_COLOR, MOVE_START_BUTTON_INACTIVE_COLOR],
	"move_end": ["move_end", MOVE_END_BUTTON_ACTIVE_COLOR, MOVE_END_BUTTON_INACTIVE_COLOR],
	"euclidean": ["euclidean", EUCLIDEAN_BUTTON_ACTIVE_COLOR, EUCLIDEAN_BUTTON_INACTIVE_COLOR, switch_mode]
}					
		
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
		w = round(WIDTH / len(BUTTON_DATA))
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
	x = 0
	y = b_height + LINE_WIDTH
	buckets = []
	for r in range(rows):
		bucket_row = []
		for c in range(cols):
			bucket = pygame.Rect(x, y, grid_width, grid_height)
			x += grid_width + LINE_WIDTH
			bucket_row.append(bucket)
		x = 0
		y += grid_height + LINE_WIDTH
		buckets.append(bucket_row)
	return buckets
		
def init():
	global DISPLAY
	DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(TITLE)
	
	button_space_width, button_space_height = calculate_button_placement()
	DATA["button_space"] = (button_space_width, button_space_height)
	DATA["grid_space"] = (WIDTH, HEIGHT - button_space_height)
	
	DATA["grid"] = Map(ROWS, COLS)
	DATA["grid"].set_start_node([1, 11])
	DATA["grid"].set_end_node(random.randint(0, (ROWS*COLS)-1))
	
	DATA["modes"] = list(BUTTON_DATA) + ["idle"]
	DATA["mode"] = DATA["modes"][-1]
	DATA["buckets"] = calculate_buckets()
	
# diaplay a button a listen for it to be clicked.
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
	mouse = pygame.mouse.get_pos()
	click = tuple(pygame.mouse.get_pressed())

	if msg == DATA["mode"]:
		pygame.draw.rect(DISPLAY, SELECTION_COLOR, (x, y, w, h))
		x += SELECTION_WIDTH
		y += SELECTION_WIDTH
		w -= (2 * SELECTION_WIDTH)
		h -= (2 * SELECTION_WIDTH)
		
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(DISPLAY, ac, (x, y, w, h))
		if click[0] == 1:
			DATA["mode"] = msg
			if action is not None:
				action()
		if DATA["mode"] == "reset":
			reset(click)
		if DATA["mode"] == "about":
			print("about")
	else:
		pygame.draw.rect(DISPLAY, ic,(x,y,w,h))

	smallText = BUTTON_TEXT_FONT
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x+(w/2)), (y+(h/2)))
	DISPLAY.blit(textSurf, textRect)

# If the current mode is either stop or reset, then begin to wipe the grid
# for the next simulation.
def update_mode():
	m = DATA["mode"]
	if m == "reset":
		DATA["mode"] = "idle"
	if m == "stop":
		DATA["mode"] = "reset"
	if m == "pause":
		if DATA["a*"] and not DATA["a*"].solvable:
			DATA["mode"] = "idle"
	if m == "start":
		if DATA["a*"] and DATA["a*"].solved:
			DATA["mode"] = "pause"
		
def handle_mode():
	grid = DATA["grid"]
	modes = DATA["modes"]
	m = DATA["mode"]
	if m == "start":
		# print("solve the grid")
		search()
	# elif m == "pause":
		# print("pause the search")
	# elif m == "stop":
		# print("stop the search")
	elif m == "draw":
		bucket_click(symbol=LEGEND["block"], left_click=grid.set_block, right_click=grid.set_empty)
	elif m == "move_start":
		bucket_click(symbol=LEGEND["start"], left_click=grid.set_start, right_click=grid.set_empty)
	elif m == "move_end":
		bucket_click(symbol=LEGEND["end"], left_click=grid.set_end, right_click=grid.set_empty)
	else:
		pass
		# print("idle")
		
def reset(click):
	l, m, r = click
	if l:
		DATA["grid"].reset_search()
	if m:
		DATA["grid"].reset_search_blocks()
	if r:
		DATA["grid"].reset_clear()
		
def search():
	grid = DATA["grid"]
	if manhattan in BUTTON_DATA:
		mode = False
	else:
		mode = True
	DATA["a*"] = A_Star(grid, mode)
	a_star = DATA["a*"]
	valid = a_star.ready_to_solve() and a_star.solvable
	end_spaces = grid.get_spaces(LEGEND["end"])
	if valid and not a_star.solved:
		checked = next(a_star.solve())	
		if checked < 0:
			print("No path found.")
			a_star.solvable = False
			a_star.solved = True
			return
		if checked not in end_spaces:
			grid.set_checked(checked)	
			
	if a_star.solved:
		print("Path found!")
		
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
			if grid.status[r_i][c_i] == symbol:
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
	b_width, b_height = DATA["button_space"]
	grid_width = (width / cols) - LINE_WIDTH
	grid_height = (height / rows) - LINE_WIDTH
	x = 0
	y = b_height + LINE_WIDTH
	for r in range(rows):
		for c in range(cols):
			rect = pygame.Rect(x, y, grid_width, grid_height)
			x += grid_width + LINE_WIDTH
			color = GRID_COLOR
			if status[r][c] == LEGEND["block"]:
				color = BLOCK_COLOR
			elif status[r][c] == LEGEND["start"]:
				color = START_BLOCK_COLOR
			elif status[r][c] == LEGEND["end"]:
				color = END_BLOCK_COLOR
			elif status[r][c] == LEGEND["checked"]:
				color = CHECKED_BLOCK_COLOR
			pygame.draw.rect(DISPLAY, color, rect)
		x = 0
		y += grid_height + LINE_WIDTH
	
def draw_display():
	# draw buttons
	for button, args in BUTTON_DATA.items():
		draw_button(*args)
		
	draw_grid()
	pygame.display.update()
	
def play():
	global b, r, c
	loop = True
	blocked = []
	while loop:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				loop = False
				
		draw_display()
		handle_mode()
		update_mode()
		CLOCK.tick(60)

if __name__ == "__main__": 
	init()
	play()