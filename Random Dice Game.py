from time import sleep
import random

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
Bet = 0
CURPOINT = 0

print(f"\n{BLACK}Running Round #{gameNum}\n{RESET}")

# the game part
while gameOver == False:
    print(
        f"\n{LTBLUE}**********/////WELCOME TO KYLE'S GAMBLING ROOM!\\\\\\\\**********{RESET}"
    )
    print(
        f"\n{LTBLUE}**********/////YOU HAVE {Wager} POINTS!\\\\\\\\********{RESET}"
    )
    Bet = input(
        f"\n{LTBLUE}**********/////HOW MUCH DO YOU WANT TO WAGER?\\\\\\\\**********\n{RESET}"
    )

    #remaining points after bet
    CURPOINT = Wager - int(Bet)

    Prediction = int(input(
        f"\n{LTBLUE}**********/////WHAT NUMBER DO YOU THINK WILL COME UP?\\\\\\\\**********\n{RESET}"
    ))

    break

#dice roll

#fix this


counter = 0

while gameOver == False:
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)

    if dice1 != dice2:
        print(f"\n{RED} Dice #1: {dice1} \n Dice #2: {dice2} {RESET}")
        sleep(1)
        print(f"\n{BLACK} Re-rolling... {RESET}")
        counter += 1

    else:
        print(f"\n{GREEN} Dice #1: {dice1}  \n Dice #2: {dice2} {RESET}")
        print(f" \n{GREEN}You rolled a double!{RESET}")
        counter += 1

        if Prediction != counter:
            print(f"\n{RED}You guessed: {Prediction} Doulbes were in {counter} rolls.")
            print(f"\n{RED}You lost {Bet} points!{RESET}")
            print(f"\n{RED}You now have {CURPOINT} points!{RESET}")
        else:
            print(f"\n{GREEN}You Guessed Correctly!{RESET}")
            Wager *= 1.5
            print(f"\n{GREEN}You won {Wager} points!{RESET}")

#play again & error trapping
        while True:
            again = input(
                '\n Would you like to play again? (enter `y` or `n`): ')
            if again in ('y', 'n'):
                break
            print(
                f'\n{RED}*** Bad value! Please enter `y` or `n`! ***{RESET}\n')

        if again == 'n':
            gameOver = True

        if again == 'y':
            gameNum += 1
            counter = 0
            print(f"\n{BLACK}Running Round #{gameNum}\n{RESET}")
            

        gameNum += 1

print(f"\n{BLACK}Thanks for playing!{RESET}")