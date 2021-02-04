from tkinter import *
import numpy as np

class App(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.label = Label(self.master,
                           text="Ax + By + Cz + ... = n")
        self.label.grid(row=0, column=1, columnspan=11)
        self.scale = Scale(self.master, from_=2, to=10,
                           length=300,command = self.resize)
        self.scale.grid(row=2, column=0, rowspan=9)
        self.entries=[Entry(self.master, width=10) for i in range (110)]
        for i in range (110):
            self.entries[i].grid(row=1+i//11, column=1+i%11)
            self.entries[i].insert(0,"0")
        self.calculate = Button(self.master, text="Calculate", command = self.reduce)
        self.calculate.grid(row=12,column=0)
        self.v=2
        self.resize(2)

    def resize(self, size):
        size=int(size)
        self.v=size
        for entry in self.entries:
            entry.config(state='disabled')
        for i in range (size*(size+1)):
            self.entries[11*(i//(size+1))+i%(size+1)].config(state='normal')

    def reduce(self):
        matrix = []
        for y in range (self.v):
            row = []
            for x in range (self.v+1):
                row.append(float(self.entries[11*y+x].get()))
            matrix.append(row)
        fin = self.rref(matrix)
        for y in range (self.v):
            for x in range (self.v+1):
                self.entries[11*y+x].delete(0, END)
                self.entries[11*y+x].insert(0, fin[y][x])

    def rref(self, matrix): 
        A = np.array(matrix, dtype=np.float64)

        i = 0 # row
        j = 0 # column
        while True:
            # find next nonzero column
            while all(A.T[j] == 0.0):
                j += 1
                # if reached the end, break
                if j == len(A[0]) - 1 : break
            # if a_ij == 0 find first row i_>=i with a 
            # nonzero entry in column j and swap rows i and i_
            if A[i][j] == 0:
                i_ = i
                while A[i_][j] == 0:
                    i_ += 1
                    # if reached the end, break
                    if i_ == len(A) - 1 : break
                A[[i, i_]] = A[[i_, i]]
            # divide ith row a_ij to make it a_ij == 1
            A[i] = A[i] / A[i][j]
            # eliminate all other entries in the jth column by subtracting
            # multiples of of the ith row from the others
            for i_ in range(len(A)):
                if i_ != i:
                    A[i_] = A[i_] - A[i] * A[i_][j] / A[i][j]
            # if reached the end, break
            if (i == len(A) - 1) or (j == len(A[0]) - 1): break
            # otherwise, we continue
            i += 1
            j += 1

        return A.tolist()
        
root = Tk()
myApp = App(root)
myApp.mainloop()
