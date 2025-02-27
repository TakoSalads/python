import tkinter as tk
import random



class blackjack:


    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.root.geometry("600x500")
        self.root.configure(background='green')
        self.deck = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ]
        random.shuffle(self.deck)
        
        self.player_hand = []
        self.player=self.deck[0:26]
        self.pCardTotal = 0
        self.p3card = []
        self.didUhit = False
        self.player_totalu1 = 0
        
        self.house_hand = []
        self.house=self.deck[27:52]
        


        self.h1card = self.house.pop(0)
        self.h2card = self.house.pop(1)

        self.label = tk.Label(self.root, text="Welcome to BlackJack!", font=('Arial', 18))
        self.label.grid(row = 0, column=2, padx=175, pady=10)


        # board
        self.dealer_label = tk.Label(self.root, text="Dealer's Hand: ", font=('Arial',18))
        self.dealer_label.grid(row=1, column=2, padx=10, pady=10)

        self.button = tk.Button(
            self.root, 
            text="Click here to get started!",                     command=self.getCard)
        self.button.grid(row=2, column=2, padx=10, pady=10)

        #hit button
        self.hitme = tk.Button(
            self.root,
            text="Hit",                     command=self.hit
        )
        self.hitme.grid(row=3, column=2, padx=100, pady=5)

        #stand button
        self.stand_Button = tk.Button(
            self.root,
            text="Stand",
            height=2,
            width=10,
            command=self.stand
        )
        self.stand_Button.grid(row=4, column=2, padx=10, pady=10)



        #get cards
        self.player_label = tk.Label(self.root, text="Player's Hand: ", font=('Arial',18))
        self.player_label.grid(row=5, column=2, padx=10, pady=30)


        



        self.root.mainloop()



    def getCard(self):
        self.p1card = self.player.pop(0)
        self.p2card = self.player.pop(1)
        self.h1card = self.house.pop(0)
        self.h2card = self.house.pop(1)
        self.player_hand.append(self.p1card)
        self.player_hand.append(self.p2card)
        self.house_hand.append(self.h1card)
        self.house_hand.append(self.h2card)

        self.r1house_hand = self.h1card

        self.dealer_label.config(text="Dealer's Hand: " + str(self.r1house_hand) + " + *UNKNOWN CARD*")
        self.player_label.config(text="Player's Hand: " + str(self.player_hand))
        self.button.pack_forget()

    #BROKEN <3
    def haveYouBusted(self):

        
        if (self.player_totalu1) == 21:
         self.player_label.config( text="BlackJack! Your Total is 21, You win!")


        elif (self.player_totalu1) > 21:
         self.player_label.config(text="You busted! You lose!")

        else:
         self.player_label.config(text="You have " + str(self.player_totalu1))
        

    def hit(self):
        self.p3card = self.player.pop(2)
        self.player_hand.append(self.p3card)
        self.player_totalu1 = sum(self.player_hand)
        
        self.player_label.config(text="Player's Hand: " + str(self.player_totalu1))
        self.didUhit = True
        print(self.player_totalu1)
        self.haveYouBusted()


    
         

    def stand(self):

            self.dealer_label.config(text="Dealer's Hand: " + str(self.house_hand))
            if sum(self.house_hand) > sum(self.player_hand):
                self.player_label.config(text="You lose!")
                self.stand_Button.config(text="Play Again?", command=self.playAgain)
                
                

            elif sum(self.house_hand) == sum(self.player_hand):
                self.player_label.config(text="Tie!")
                self.button.config(text="Play Again?", command=self.playAgain)

            elif sum(self.house_hand) < sum(self.player_hand):
                self.player_label.config(text="You Win!")
                self.stand_Button.config(text="Play Again?", command=self.playAgain)
                

            else:
                self.player_label.config(text="You lose!")
                self.stand_Button.config(text="Play Again?", command=self.playAgain)

            if sum(self.house_hand) > self.player_totalu1 and self.didUhit == True:
              self.player_label.config(text="You lose!")
              self.stand_Button.config(text="Play Again?", command=self.playAgain)

            elif sum(self.house_hand) == self.player_totalu1 and self.didUhit == True:
                self.player_label.config(text="Tie!")
                self.stand_Button.config(text="Play Again?", command=self.playAgain)

            elif sum(self.house_hand) < self.player_totalu1 and self.didUhit == True:
               self.player_label.config(text="You Win!")
               self.stand_Button.config(text="Play Again?", command=self.playAgain)

            else:
                self.player_label.config(text="You lose!")
                self.stand_Button.config(text="Play Again?", command=self.playAgain)
                
    def playAgain(self):
            self.root.destroy()
            blackjack()
            
        

        
            self.button.pack_forget()
            self.hitme.pack_forget()
            self.stand.pack_forget()





blackjack()