from tkinter import *
import random

#colours!
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
RESET= '\033[0m'

#functions
def guessField():
    global counter, max_guess, min_guess
    try:
        guess = int(E1.get())
        counter += 1
        
        #if guess is out of 1 - 10
        if guess > 10:
            var.set("Your Guess is too high: pick a number between 1 - 10")
            counter -= 1
        elif guess < 1:
            var.set("Your Guess is too low: pick a number between 1 - 10")
            counter -= 1
            
        #check if hint has been followed   
        elif guess >= max_guess:
            counter -= 1
            var.set(f"Your current guess is higher than your previous guess of: {max_guess}")
        elif guess <= min_guess:
            counter -= 1
            var.set(f"Your current guess is lower than your previous guess of: {min_guess}")


        #while guess is good!
        else:
            if guess == RNDMNUM:
                L2.configure(fg='green')
                var.set(f"Congratulations! You guessed the number correctly in {counter} attempts.")
                PAB.pack(pady=20)
                E1.pack_forget()
                GB.pack_forget()
            elif guess > RNDMNUM:
                var.set(f"Lower! - Current Guess: {counter}")
                max_guess = guess
            elif guess < RNDMNUM:
                var.set(f"Higher! - Current Guess: {counter}")
                min_guess = guess
                
                
        loser()
                
    #incase user error  
    except ValueError:
        var.set("Please enter a valid number")
        
        
def loser():
    global counter
    if counter > 5:
        L2.configure(fg='red')
        var.set("You've used all your guesses!")
        E1.pack_forget()
        GB.pack_forget()
        PAB.pack(pady=25)
        
        
#reset variables and visuals        
def playAgain():
    global gameOver, counter, RNDMNUM, min_guess, max_guess
    counter = 0
    L2.configure(fg='black')
    min_guess = 0
    max_guess = 11
    gameOver = False
    RNDMNUM = random.randint(1, 10)
    var.set('Guess a number between 1 and 10!')
    PAB.pack_forget()
    E1.delete(0, END)
    E1.pack(padx=100, pady=50)
    GB.pack(pady=20)
    
    
    
#root and window
root = Tk()
root.title("Random Number Guessing Game")
root.geometry("600x500")


#variables!
gameOver = False
counter = 0
gameNum = 0
RNDMNUM = random.randint(1, 10)
var = StringVar()
var.set('Guess a number between 1 and 10!')
max_guess = 11
min_guess = 0


#visuals
L1 = Label(root, text="Welcome to the guessing game!")
L2 = Label(root, textvariable=var)
E1 = Entry(root)
GB = Button(root, text="Submit Guess", command = guessField)
PAB = Button(root, text="Play Again", command=playAgain)
            
#placements            
L1.pack(padx=100, pady=25)
L2.pack(padx=100, pady=45)
E1.pack(padx=100, pady=50)
GB.pack(pady=20)

#needed
root.mainloop()



    