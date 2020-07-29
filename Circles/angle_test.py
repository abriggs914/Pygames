import math

center_x = 25
center_y = 25
radius = 10

def delta_x(x):
	return x - center_x
    
def delta_y(y):
	return y - center_y
    
def toa(opp, adj):
	if adj == 0:
		adj = 1
	return math.degrees(math.atan(opp / adj))


for x in range(0, 50, 5):
	for y in range(0, 1, 5):
		print("x:", x, "y:", y, "t:", (toa(x, y)))