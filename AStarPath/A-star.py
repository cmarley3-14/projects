# A* pathfinder algorithm

from tkinter import *
from os import path

class App(Frame):
    def __init__(self, master):
        self.master = master
        self.master.resizable(False, False)
        super().__init__()
        self.help = Label(self.master, text=
                          "R-click-drag for obstacles, L-click-drag to remove")
        self.help.grid(row=0,column=0,columnspan=4,sticky="news")
        self.canvas = Canvas(self.master, width=510, height=510,
                             bg="white")
        self.canvas.grid(row=1,column=0,columnspan=4)
        self.b_solve = Button(self.master, text="SOLVE", command=self.solve)
        self.b_solve.grid(row=2, column=0, columnspan=2, sticky="news")
        self.e_filename = Entry(self.master, relief=FLAT)
        self.e_filename.insert(0,"Enter load/save filename here.")
        self.e_filename.grid(row=2,column=2,sticky="news",padx=5)
        self.sv_help = StringVar()
        self.l_help = Label(self.master, textvariable=self.sv_help)
        self.l_help.grid(row=2,column=3)
        self.b_clear = Button(self.master, text="CLEAR", command=self.clear)
        self.b_clear.grid(row=3, column=0, sticky="news")
        self.b_reset = Button(self.master, text="RESET", command=self.reset)
        self.b_reset.grid(row=3, column=1, sticky="news")
        self.b_load = Button(self.master, text="LOAD MAZE", command=self.load)
        self.b_load.grid(row=3, column=2, sticky="news")
        self.b_save = Button(self.master, text="SAVE MAZE", command=self.save)
        self.b_save.grid(row=3, column=3, sticky="news")
        self.blocks = [] # all the blocks in the grid
        
        for y in range (0, 50): # the coordinate system  is (0,0) to (49,49)
            for x in range (0, 50):
                self.blocks.append(self.canvas.create_rectangle(10*x+5, 10*y+5,
                                                                10*x+15, 10*y+15, fill = "white"))
        self.canvas.itemconfig(52, fill="red")
        self.canvas.itemconfig(2449, fill="green")
        self.canvas.bind('<B1-Motion>', self.set_obstacle)
        self.canvas.bind('<B3-Motion>', self.remove_obstacle)

        self.start = (1,1)
        self.goal = (48,48) # immutable; x-y coordinates
        self.open = [Node(self.start, self.goal, self.start, None, 0)] # open nodes that can have children
        self.open_loc = [self.start]
        self.preclosed = [] # for when user is destroying and rebuilding obstacles
        self.closed = [] # for the program adding tuples. allows for "CLEAR" button.
        

    def set_obstacle(self,event):
        x, y = (event.x-5)//10, (event.y-5)//10
        if x > 49 or y > 49:
            return
        if not (x==y and (x==1 or x==48)):
            if (x,y) not in self.preclosed:
                self.canvas.itemconfig(self.blocks[x+y*50],fill="blue")
                self.preclosed.append((x,y))
        
    def remove_obstacle(self,event):
        x, y = (event.x-5)//10, (event.y-5)//10
        if x > 49 or y > 49:
            return
        if not (x==y and (x==1 or x==48)):
            if (x,y) in self.preclosed:
                self.canvas.itemconfig(self.blocks[x+y*50],fill="white")
                self.preclosed.remove((x,y))
        
    def solve(self):
        if len(self.open) > 0: # while there are still searchable nodes
            n = self.open[0] # find n with lowest "f"
            # why do i start from the end? most recently added node!
            for o in self.open:
                if o.get_f_moddir() < n.get_f_moddir():
                    n = o
            if n.loc == self.goal:
                self.trace_solution(n) # if goal, traceback path
                return
            else:
                for co in n.get_children():
                    if co not in self.preclosed + self.open_loc + self.closed: # if the open node already exists
                        self.open.append(Node(self.start, self.goal, co, n, n.l+1))
                        self.open_loc.append(co)
                self.open.remove(n)
                self.open_loc.remove(n.loc)
                self.closed.append(n.loc)
                if n.loc != self.start:
                    self.canvas.itemconfig(self.blocks[n.loc[0]+n.loc[1]*50], fill="#888888")
            self.canvas.after(1, self.solve)
            

    def trace_solution(self, n):
        if n.loc != self.start:
            if n.loc != self.goal:
                self.canvas.itemconfig(self.blocks[n.loc[0]+n.loc[1]*50],fill="#44FF00")
            n = n.p # get the parent node
            self.canvas.after(4, lambda : self.trace_solution(n))

            
    def clear(self):
        for i in range(len(self.blocks)):
            if (i%50,i//50) not in self.preclosed:
                self.canvas.itemconfig(self.blocks[i], fill="white")
        self.canvas.itemconfig(52, fill="red")
        self.canvas.itemconfig(2449, fill="green")
        self.open = [Node(self.start, self.goal, self.start, None, 0)]
        self.open_loc = [self.start]
        self.closed = []
        
    def reset(self):
        for block in self.blocks:
            self.canvas.itemconfig(block, fill="white")
        self.canvas.itemconfig(52, fill="red")
        self.canvas.itemconfig(2449, fill="green")
        self.open = [Node(self.start, self.goal, self.start, None, 0)]
        self.open_loc = [self.start]
        self.preclosed = []
        self.closed = []

    def save(self):
        infn = self.e_filename.get()
        if infn == "Enter load/save filename here.":
            self.sv_help.set("ERROR: Create filename")
            return
        if infn[-4:] != ".txt":
            infn += ".txt"
        if path.exists(infn):
            self.sv_help.set("ERROR: File exists")
            return
        try:
            infile = open(infn, 'w')
        except OSError:
            self.sv_help.set("ERROR: Filename rejected")
            return
        for i in range(len(self.blocks)):
            if (i%50,i//50) not in self.preclosed:
                infile.write('0')
            else:
                infile.write('1')
        infile.close()
        
    def load(self):
        infn = self.e_filename.get()
        if infn == "Enter load/save filename here.":
            self.sv_help.set("ERROR: Enter filename")
            return
        if infn[-4:] != ".txt":
            infn += ".txt"
        if not path.exists(infn):
            self.sv_help.set("ERROR: Does not exist")
            return
        try:
            infile = open(infn)
        except OSError:
            self.sv_help.set("ERROR: Filename rejected")
            return
        self.reset()
        data = infile.read()
        for i in range(len(data)):
            if data[i]=='1':
                self.canvas.itemconfig(self.blocks[i],fill="blue")
                self.preclosed.append((i%50,i//50))            
        infile.close()

class Node(): # NO DIAGONAL MOVES ALLOWED!
    def __init__(self, st, gl, loc, p, l): # all tuples, except parent and length
        self.st = st
        self.gl = gl
        self.loc = loc 
        self.p = p # yes, parents can be "None"
        self.l = l
        
    def get_children(self):
        c = [] # children
        c.append((self.loc[0]+1, self.loc[1])) if self.loc[0] != 49 else None
        c.append((self.loc[0], self.loc[1]+1)) if self.loc[1] != 49 else None
        c.append((self.loc[0]-1, self.loc[1])) if self.loc[0] != 0 else None
        c.append((self.loc[0], self.loc[1]-1)) if self.loc[1] != 0 else None
        
        return c

    def __str__(self):
        if self.p == None:
            return self.loc
        return "{} <-- {}".format(self.loc, self.p.loc)

    def __lt__(self, other):
        return self.get_f_moddir() < other.get_f_moddir()

    def get_f_radial(self):
        g = abs(self.loc[0]-self.st[0])+abs(self.loc[1]-self.st[1])
        h = abs(self.loc[0]-self.gl[0])+abs(self.loc[1]-self.gl[1])
        return g+h # combined rect distance from start and end
    
    def get_f_direct(self):
        return abs(self.loc[1]-self.loc[0]) # distance from diag line

    def get_f_moddir(self):
        # The best combos seem to be 172 and 101
        return 1*self.get_f_direct()+0*self.get_f_radial()+1*self.l

        
root = Tk()
myApp = App(root)
myApp.mainloop()
    
