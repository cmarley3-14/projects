from tkinter import *
from random import randint
from time import sleep

#Three classes: the bird, the obstacles, the game window.
#It's better than having one class being the entire game.

class Bird():
    def __init__(self, canvas):
        self.canvas = canvas
        self.yLoc = 200
        self.dYdT = -1 #So you can change gravity
        self.body = self.canvas.create_oval(190,190,210,210,
                                            fill='yellow',tags='bird')
        beakPoints = [205,195,215,200,205,205] #The triangle
        self.beak = self.canvas.create_polygon(beakPoints,
                                               fill='red',tags='bird')
    def move(self):
        self.canvas.move('bird', 0, self.dYdT)
        self.yLoc += self.dYdT
        if self.dYdT < 20:
            self.dYdT += 1
        if self.yLoc > 488:
            self.dYdT = 0 #Don't fall through the ground!
        if self.yLoc < 1: #Anti-ceiling!
            self.dYdT = 2
    def flight(self, event):
        if self.yLoc > 12:
            self.dYdT = -12 #Anti-gravity!
        

class Pillar():
    def __init__(self, canvas, height, first=False):
        if first:
            self.xLoc = 1000 #Buffer when game starts
        else:
            self.xLoc = 600
        self.dXdT = -5 #If you change this, you'll have to change score detection.
        self.canvas = canvas
        self.height = height
        self.upper = self.canvas.create_rectangle(self.xLoc,0,self.xLoc+50,height-65,
                                                  fill='green',outline='green')
        self.lower = self.canvas.create_rectangle(self.xLoc,height+65,self.xLoc+50,500,
                                                  fill='green',outline='green')
    def move(self):
        self.canvas.move(self.upper, self.dXdT, 0)
        self.canvas.move(self.lower, self.dXdT, 0)
        self.xLoc += self.dXdT

class App(Frame):
    def __init__(self, master):
        self.master = master
        super().__init__()
        self.label = Label(text="GAME BEGINS SOON!", font=("Comic Sans MS",24),
                           borderwidth = 2, relief='solid')
        self.label.grid(row=0,column=0, sticky='news')
        
        try:
            infile = open('flappyBird_high.txt','r')
            self.highScore = int(infile.readline())
            infile.close()
        except:
            self.highScore = 0
            
        self.high = Label(text="High Score: {}".format(self.highScore),
                          font=("Arial",24))
        self.high.grid(row=0,column=1, sticky='news')
        
        self.canvas = Canvas(height=500, width=600, bg='skyblue')
        self.canvas.grid(row=1, column=0, columnspan=2)
        self.grass = self.canvas.create_rectangle(0,450,600,500,
                                     fill='limegreen',outline='green')
        
        self.bird = Bird(self.canvas)
        self.master.bind('<Key>', self.bird.flight)
        self.p1 = Pillar(self.canvas, 200, True)
        #The first pillar is set to location 1000 to allow for buffer time.
        self.pillars = [self.p1]
        self.score = 0
        self.main_game()

    def main_game(self):
        self.bird.move()
        rand = randint(100,400)
        if self.pillars[0].xLoc < 300:
            self.pillars.insert(0,Pillar(self.canvas,rand))
        for pillar in self.pillars:
            pillar.move()
            if pillar.xLoc < 161 and pillar.xLoc > 156:
                self.score += 1
                if self.score > self.highScore:
                    self.highScore = self.score + 0
                self.label.config(text="Score: {}".format(self.score))
                self.high.config(text="High Score: {}".format(self.highScore))
            if pillar.xLoc < -50:
                self.pillars.remove(pillar)
                
        #touches = list(self.canvas.find_overlapping(190,self.bird.yLoc-10,210,self.bird.yLoc+10))
        try:
            uCx1, uCy1, uCx2, uCy2 = self.canvas.coords(self.pillars[1].upper)
            lCx1, lCy1, lCx2, lCy2 = self.canvas.coords(self.pillars[1].lower)
        except:
            uCx1, uCy1, uCx2, uCy2 = self.canvas.coords(self.pillars[0].upper)
            lCx1, lCy1, lCx2, lCy2 = self.canvas.coords(self.pillars[0].lower)
        upCross = self.canvas.find_overlapping(uCx1,uCy1, uCx2,uCy2)
        loCross = self.canvas.find_overlapping(lCx1,lCy1, lCx2,lCy2)
        #Overlapping with bird coordinates creates false positives.
        if (2 in upCross) or (2 in loCross): #And if the bird's id is in there, kill the game.
            if self.score == self.highScore:
                infile = open('flappyBird_high.txt','w')
                infile.write(str(self.highScore))
                infile.close()
            sys.exit()
        self.after(30, self.main_game) #Game update speed.
        
root = Tk()
myApp = App(root)
myApp.mainloop()
