from time import sleep
import random
import sys
import os

#COLORS
RED = '\033[1;31;48m'
BLACK = '\033[30m'
GREEN = '\033[32m'
RESET = '\033[0m'
LTBLUE = '\033[94m'

#variables
gameNum = 1
gameOver = False
counter = 0
Wager = 100 #starting points
CURPOINT = 100
Prediction = 0
Bet = 0



print(f"\n{BLACK}Running Round #{gameNum}\n{RESET}")

# the game part
def wagerscreen():
    global Wager
    global Prediction
    global CURPOINT
    global counter
    global Bet
    while startGame == True:
        print(
            f"\n{LTBLUE}**********/////WELCOME TO KYLE'S GAMBLING ROOM!\\\\\\\\**********{RESET}"
        )
        print(
            f"\n{LTBLUE}**********/////YOU HAVE {CURPOINT} POINTS!\\\\\\\\********{RESET}"
        )
        try:
            Bet = int(input(
                f"\n{LTBLUE}**********/////HOW MUCH DO YOU WANT TO WAGER?\\\\\\\\**********\n{RESET}" ))
            if Bet > 0 and Bet <= CURPOINT:
                break
            else:
                print("\nYou don't have enough points!")
        except ValueError:
            print(f"{RED}Invalid Input, Please Enter A Number. {RESET}")


    while startGame == True:            
        try:
            Prediction = int(input(
                f"\n{LTBLUE}**********/////WHAT NUMBER DO YOU THINK WILL COME UP?\\\\\\\\**********\n{RESET}"
            ))
            if Prediction > 0:
                break
            else:
                print("\nInvalid Prediciton... The Prediction must be positive!")
        except ValueError:
            print(f"{RED}Invalid Input, Please Enter A Number. {RESET}")


counter = 0


def diceRoll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1, dice2

def game():
    global Wager
    global Prediction
    global CURPOINT
    global counter
    global gameNum
    global Bet
    global gameOver
    global Prediction
    counter = 0
    while True:
        dice1, dice2 = diceRoll()
        if dice1 != dice2:
            print(f"\n{RED} Dice #1: {dice1} \n Dice #2: {dice2} {RESET}")
            sleep(0.2)
            print(f"\n{BLACK} Re-rolling... {RESET}")
            counter += 1
        else:
            print(f"\n{GREEN} Dice #1: {dice1}  \n Dice #2: {dice2} {RESET}")
            print(f" \n{GREEN}You rolled a double!{RESET}")
            counter += 1
            break

    if Prediction != counter:
        print(f"\n{RED}You guessed: {Prediction} Doulbes were in {counter} rolls.")
        print(f"\n{RED}You lost {Bet} points!{RESET}")
        CURPOINT -= Bet
        print(f"\n{RED}You now have {CURPOINT} points!{RESET}")
    else:
        print(f"\n{GREEN}You Guessed Correctly!{RESET}")
        CURPOINT += int(Bet * 1.5)
        print(f"\n{GREEN}You won {Bet} points!{RESET}")


    if CURPOINT <=  0:
        os.system('clear')
        print(f"{RED}\n\nYou've Ran Out of Points!\n\nYou've Lost the Game!\n")
        sys.exit()



#play again & error trapping
def replay():
        global gameNum
        global gameOver
        global counter
    
        while True:
            again = input(
                '\n Would you like to play again? (enter `y` or `n`): ')
            if again in ('y', 'n'):
                break
            print(
                f'\n{RED}*** Bad value! Please enter `y` or `n`! ***{RESET}\n')

        if again == 'n':
            gameOver = True
            print(f"\n\n{GREEN}Thanks for playing{RESET}")
            sys.exit()

        elif again == 'y':
            gameNum += 1
            counter = 0
            os.system('clear')
            wagerscreen()
            game()
            replay()



startGame = input(f"{LTBLUE}Would you like to play? (enter `y` or `n`): {RESET}")
if startGame == 'y':
    startGame = True
    wagerscreen()
    game()
    replay()
else:
    startGame = False
    print(f"\n{RED}Thanks for playing!{RESET}")
    sys.exit()
