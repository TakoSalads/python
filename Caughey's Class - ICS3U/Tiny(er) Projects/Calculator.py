# Kyle Button
# 29/02/24
#Purpose: To create a program that will act as a calculator for the user

from time import sleep

RED = '\033[1;31;48m'
BLACK = '\033[30m'
RESET= '\033[0m'

gameNum = 1
gameOver = False

print(f"\n{BLACK}Running Calculator\n{RESET}")


while not gameOver:  # start of calculator

    def add(a, b):
        return a + b

    def subtract(a, b):
        return a - b

    def multiply(a, b):
        return a * b

    def divide(a, b):
        return a / b

    print(f"\n{BLACK}What would you like to Calculate")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
  
    while (True):
    
        choice = input("Enter choice(A/S/M/D): ").upper()
        
        if choice in ('A', 'S', 'M', 'D'):
            break
        else:
            print("Invalid Input")

    while True:
        try:  #try to convert the input to an integer
            num1 = float(input("Enter first number: "))
        except ValueError:
            # this code is executed if they did not enter an integer
            print( ' *** you did not enter an integer!\n' )
        else :
            break

      
    while True:
        try:  #try to convert the input to an integer
            num2 = float(input("Enter second number: "))
        except ValueError:
            # this code is executed if they did not enter an integer
            print( ' *** you did not enter an integer!\n' )
        else :
            break

    if choice == 'A':
        print(add(num1, num2))
    elif choice == 'S':
        print(subtract(num1, num2))
    elif choice == 'M':
        print(multiply(num1, num2))
    elif choice == 'D':
        print(divide(num1, num2))


    while True:  # top of error trapping loop
        again = input('Would you like to make another calculation? (enter `y` or `n`): ')
        if again in ('y', 'n'):
            break
        print(' *** Bad value! only enter `y` or `n`!\n')

    if again == 'n':
        gameOver = True

    gameNum += 1

print(f"\n\n{RED}Thank you for calculating!")
