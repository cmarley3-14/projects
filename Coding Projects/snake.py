from turtle import *
from math import *
from random import *
from time import *

def square(t, center, side, color):
    t.fillcolor(color)
    t.penup()
    t.goto(center[0]-side/2, center[1]+side/2)
    t.pendown()
    t.begin_fill()
    for i in range (4):
        t.fd(side)
        t.rt(90)
    t.end_fill()

heading = [10,0]
screen = Screen()

def up():
    global heading
    if heading != [0,-10]:
        heading = [0,10]
def down():
    global heading
    if heading != [0,10]:
        heading = [0,-10]
def right():
    global heading
    if heading != [-10,0]:
        heading = [10,0]
def left():
    global heading
    if heading != [10,0]:
        heading = [-10,0]
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(right, "Right")
screen.onkey(left, "Left")

snake = Turtle()
apple = Turtle()
board = Turtle()
ht(); snake.ht(); apple.ht(); board.ht()
square(board,(0,0),410,"white")
tracer(0,0)
# 410/2=205... bc boxes on mults of 10 : side = 5... 20 hash marks
sp = [[x,0] for x in range (-50,0,10)] #snake positions
for i in range(len(sp)):
    if i==(len(sp)-1):
        square(snake, sp[i], 10, "#00FF00")
    else:
        square(snake, sp[i], 10, "green")
    update()
    sleep(.02)
applepos = [randint(-19,19)*10, randint(-19,19)*10]
square(apple,applepos,10,"red")
end = False
while not end:
    screen.listen()
    snake.clear()
    sp.append([sp[len(sp)-1][0]+heading[0],sp[len(sp)-1][1]+heading[1]])
    if sp[len(sp)-1]!=applepos:
        del sp[0]
    while applepos in sp:
        applepos = [randint(-19,19)*10, randint(-19,19)*10]
        apple.clear()
        square(apple,applepos,10,"red")
    for i in range(len(sp)):
        if i==(len(sp)-1):
            square(snake, sp[i], 10, "#00FF00")
        else:
            square(snake, sp[i], 10, "green")
    if (abs(sp[len(sp)-1][0]) > 200 or abs(sp[len(sp)-1][1]) > 200):
        end = True
    if len(sp) == 1681:
        end = True
    if sp[len(sp)-1] in sp[:(len(sp)-1)]:
        end = True
    update()
    sleep(.05)

