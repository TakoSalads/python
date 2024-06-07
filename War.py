#Kyle Button
#4/5/24
#Pupose: To create a program that will allow you to play the card game war against an AI

#06/02/2024 - Fixing up the code:
#Current issues with code
#👎 All attached files properly named (including name & project description)
#👎 Flowchart
#Coding style: - Good code but some inefficiencies or potential improvements
#Use of arrays - Adequate
#👎 All inputs error trapped appropriately
#👎 name/date/purpose at top
#Your mark could improve if you make some or all of the following improvements: - Error trap all inputs (within separate loops) - Fully document all aspects of your code - see feedback above - Fix the errors in the program
#
#Does not handle ties... so games never end. You do not error trap the variable answer... the game starts if you enter `g`... need a while loop around this

#imports
import random
import time
import os
from tkinter import *

#colours!
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'


#fuctions
def startGame():
    global p1card, c1card
    B1.pack_forget()

    cardTotal.set(f"STARTING UP")
    L4 = Label(root, textvariable=cardTotal)
    L4.pack(pady=10)

    cardDisplay.set(f"STARTING UP")
    L2 = Label(root, textvariable=cardDisplay)
    L2.pack(pady=10)

    winLoseOrTie.set(f"Starting up")
    L3 = Label(root, textvariable=winLoseOrTie)
    L3.pack(pady=10)

    def gameRound():
        global p1card, c1card
        if isThereAnyCards():
            return
        p1card = player.pop(0)
        c1card = computer.pop(0)
        compareHands()
        cardDisplay.set(
            f"Your card is {p1card} and the computers card is {c1card}")
        war()
        ptotal = int(len(player))
        ctotal = int(len(computer))
        cardTotal.set(f"PLayers Deck: {ptotal}      Computers Deck: {ctotal}")
        if not isThereAnyCards():
            root.after(5, gameRound)

    gameRound()


def war():
    global player_score, computer_score, p1card, c1card
    if result == 1:
        player_score += 1
        player.extend([p1card, c1card])
        winLoseOrTie.set(f"Player wins the round!")

    elif result == 2:
        computer_score += 1
        winLoseOrTie.set(f"Computer wins the round!")
        computer.extend([p1card, c1card])

    else:
        isThereATie()


def isThereATie():
    global p1card, c1card, player_score, computer_score, tiePile
    if result == 0:
        winLoseOrTie.set("The round was a Tie!")
        tiePile.append(c1card)
        tiePile.append(p1card)
        isThereAnyCards()
        p1card = player.pop(0)
        c1card = computer.pop(0)
        compareHands()
        cardDisplay.set(
            f"Your card is {p1card} and the computers card is {c1card}")

        if result == 1:
            player_score += 1
            winLoseOrTie.set("Player wins the tie")
            player.extend(tiePile + [p1card + c1card])

        elif result == 2:
            computer_score += 1
            winLoseOrTie.set("Computer wins the tie!")
            computer.extend(tiePile + [p1card + c1card])

        else:
            isThereATie()

    root.after(1000, isThereATie)


def playAgain():
    global gameNum, gameOver, counter
    while True:
        again = input('\n Would you like to play? (enter `y` or `n`): ')
        if again in ('y', 'n'):
            break
        print(f'\n{RED}*** Bad value! Please enter `y` or `n`! ***{RESET}\n')

    if again == 'n':
        gameOver = True
        os.system('clear')
        print(f"\n{BLACK}Thanks for playing!{RESET}")

    if again == 'y':
        gameNum += 1
        counter = 0
        os.system('clear')
        print(f"\n{BLACK}Running Round #{gameNum}\n{RESET}")


def compareHands():
    global p1card, c1card, result
    if int(p1card) > int(c1card):
        result = 1
    elif int(p1card) < int(c1card):
        result = 2
    else:
        result = 0


def isThereAnyCards():
    global computer
    global player
    global gameOver

    if len(player) == 0:
        cardDisplay.set(f"Player has no cards left!")
        winLoseOrTie.set(f"**** -DEFEAT- COMPUTER WINS ****")
        playAgain()

        return True

    if len(computer) == 0:
        cardDisplay.set(f"Computer has no cards left!")
        winLoseOrTie.set(f"**** CONGRATULATIONS YOU WIN  ****")
        playAgain()
        return True

    return False


#root and window
root = Tk()
root.title("WAR! - Kyle Button")
root.geometry("500x500")

#deck of cards & variables
deck = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
    11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 13
]
random.shuffle(deck)
player = deck[:26]
computer = deck[26:]
player_score = 0
computer_score = 0
tiePile = []
sleeplen = 1.5
gameNum = 0
result = 0
gameOver = False
cardDisplay = StringVar()
winLoseOrTie = StringVar()
cardTotal = StringVar()

#visuals !!!! lets do this !!!!!
L1 = Label(root, text="Welcome to War! \n")
B1 = Button(root, text="Click to get started", command=startGame)

#placements
L1.pack(pady=25)
B1.pack(pady=10)

root.mainloop()
