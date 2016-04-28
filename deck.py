
# TODO: make 11-14 display as jack, queen, king, ace rather than the underlying numbers.
# TODO: double check randomness distribution of shuffling method.
# TODO: add assert statements for restricted inputs.
# TODO: reorganize the method order?
# TODO: not sure how random the random shuffle is-- could test with simulation and graphing.
# TODO: consistent casing for method names.
# TODO: change hasstraight from hardcoded 3 to variable length.



from operator import attrgetter
import random

from __future__ import division

import matplotlib.pyplot as plt


class Deck:
    """The deck class represents a 52-card deck, Aces high."""
    
    
    def __init__(self):
        # Initialize the new deck
        self.new_deck = []
        suits = ["clubs", "diamonds", "hearts", "spades"]
 
        # By convention: jack = 11, queen = 12, king = 13, ace = 14
        # Might be more pythonic to use zip instead of double loop
    
        # Populate the deck with 52 cards
        for suit in suits:
            for number in range(2, 15):
                new_card = Card(number, suit)
                self.new_deck.append(new_card)
    

    def dealOne(self):
        """Moves the top card from the deck to a player's hand."""
        dealt_card = self.new_deck.pop()
        return dealt_card
    
    
    def print_order(self):
        """Prints the cards in the deck, in order."""
        for card in self.new_deck:
            card.print_card()
    
    
    def shuffle(self, goodness):
        """
        Shuffles the deck based on a goodness input: 0 is a perfectly random shuffle, 1 is no shuffle.
        If goodness = 0, the shuffle is completely random.
        If goodness = 1, there is no shuffle: no card changes positions.
        At a goodness of 0.5, there is a 50% chance for a given card to change positions during the shuffle.
        """
        ## Assert goodness between 0 and 1
        
        for card in self.new_deck:
            
            # Check if the card will be shuffled to a new position.
            randomness_test = random.random() #a number between 0 and 1
        
            # If the shuffling goodness threshold is higher than the random number, shuffle the card elsewhere;
            # Otherwise do nothing.
            if goodness < randomness_test:
                x = self.new_deck.pop()
                self.new_deck.insert(random.randrange(len(self.new_deck) + 1), x)





class Card:
    """The card class represents a single card."""
    
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        
        
    def __repr__(self):
        return repr((self.number, self.suit))
        
        
    def print_card(self):
        """Prints the card's number and suit."""
        card_info = (self.number, self.suit)
        print card_info
        
        #add assert statements






class Hand:
    """The hand class represents a set of 0-52 cards, in definite order."""
    
    suit_order = ["clubs", "diamonds", "hearts", "spades"]
    #from lowest to highest; conveniently also in alphabetical order
    
    def __init__(self):
        self.new_hand = []
    
    
    def print_hand(self):
        """Prints the cards in the hand, in order."""
        for card in self.new_hand:
            card.print_card()
    
    
    def addCard(self, deck_name):
        "Deals a card from the deck, and adds it to the player's hand."
        dealt_card = deck_name.dealOne()
        self.new_hand.append(dealt_card)
        
    
    def sortBySuit(self):
        """Sorts cards by suit, then by value. Low to high."""
        self.new_hand = sorted(self.new_hand, key = attrgetter("suit", "number"))
    
    
    def sortByValue(self):
        """Sorts cards by value, then by suit. Low to high."""
        self.new_hand = sorted(self.new_hand, key = attrgetter("number", "suit"))
        
        
    def hasStraight(self, straight_length = 3, sameSuit = False):
        """Checks whether the hand contains a straight of the given length or greater.
        If sameSuit is enabled, only count straights with cards in the same suit (flushes).
        Finds the first straight, but does not count if there are multiples."""
        
        # First sorts the hand by value.
        self.sortByValue()
        
        # Then checks whether any sequence of N length is a straight.
        # First check whether hand is longer than straight length.
        
        hand_length = len(self.new_hand)
        
        if hand_length >= straight_length:
            
            for i in range(0, hand_length - straight_length):  #ob1?
                card1 = self.new_hand[i]
                card2 = self.new_hand[i+1]
                card3 = self.new_hand[i+2]
                
                # Refactor later-- redundant cases.
                if sameSuit == False:
                    if card1.number + 1 == card2.number:
                        if card2.number + 1 == card3.number:
                            #print "A straight of", card1.print_card(), card2.print_card(), card3.print_card()
                            return True
                        
                elif sameSuit == True:
                    if card1.number + 1 == card2.number:
                        if card2.number + 1 == card3.number:
                            if card1.suit == card2.suit and card2.suit == card3.suit:
                                #print "A straight of", card1.print_card(), card2.print_card(), card3.print_card()
                                return True

            else:
                #print "No straight in this hand"
                return False







def Round(shuffle_quality = 0, player_count = 2, straight_count = 3):
    """Creates a deck, shuffles, deals hands to players, and checks for straights."""
    deck = Deck()
    deck.shuffle(shuffle_quality)
    
    #deck.print_order()
    # Hard coding two players; refactor later.
    
    PlayerHand = Hand() #this is the player's hand, that we'll check
    OtherHands = Hand() #this is crude, as it just simulates cards dealt to "other players" and does not distinguish their hands.
    #fine for the purposes of this simulation
    
    player_count -=1 #player's hand is accounted for
        
    # Hand size of 5.
    hand_size = 5
    while hand_size > 0:
        PlayerHand.addCard(deck)
        
        for i in range(player_count):
            OtherHands.addCard(deck)
        
        hand_size -= 1
    
    #PlayerHand.print_hand()
    return PlayerHand.hasStraight()
    




def Simulate_Rounds(num_rounds = 50000, shuffle_quality = 0, player_count = 2, straight_count = 3):
    
    total_rounds = num_rounds
    
    straight_counter = 0
    no_straight_counter = 0
    
    while num_rounds > 0:
        result = Round(shuffle_quality, player_count, straight_count)
        
        if result == True:
            straight_counter += 1
        elif result == False:
            no_straight_counter += 1
    
        num_rounds -= 1
        
    straight_chances = straight_counter / total_rounds

#     print "The number of straights is", straight_counter, "out of", total_rounds
#     print "The number of misses is", no_straight_counter, "out of", total_rounds
#     print "The chances of getting a straight are", straight_chances
    
    return straight_chances
        
        





"""
#QUESTION 1: Chance of being dealt a 3-card straight?

Simulate_Rounds(500000)


The number of straights is 117860 out of 500000
The number of misses is 382140 out of 500000
The chances of getting a straight are 0.23572




#QUESTION 2: How do the chances vary with how well the deck is shuffled?

shuffle_answer_list = []

for i in range (0, 11):
    i = i/10
    straight_chance = Simulate_Rounds(50000, shuffle_quality = i)
    
    shuffle_answer_list.append("In round " + str(i))
    shuffle_answer_list.append(straight_chance) 
    
for item in shuffle_answer_list:
    print item
    
#NOTE-- this is a result of the shuffle system switching off between players. If cards were dealt to one player at a time, 
#the chance of a straight would approach 1 as shuffle quality --> 1.


In round 0.0
0.23992
In round 0.1
0.241
In round 0.2
0.21698
In round 0.3
0.18436
In round 0.4
0.17028
In round 0.5
0.18612
In round 0.6
0.18854
In round 0.7
0.1408
In round 0.8
0.06212
In round 0.9
0.0166
In round 1.0
0.0





#QUESTION 3: How does this answer change if you vary the number of players?
#Will take this as asking about a perfect shuffle, but could do a randomness x player count plot.

player_count_list = []

for i in range(2, 9):
    straight_chance = Simulate_Rounds(50000, player_count = i)
    
    player_count_list.append("For number of players: " + str(i))
    player_count_list.append(straight_chance) 
    
for item in shuffle_answer_list:
    print item



In round 0.0
0.2446
In round 0.1
0.2428
In round 0.2
0.216
In round 0.3
0.1932
In round 0.4
0.1766
In round 0.5
0.173
In round 0.6
0.1834
In round 0.7
0.1384
In round 0.8
0.0602
In round 0.9
0.0158
In round 1.0
0.0
"""








