#goal: make a functional randition of the card game war in python

suits = {"Hearts", "Diamonds", "Clubs", "Spades"}
ranks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
print(deck)
