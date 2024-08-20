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


def calculator():
    #calcualting values
    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

    def multiply(a, b):
        return a * b

    def divide(a, b):
        return a / b

    



#varibles
    

root = Tk()
root.title("Currency Converter & Calculator")
root.geometry("600x500")


#visuals
L1 = Label(root, text="Currency Converter & Calculator")
Button1 = Button(root, text="ADD")
Button2 = Button(root, text="SUBTRACT")


#placements
L1.grid(row=2, column=1)
Button1(row=1, column=1)
Button2(row=1, column=2)



root.mainloop()
    