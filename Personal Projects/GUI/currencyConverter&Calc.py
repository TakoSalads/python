#Kyle Button
#08/20/24
#Purpose: conversion to CAD, USD, JYEN, GBP, KOR and calculator with AMDS

from tkinter import *

def convertor():
    #conversions based on USD value
    
    USD = 1
    CAD = 0.73
    YEN = 0.0069
    EURO = 0.90
    WON = 0.00075

def usdtocad():
    try:
        tobe = float(Entry1.get())
        Total = tobe * 0.73

        Answer.config(text=f"USD to CAD: {Total}")

    except ValueError:
        print("Invalid Input")

def usdtoyen():
    try:
        tobe = float(Entry1.get())
        Total = tobe * 0.0069

        Answer.config(text=f"USD to Japanese Yen: {Total}")

    except ValueError:
        print("Invalid Input")

def usdtoEuro():
    try:
        tobe = float(Entry1.get())
        Total = tobe * 0.90

        Answer.config(text=f"USD to Euro: {Total}")

    except ValueError:
        print("Invalid Input")

def usdtoWon():
    try:
        tobe = float(Entry1.get())
        Total = tobe * 0.00075

        Answer.config(text=f"USD to Chinese Won: {Total}")

    except ValueError:
        print("Invalid Input")


#calcultor ---

def add():
    try:
        num1 = float(Entry1.get())
        num2 = float(Entry2.get())

        Total = num1 + num2
        Answer.config(text=f"Total: {Total}")

    except ValueError:
        print("Invalid Input")
    
def subtract():
    try:
        num1 = float(Entry1.get())
        num2 = float(Entry2.get())

        Total = num1 - num2
        Answer.config(text=f"Total: {Total}")

    except ValueError:
        print("Invalid Input")

def multiply():
    try:
        num1 = float(Entry1.get())
        num2 = float(Entry2.get())

        Total = num1 * num2
        Answer.config(text=f"Total: {Total}")

    except ValueError:
        print("Invalid Input")

def divide():
    try:
        num1 = float(Entry1.get())
        num2 = float(Entry2.get())

        Total = num1 / num2
        Answer.config(text=f"Total: {Total}")

    except ValueError:
        print("Invalid Input")


#varibles

root = Tk()
root.title("Currency Converter & Calculator")
root.geometry("600x500")


#visuals
L1 = Label(root, text="Currency Converter & Calculator")
Button1 = Button(root, text="Add", command=add)
Button2 = Button(root, text="Subtract", command=subtract)
Button3 = Button(root, text="Multiply", command=multiply)
Button4 = Button(root, text="Divide", command=divide)
Entry1 = Entry(root)
Entry2 = Entry(root)
Answer = Label(root, text="Answer will display here")
Button5 = Button(root, text="CAD", command=usdtocad)
Button6 = Button(root, text="Yen", command=usdtoyen)
Button7 = Button(root, text="Euro", command=usdtoEuro)
Button8 = Button(root, text="Won", command=usdtoWon)



#placements
L1.grid(row=1, column=2)
Button1.grid(row=2, column=1)
Button2.grid(row=3, column=1)
Button3.grid(row=4, column=1)
Button4.grid(row=5, column=1)
Entry1.grid(row=2, column=2)
Entry2.grid(row=3, column=2)
Answer.grid(row=4, column=2, pady=20)
Button5.grid(row=2, column=3)
Button5.grid(row=3, column=3)
Button5.grid(row=4, column=3)
Button5.grid(row=5, column=3)




root.mainloop()
    