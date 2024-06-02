#Kyle Button
#4/5/24
#Pupose: To create a program that will allow you to play the card game war against an AI



import random
import time
import os
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
RESET= '\033[0m'
sleeplen = 1.5
gameNum = 0
gameOver = False

#play again loop as a function (cleanliness)

def playAgain():
    global gameNum
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
        gameOver = False


        gameNum += 1


# instuctions for game:

#The two players `turn over` the top card of their deck and the player with the higher card `wins` that round and adds one point to their total. The loser subtracts one point from their total.

#If the cards are the same, the round is a tie and neither player gets a point

#The player with the most points after all 26 cards are turned over wins that game

print(f"{BLUE}\n\n/////*****   Welcome to War!   *****/////\n{RESET}")

print(f"{BLUE}\n\n/////*****   How do you play war?   *****/////\n{RESET}")
print(f"{BLUE}\nWar is a two-player card game where each player reveals the top card of their deck simultaneously. The player with the higher card takes both cards. In case of a tie, players enter a 'war,' placing additional cards face-down before revealing another card. The game continues until one player collects all the cards{RESET}\n")

#play again & error trapping

playAgain()

#deck of cards & variables


deck = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ]

random.shuffle(deck)

#player 1's deck
player=deck[:26]
#player 2's deck
computer=deck[26:]

#Current Points
player_score=0
computer_score=0
tiePile=[]

#play again loop as a function (cleanliness)

def playAgain():
    global gameNum
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


        gameNum += 1

#win, lose, or tie
def compareHands(player, computer):
    if p1card > c1card:
        result = 1
    if p1card < c1card:
        result = -1
    else:
        result = 0
    return result

#check for cards left

def isThereAnyCards():
    global computer
    global player
    global gameOver
    
    if len(player) == 0:
        print(f"\n{BLACK}Player has no cards left!{RESET}")
        print(f"{RED}\n\n**** -DEFEAT- COMPUTER WINS ****\n\n{RESET}")
        playAgain()
        
        return True

    if len(computer) == 0:
        print(f"\n{BLACK}Computer has no cards left!{RESET}")
        print(f"{GREEN}\n\n**** CONGRATULATIONS YOU WIN  ****\n\n{RESET}")
        playAgain()
        return True

    return False

#While loop (basically the whole game)
while gameOver == False:

    isThereAnyCards()
    p1card = player.pop(0)
    c1card = computer.pop(0)

    print(f"{BLUE}  ///*** CURRENT ROUND: {computer_score+player_score} ***///   {RESET}")
    

    if compareHands(p1card, c1card) == 1:
        player_score += 1
        print(f"{GREEN}\nPlayer wins the round!{RESET}")
        player.append(p1card)
        player.append(c1card)


    elif compareHands(p1card, c1card) == -1:
        computer_score += 1
        print(f"{RED}\nComputer wins the round!{RESET}")
        computer.append(p1card)
        computer.append(c1card)

    while compareHands(p1card, c1card) == 0:
        print("\nThe round was a Tie!")
        tie = True
        tiePile = []
        while tie == True:
            tiePile.append(c1card)
            tiePile.append(p1card)
            isThereAnyCards()
            p1card = player.pop(0)
            c1card = computer.pop(0)
            print(f"{BLUE}")
            print(p1card, c1card)
            if compareHands(p1card, c1card) == 1:
                player_score += 1
                print(f"{GREEN}\n     Player wins the tie{RESET}")
                player.extend(tiePile)
                player.append(c1card)
                player.append(p1card)
                break
                
            elif compareHands(p1card, c1card) == -1:
                computer_score += 1
                print(f"{RED}\n     Computer wins the tie!{RESET}")
                computer.extend(tiePile)
                computer.append(c1card)
                computer.append(p1card)
                break


            elif len(player) == 0 or len(computer) == 0:
                tie = False
                break

    print(f"{GREEN}\n\nPlayer's Card: {p1card}{RESET}       {RED}Computer's Card: {c1card}{RESET}")
                
    print(f"\n\nPlayer's Deck: {len(player)}{RESET}       Computer's Deck: {len(computer)}{RESET}")
        
    time.sleep(sleeplen)

    print(f"\n{BLUE}    *****Drawing next card*****    {RESET}")

    os.system('clear')