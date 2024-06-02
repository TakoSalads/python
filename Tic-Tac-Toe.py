#Kyle Button
#April 11, 2024
#Purpose: to create a program that will allow the user to play the game tic tac toe against an ai or another player.


#Expectations:
#Good and appropriate use of if/elif/else statements, while loops and functions, and arrays
#Good programming style
#→ variable & function names must be descriptive and appropriate
#→ good use of white space (blank lines) so it is easy to read
#→ your code should be well documented appropriately
#→ all numeric inputs should be error trapped appropriately 
#→ inputs for the play again loop must be error trapped as well
#Your code should be efficient!
#Your output should be formatted nicely with informative instructions and include an appropriate introduction and conclusion

#Imports and colors
import random
import time
import os
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
RESET= '\033[0m'

#Board
ASOS = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
winners = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],[2, 5, 8], [0, 4, 8], [2, 4, 6]]

def printBoard():
    
    print("\n\n     0  |  1  |  2   \n "
          "  -----|-----|-----\n "
          "    3  |  4  |  5   \n "
          "  -----|-----|-----\n "
          "    6  |  7  |  8   \n " )
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])
    

gameOver = False
player_score=0
computer_score=0



#def isThereAWinner():
 #   for var in winners:
  #      print(var[0], var[1], var[2])
   # if var[0] == 'X' and var[1] == 'X' and var[2] == 'X':
    #    return True
    #return False





def computer_turn():
    global outofmoves
    compturn = 'O'
    c_input = random.choice(ASOS)
    ASOS.remove(c_input)
    c_input = int(c_input)
    if board[c_input] == ' ':
        board[c_input] = compturn
    print(board)
    os.system('clear')



def wincheck():
    for a,b,c in winners:
        if board[a] == 'X' and board[b] == 'X' and board[c] == 'X':
            print("\n\n    ***You win!***    ")
            return True
    return False

def wincheckcomp():
    for a,b,c in winners:
        if board[a] == 'O' and board[b] == 'O' and board[c] == 'O':
            print("\n\n    ***O wins***    ")
            return True
    return False
    

        

#Starting game
print("Welcome to Tic Tac Toe")

#would you like to play loop

def playAgain():
    global gameOver
    global answer
    answer = input(f"{BLUE}Would you like to play?  (y/n) {RESET}")
    if answer.lower() == "y":
       gameOver = False
    elif answer.lower() == "n":
       gameOver = True
    else: 
        print("\ninvalid input please enter Y or N")
        

    

playAgain()

# start of game 
while gameOver == False:
    printBoard()

    turn = 'X'
    counter = 0

    
    try: 
        p_input = int(input("Where would you like to go?"))
        if p_input < 0 or p_input > 8:
            print(f"\n{RED}Invalid input please enter a number between 0 and 8{RESET}")
            continue
    except ValueError:
        print(f"\n{RED}Invalid input please enter a number between 0 and 8{RESET}")
        continue


    if board[p_input] == ' ':
        board[p_input] = turn
        ASOS.remove(str(p_input))
    else:
        print(f"\n{RED}Space is already taken please try again{RESET}")
        continue


    if len(ASOS) == 0:
        print("There are no more moves!")
        print(board)
        playAgain()
        break

    if wincheck() == True:
        playAgain()
        break
        


    computer_turn()
    wincheckcomp()

    if wincheck() == True:
        playAgain()
        break
        

    if wincheckcomp() == True:
        playAgain()
        break