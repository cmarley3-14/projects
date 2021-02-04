from tkinter import *
from math import *
from operator import xor

class App(Frame):
    def __init__(self, master): # master = window
        super().__init__() # init Frame
        self.master = master

        self.L_message = Label(self.master,
                               text="This is a multipurpose calculator. You may " +
                               "leave no more than one non-asterisk field blank.\n" +
                               "You must specify interest rate. " +
                               "You can substitute cost/down for mortgage.\n" +
                               "ENTER MONETARY AMOUNTS WITHOUT A DOLLAR SIGN.")
        self.L_message.grid(row=0, column=0, columnspan=3,
                            padx=5, pady=2)
        self.L_warning = Label(self.master, text="")
        self.L_warning.grid(row=1, column=0, columnspan=3,
                            padx=5, pady=2)
        self.L_total = Label(self.master, text="Total Cost (ex. down): $0.00")
        self.L_total.grid(row=10, column=0, columnspan=3,
                          padx=5, pady=5)
        
        
        self.L_house = Label(self.master, text="**Cost of house: ")
        self.L_house.grid(row=2, column=0,
                            padx=5, pady=2)
        self.L_down = Label(self.master, text="**Down payment / percentage %: ")
        self.L_down.grid(row=3, column=0,
                            padx=5, pady=2)
        self.L_mortgage = Label(self.master, text="Mortgage amount: ")
        self.L_mortgage.grid(row=4, column=0,
                            padx=5, pady=2)
        self.L_interest = Label(self.master, text="Annual interest rate %: ")
        self.L_interest.grid(row=5, column=0,
                            padx=5, pady=2)
        self.L_payment = Label(self.master, text="Monthly payment: ")
        self.L_payment.grid(row=6, column=0,
                            padx=5, pady=2)
        self.L_months = Label(self.master, text="Mortgage period (mo.): ")
        self.L_months.grid(row=7, column=0,
                            padx=5, pady=2)

        self.E_house = Entry(self.master, width=50)
        self.E_house.grid(row=2, column=1, columnspan=2,
                            padx=5, pady=2)
        self.E_down = Entry(self.master, width=33)
        self.E_down.grid(row=3, column=1,
                            padx=5, pady=2)
        self.E_downPercent = Entry(self.master, width = 15)
        self.E_downPercent.grid(row=3, column=2,
                                padx=4, pady=2)
        self.E_mortgage = Entry(self.master, width=50)
        self.E_mortgage.grid(row=4, column=1, columnspan=2,
                            padx=5, pady=2)
        self.E_interest = Entry(self.master, width=50)
        self.E_interest.grid(row=5, column=1, columnspan=2,
                            padx=5, pady=2)
        self.E_payment = Entry(self.master, width=50)
        self.E_payment.grid(row=6, column=1, columnspan=2,
                            padx=5, pady=2)
        self.E_months = Entry(self.master, width=50)
        self.E_months.grid(row=7, column=1, columnspan=2,
                            padx=5, pady=2)

        self.B_calc = Button(self.master, text="Calculate", command=self.calculate)
        self.B_calc.grid(row=8, column=0, columnspan=3,
                            padx=5, pady=2)


    def calculate(self):
        self.L_warning.config(text="")
        house = self.str_float(self.E_house.get())
        down = self.str_float(self.E_down.get())
        downPercent = self.str_float(self.E_downPercent.get())/100
        mortgage = self.str_float(self.E_mortgage.get())
        interest = self.str_float(self.E_interest.get())/1200
        payment = self.str_float(self.E_payment.get())
        months = self.str_float(self.E_months.get())
        if down or downPercent:
            if down == 0:
                down = downPercent*house
                self.E_down.insert(0,down)
            else:
                downPercent = down/house
                self.E_downPercent.insert(0,(round(downPercent*100, 3)))
        if ((house and down) or mortgage):
            if mortgage == 0:
                mortgage = house - down
                self.E_mortgage.insert(0,mortgage)
        else:
            if (interest and payment and months):
                pass
            else:
                self.L_warning.config(text="ERROR: Not enough values for calculations!")
                return
            
        if not interest:
            self.L_warning.config(text="ERROR: Please specify an interest rate!")
        if (mortgage and payment and months):
            self.L_warning.config(text="ERROR: Please leave a pound field to calculate!")
            return
        if not (mortgage or payment or month):
            self.L_warning.config(text="ERROR: Please include all necessary details!")
            return
        
        if not xor(mortgage!=0, xor(payment!=0, months!=0)): #condensed, and b/c xor req's bool
            if not mortgage:
                mortgage = payment*((1+interest)**months-1)/(interest*(1+interest)**months)
                self.E_mortgage.insert(0,"{:,.2f}".format(mortgage))
                if house:
                    down = house - mortgage
                    self.E_down.insert(0,"{:,.2f}".format(down))
                    downPercent = down/house
                    self.E_downPercent.insert(0,(round(downPercent*100, 3)))
                amount = payment*months
                self.L_total.config(text="Total Cost (ex. down): ${:,.2f}".format(amount))
            if not payment:
                payment = (mortgage*(1+interest)**months)*interest/((1+interest)**months-1)
                self.E_payment.insert(0,"${:,.2f}".format(payment))
                amount = payment*months
                self.L_total.config(text="Total Cost (ex. down): ${:,.2f}".format(amount))
            if not months:
                if interest*mortgage >= payment:
                    self.L_warning.config(text="ERROR: Non-decreasing debt!")
                    self.L_total.config(text="Total Cost (ex. down): $∞∞∞∞∞∞∞∞.∞∞")
                else:
                    months = log(payment/(payment-interest*mortgage), 1+interest)
                    self.E_months.insert(0, months)
                    amount = payment*months
                    self.L_total.config(text="Total Cost (ex. down): ${:,.2f}".format(amount))
                    
    def str_float(self, var):
        try:
            if var == '':
                var = 0
            var = float(var)
            return var
        except:
            self.L_warning.config(text="ERROR: Please enter only numbers into the fields!")


root = Tk()
myApp = App(root)
myApp.mainloop()
        
