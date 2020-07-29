import pygame
import math
import random as rand
from time import sleep

# Circle drawing
#
# July 2020
#
# Python program using pygame to draw a grid of circles to the screen and plot
# moving dots on either the circumference or the on the circles within the grid.
#
# Option to have the dots follow the mouse or use the top and left row and column
# as a legend where the dots lower in the grid are plotted using the x and y coordinates
# of the legend dot.
#
# Option to have the dots constrained to the circumference of the grid circles or
# can draw on the circle space. When the whole circle is used, it's path will be 
# drawn behind it.
#
# Therefore this program supports 4 states:
#	Dots follow mouse on circumference
#	Dots follow mouse within their circle
#	Dots follow legend on circumference
#	Dots follow legend within their circle
#
# Switch the FOLLOW_MOUSE and MARK_CENTER variables to change the state.

##################################################
##					Design vars					##
##################################################

CIRCLE_MARKER_COLOR = (255, 255, 255) 	# white
BACKGROUND_COLOR = (0, 0, 0) 			# black
CIRCLE_MARKER_SIZE = 10					# diameter of dot
CIRCLE_BORDER_SIZE = 3					# space of the grid circle color shown
SCREEN_PROPORTION = 0.85				# margin space for circle drawing

##################################################
##					Game vars					##
##################################################

DISPLAY = None							# Display surface
TITLE = "Circles"						# title
WIDTH = 750								# width and height
HEIGHT = 750
ROWS = 11								# Number of rows and columns
COLS = 11
DATA = {}								# Dictionary of; circle / radius / spacing data values
FOLLOW_MOUSE = False					# Control whether the mouse is followed or not
MARK_CENTER = True						# Control whether the whole grid circle holds the dot or just it's circumference
CLOCK = pygame.time.Clock()				# Clock and framerate
FRAME_RATE = 60

#######################################################################################################################

class Circle:

	def __init__(self, x, y, radius, color):
		self.x = round(x)
		self.y = round(y)
		self.radius = round(radius)
		self.color = color
		self.marker_x = None
		self.marker_y = None
		self.angle = None
		self.line = None
		
	def __repr__(self):
		return "CIRCLE: x: {x}, y: {y}, radius {r}, marker: {m}, ".format(x=self.x, y=self.y, r=self.radius, m=(self.marker_x, self.marker_y, self.angle))
		
	def set_marker_circumference(self, x, y):
		marker_x = round(x)
		marker_y = round(y)
		a = compute_angle(self.x, self.y, marker_x, marker_y)
		self.set_angle(a)
		
	def set_marker_center(self, x, y):
		circle_radius = self.radius
		dist = compute_distance(self.x, self.y, x, y)
		dist = min(dist, circle_radius)
		radius = dist - CIRCLE_BORDER_SIZE / 2
		a = compute_angle(self.x, self.y, x, y)
		self.marker_x = round(self.x + (radius * math.cos(math.radians(a))))
		self.marker_y = round(self.y + (radius * math.sin(math.radians(a))))
		self.angle = a
		
	# angle in degrees
	def set_angle(self, a):
		radius = self.radius - CIRCLE_BORDER_SIZE / 2
		self.marker_x = round(self.x + (radius * math.cos(math.radians(a))))
		self.marker_y = round(self.y + (radius * math.sin(math.radians(a))))
		self.angle = a
	
	def add_draw_line(self):
		if self.line is None:
			pt = (self.marker_x, self.marker_y)
			self.line = [pt, pt]
		else:
			pt = (self.marker_x, self.marker_y)
			if pt not in self.line:	
				self.line.append(pt)
	
	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
		pygame.draw.circle(surface, BACKGROUND_COLOR, (self.x, self.y), self.radius - CIRCLE_BORDER_SIZE)
		
		if self.marker_x and self.marker_y:
			pygame.draw.circle(surface, CIRCLE_MARKER_COLOR, (self.marker_x, self.marker_y), CIRCLE_MARKER_SIZE // 2)
		if self.line:
			pygame.draw.lines(surface, self.color, False, self.line, 1)


# return random RGB color
def gen_color():
	return (
		rand.randint(10, 245),
		rand.randint(10, 245),
		rand.randint(10, 245)
	)
	
# compute the angle of the right_angled triangle formed from a 
# given center point and cordinates x and y.
# Quadrants are specified to the 2D coordinate system where right
# is positive x direction and down is positive y direction.
# Returns the angle in degrees.
def compute_angle(cx, cy, x, y):
	opp = abs(y - cy)
	adj = abs(x - cx)
	if adj == 0:
		adj = 1
	a = math.degrees(math.atan(opp / adj))
	delta_x = x - cx
	delta_y = y - cy
	# Quadrant 2 - Cartesian 3
	if delta_x < 0 and delta_y >= 0:
		a = 180 - a
	# Quadrant 3 - Cartesian 2
	if delta_y < 0 and delta_x < 0:
		a += 180
	# Quadrant 4 - Cartesian 1
	if delta_y < 0 and delta_x >= 0:
		a = 360 - a
	return (a)
	
# Euclidian distance between two points
def compute_distance(x1, y1, x2, y2):
	return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
	
# Compute the total horizontal drawing distance.
def compute_col_space():
	return (WIDTH / COLS) * SCREEN_PROPORTION
	
# Compute the total vertical drawing space.
def compute_row_space():
	return (HEIGHT / ROWS) * SCREEN_PROPORTION

# Ensure that all circles will be the same size, given number of rows and columns.
def compute_radius():
	return min(round(DATA["col_space"] / 2), round(DATA["row_space"] / 2))
	
# Ensure that the spaces are even and will hold all circles.
def compute_spacing():
	return min(round(DATA["col_space"]), round(DATA["row_space"]))
	
# Create a list of Circle objects and calculate their areas, and coordinates.
def create_circles():
	width_margin = WIDTH * (1 - SCREEN_PROPORTION) // 2
	height_margin = HEIGHT * (1 - SCREEN_PROPORTION) // 2
	spacing = DATA["spacing"]
	radius = DATA["radius"]
	circles = []
	for r in range(ROWS):
		row = []
		for c in range(COLS):
			x = ((spacing * c) + radius) + width_margin
			y = ((spacing * r) + radius) + height_margin
			color = gen_color()
			circle = Circle(x, y, radius, color)
			row.append(circle)
		circles.append(row)
	return circles

# Initialize the DATA dictionary.
# Called immediately on run, before the main loop.
def init():
	global DISPLAY
	pygame.init()
	DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(TITLE)
	
	DATA["col_space"] = compute_col_space()
	DATA["row_space"] = compute_row_space()
	DATA["spacing"] = compute_spacing()
	DATA["radius"] = compute_radius()
	DATA["circles"] = create_circles()
	set_circles()
	
# Set the legend circle dots to equal spacing along each axis.
# This is only used to initialize the program.
def set_circles():
	radius = DATA["radius"]
	circumference = 2 * math.pi * radius
	slice_space = round(360 / max(ROWS, COLS))
	print("circumference: ", circumference, "slice_space: ", slice_space)
	for r in range(ROWS):
		for c in range(COLS):
			circle = DATA["circles"][r][c]
			if r == 0 or c == 0:
				if r == 0:
					circle.set_angle(c * round(360 / COLS))
				else:
					y = r * round(360 / ROWS)
					circle.set_angle(r * round(360 / ROWS))
			else:
				top_circle_x = DATA["circles"][0][c].marker_x
				left_circle_y = DATA["circles"][r][0].marker_y
				rect = pygame.Rect(top_circle_x-radius, left_circle_y-radius, (2*radius), (2*radius))
				marker_x = rect.left + ((slice_space * max(c, r)) % rect.width)
				marker_y = rect.top + ((slice_space * max(r, c)) % rect.height)
				circle.set_marker_circumference(marker_x, marker_y)
				
# Update the dot marker coordinates from the legend.
# Add a slice of space to each legend circle and
# re-map each of the the grid dots.
def update_circles():
	for r in range(ROWS):
		for c in range(COLS):
			circle = DATA["circles"][r][c]
			marker_x = circle.marker_x
			marker_y = circle.marker_y
			marker_a = circle.angle
			if r == 0 or c == 0:
				if r == 0:
					circle.set_angle((marker_a + 1) % 360)
				else:
					circle.set_angle((marker_a - 1) % 360)
			else:
				top_circle_x = DATA["circles"][0][c].marker_x
				left_circle_y = DATA["circles"][r][0].marker_y
				if MARK_CENTER:
					circle.set_marker_center(top_circle_x, left_circle_y)
					circle.add_draw_line()
				else:
					circle.set_marker_circumference(top_circle_x, left_circle_y)
	
def follow_mouse():
	cx, cy = pygame.mouse.get_pos()		
	for r in range(ROWS):
		for c in range(COLS):
			circle = DATA["circles"][r][c]
			if MARK_CENTER:				
				circle.set_marker_center(cx, cy)
				circle.add_draw_line()
			else:
				circle.set_marker_circumference(cx, cy)
						
def draw_circles():
	for r in range(0, ROWS):
		for c in range(0, COLS):
			circle = DATA["circles"][r][c]
			circle.draw(DISPLAY)
			
def draw_display():
	DISPLAY.fill(BACKGROUND_COLOR)
	draw_circles()
	pygame.display.update()


def main_loop():
	loop = True
	while loop:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				loop = False
			
		# circle markers will follow the mouse instead of legend
		if FOLLOW_MOUSE:
			follow_mouse()
		else:
			update_circles()
		
		draw_display()
		CLOCK.tick(FRAME_RATE)
	
	
if __name__ == "__main__":
	init()
	main_loop()