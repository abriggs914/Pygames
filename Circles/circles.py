import pygame
import random as rand
import math
from time import sleep

# Circle drawing

##################################################
##					Design vars					##
##################################################

CIRCLE_MARKER_COLOR = (255, 255, 255) # white
BACKGROUND_COLOR = (0, 0, 0) # black
CIRCLE_MARKER_SIZE = 10
CIRCLE_BORDER_SIZE = 3
SCREEN_PROPORTION = 0.85

##################################################
##					Game vars					##
##################################################

WIDTH = 750
HEIGHT = 750
ROWS = 12
COLS = 12
RPM = 100
DISPLAY = None
TITLE = "Circles"
DATA = {}
FOLLOW_MOUSE = False
MARK_CENTER = True
CLOCK = pygame.time.Clock()
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
		a = 180 - a #(90 - a) + 90
	# Quadrant 3 - Cartesian 2
	if delta_y < 0 and delta_x < 0:
		a += 180
	# Quadrant 4 - Cartesian 1
	if delta_y < 0 and delta_x >= 0:
		a = 360 - a #(90 - a) + 270
	return (a)
	
def compute_distance(x1, y1, x2, y2):
	return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5
	
def compute_col_space():
	return (WIDTH / COLS) * SCREEN_PROPORTION
	
def compute_row_space():
	return (HEIGHT / ROWS) * SCREEN_PROPORTION

def compute_radius():
	return min(round(DATA["col_space"] / 2), round(DATA["row_space"] / 2))
	
def compute_spacing():
	return min(round(DATA["col_space"]), round(DATA["row_space"]))
	
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
	
def set_circles():
	radius = DATA["radius"]
	circumference = 2 * math.pi * radius
	slice_space = round(360 / max(ROWS, COLS))# 1 #round(circumference / max(ROWS, COLS))
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
					
				# pygame.draw.circle(DISPLAY, (255,255,255), (circle.x, circle.y), 5)
				# pygame.draw.circle(DISPLAY, (255,85,85), (circle.marker_x, circle.marker_y), 3)
				# pygame.display.update()
				# sleep(1)
				
				

				# print("circle:", circle)
				# x = circle.x
				# y = circle.y
				# rect = pygame.Rect(x-radius, y-radius, (2*radius), (2*radius))
				# marker_x = rect.left + (((2*radius) * r) % rect.width)
				# marker_y = rect.top + ((((2*radius)) * c) % rect.height)
				# print("r:", r, "c:", c, "marker_x:", marker_x, "marker_y:", marker_y)
				# circle.set_marker_circuference(marker_x, marker_y)
			else:
				top_circle_x = DATA["circles"][0][c].marker_x
				left_circle_y = DATA["circles"][r][0].marker_y
				rect = pygame.Rect(top_circle_x-radius, left_circle_y-radius, (2*radius), (2*radius))
				marker_x = rect.left + ((slice_space * max(c, r)) % rect.width)
				marker_y = rect.top + ((slice_space * max(r, c)) % rect.height)
				#print("marker_x:", marker_x, "marker_y:", marker_y)
				circle.set_marker_circumference(marker_x, marker_y)
				
			
def update_circles():
	radius = DATA["radius"]
	circumference = 2 * math.pi * radius
	slice_space = round(360 / max(ROWS, COLS))
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
				else:
					circle.set_marker_circumference(top_circle_x, left_circle_y)
				
				circle.add_draw_line()
				
				
				
				#vector = pygame.Vector2(abs(marker_x - x), abs(marker_y - y))
				#vector.rotate(1)
				#new_x = vector.x
				#new_y = vector.y
				#print("new_x", new_x, ",new_y:", new_y)
				#circle.set_marker(new_x, new_y)
				
				
				
				
				# rect = pygame.Rect(x-radius, y-radius, (2*radius), (2*radius))
				# end_x, end_y = circle.end_point
				# new_x, new_y = circle.end_point
				# message = ""
				# # left
				# if end_x <= rect.left:
					# # top_left
					# if end_y <= rect.top:
						# message += "top_left"
						# new_x += 1
					# # bottom_left
					# else:
						# message += "bottom_left"
						# end_y -= 1
				# # right
				# else:
					# # top_right
					# if end_y <= rect.top:
						# message += "top_right"
						# new_y += 1
					# # bottom_right
					# else:
						# message += "bottom_right"
						# new_x -= 1
				
				# # marker_x = rect.left + ((slice_space * max(c, r)) % rect.width)
				# # marker_y = rect.top + ((slice_space * max(r, c)) % rect.height)
				# # print("marker_x:", marker_x, "marker_y:", marker_y)
				# message += ", new_x: " + str(new_x) + ", new_y: " + str(new_y)
				# print(message)
				# circle.set_marker(new_x, new_y)	
	
def follow_mouse():
	cx, cy = pygame.mouse.get_pos()		
	for r in range(ROWS):
		for c in range(COLS):
			if MARK_CENTER:				
				DATA["circles"][r][c].set_marker_center(cx, cy)
			else:
				DATA["circles"][r][c].set_marker_circumference(cx, cy)
					
						
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