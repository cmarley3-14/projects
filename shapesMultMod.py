def line(p1,p2): # p1 and p2 are tuples of points
	penup()
	goto(p1)
	pendown()
	goto(p2)
	penup()
	
def loc(pnt, div, rad):
	x = rad*cos(2*pi*pnt/div) # x = r*cos(ϴ)
	y = rad*sin(2*pi*pnt/div) # y = r*sin(ϴ)
	# ϴ... 2π radians to a circle, we go a fraction around.
	return (x,y)

def main(multiplier, divisions=200, radius=200, times=1):
	'''
        if divisions > 500:
		divisions = 500
	if radius > 200:
		radius = 200
	if abs(multiplier) < .1:
		quit()
	if abs(multiplier) < 1 and times == 1:
		times = 1/abs(multiplier)
        '''
	hideturtle()
	penup()
	goto(0,-radius)
	pendown()
	circle(radius)
	pencolor('#{:06x}'.format(randrange(0,256**3)))
	for tick in range (1,int(times*divisions)+1):
		final = multiplier*tick
		a = loc(tick, divisions, radius)
		b = loc(final, divisions, radius)
		line(a,b)
		update()

'''
    This idea came after watching a Mathologer video on making
    drawings by defining points equidistant on a circle, looping
    through each, multiplying it by some number, and connecting the dots.

    We start at tick 1. Where it lands is based off tick*multiplier.
    'a' and 'b' are used to find the location of these points on the circle
    based off of the circle's radius, and how many ticks we've divided
    the circle up into. Then, we draw a line between those two points.
'''
    

from turtle import *
from math import pi, sin, cos
from random import randrange
from time import sleep
tracer(0,0)
''' Remember to set 'times' to the denominator of 'multiplier' '''
#main(.8, divisions = 100, times=5)
#main(34, 500)
#main(.4, 100, 250, 5)
while True:
        div = randrange(1,3)
        main(randrange(2,40)/div, 240, 320, div)
        sleep(2)
        clear()
