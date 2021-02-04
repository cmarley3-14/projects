from turtle import *
from math import *
from random import randint, random

def drawTriangle(sideLength, turtle):
    turtle.hideturtle()
    turtle.penup()
    #turtle.goto(-sideLength/2, -sideLength/sqrt(12)) #sqrt 12 b/c 2*sqrt3
    turtle.goto(-sideLength/2, -sideLength*sqrt(3)/4)
    turtle.pendown()
    for i in range(3):
        turtle.fd(sideLength)
        turtle.lt(120)
    turtle.penup()
    '''return ((-sideLength/2, -sideLength/sqrt(12)),
            (sideLength/2, -sideLength/sqrt(12)),
            (0, sideLength/sqrt(3)))'''
    return ((-sideLength/2, -sideLength*sqrt(3)/4),         # Returns a tuple containing
            (sideLength/2, -sideLength*sqrt(3)/4),          # the vertices of the triangle.
            (0, sideLength*sqrt(3)/4))                      # Difference is in y-position on screen.

def midpoint(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return (0.5*(x0+x1), 0.5*(y0+y1))

def main(size, iterations, turtle):
    if size > 750:
        size = 750
    vertices = drawTriangle(size, turtle)
    seedX = random()
    seedY = random()
    initX = (0.5 - seedX)*size
    #initY = ((0.5*size - abs(initX))*sqrt(3))*seedY - 0.5*size/sqrt(3)
    initY = ((0.5*size - abs(initX))*sqrt(3))*seedY - 0.25*size*sqrt(3)
    # initY takes initX and creates a vertical line of possible possitions in a triangle.
    # Then, seedY is a random decimal, which specifies a position on said line
    # and the position is shifted accordingly inside the triangle.
    newPoint = (initX, initY)
    turtle.goto(initX, initY)
    turtle.dot(4, 'green')
    for i in range(iterations):
        vertex = randint(0,2)
        newPoint = midpoint(newPoint, vertices[vertex])
        turtle.goto(newPoint)
        if i % 2 == 0:
            turtle.dot(3, 'red')
        else:
            turtle.dot(3, 'blue')
        if i % 400 == 0:
            update()
    turtle.goto(size/2,size/2)
    turtle.showturtle()
    update()
    
tracer(0,0)
t = Turtle()
main(750, 10000, t)
