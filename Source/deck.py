# -*- coding: utf-8 -*-

""" Deck """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'


from actioncard import ActionCard
from upgradecard import UpgradeCard
from card import Card

import random

class Deck:

    def __init__(self):
        # Defining amount per card type
        # ACTIONCARDS
        MUDS                 = [ActionCard("MUD")] * 21
        RAINS                = [ActionCard("RAIN")] * 4
        LIGHTNINGS           = [ActionCard("LIGHTNING")] * 4
        FARMER_CLEANS        = [ActionCard("FARMER_CLEANS")] * 8
        STORM                = [ActionCard("STORM")] * 1

        # UPGRADECARDS
        STALLS               = [UpgradeCard("STALL")] * 9
        LIGHTNING_CONDUCTORS = [UpgradeCard("LIGHTNING_CONDUCTOR")] * 4
        ANNOY_FARMER         = [UpgradeCard("ANNOY_FARMER")] * 4

        # Initializing Deck and Discard pile
        # DECK
        self.draw_deck = MUDS + RAINS + LIGHTNINGS + FARMER_CLEANS + STALLS \
        + LIGHTNING_CONDUCTORS + ANNOY_FARMER + STORM
        random.shuffle(self.draw_deck)

        # DISCARD PILE
        self.discard_pile = list()

    def deal_card(self):
        """
        Method takes a card from the draw_deck for the player to take in his
        hands. If no cards are present in the draw_deck, a new draw_deck is 
        created.
            
        Parameters
        ----------
        None.
        
        Returns
        -------
        card : Card
            The card that is given from the draw_deck
        """
        if not self.deck_has_cards():
            self.create_new_draw_deck()
        card = self.draw_deck.pop()
        return card

    def deck_has_cards(self):
        """
        Checks if the draw deck has any cards left.
            
        Parameters
        ----------
        None.
        
        Returns
        -------
        bool
            Indicates if there are cards left in the draw deck
        """
        return len(self.draw_deck) > 0

    def create_new_draw_deck(self):
        """
        Takes all cards from the discard pile, moves it to the draw deck and 
        shuffles the draw deck.
            
        Parameters
        ----------
        None.
        
        Returns
        -------
        bool
            Indicates if the draw deck could be newly createded
        """
        self.draw_deck = self.discard_pile
        random.shuffle(self.draw_deck)
        self.discard_pile = []
        return True

    def add_card_to_discard_pile(self, card):
        """
        Adds a card to the discard pile
            
        Parameters
        ----------
        card : Card
            The card that should be moved to the discard pile
        
        Returns
        -------
        bool
            Indicates if the card is added to the discard pile succesfully
        """
        self.discard_pile.append(card)
        return True

    def add_destroyed_card_to_discard_pile(self, card_type):
        """
        Adds a destroyed card to the discard pile
            
        Parameters
        ----------
        card_type : string
            Indicates the type of the card which was destroyed
        
        Returns
        -------
        bool
            Indicates if the destroyed card is added to the discard pile 
            succesfully
        """
        self.discard_pile.append(UpgradeCard(card_type))
        return True


if __name__ == "__main__":
    #helper function for testing
    def check_number_of_cards(deck, number_of_cards):
        if len(deck.draw_deck) == number_of_cards:
            return True
        else:
            return False

    #helper function for testing
    def empty_draw_deck(deck):
        for i in range(len(deck.draw_deck)):
            card = deck.deal_card()
            deck.add_card_to_discard_pile(card)
        return deck

    #helper function for testing
    def check_if_empty(deck):
        if not deck.deck_has_cards():
            return True
        else:
            return False

    deck = Deck()

    print("\nTest number of cards in draw deck")
    print("Expected: True")
    print("Status:", check_number_of_cards(deck, 55))
    print("Expected: False")
    print("Status:", check_number_of_cards(deck, 32))
    
    print("\nTest deal_card with number of cards in deck")
    card1 = deck.deal_card()
    print("Expected: True")
    print("Status:", isinstance(card1, Card))
    
    card2 = deck.deal_card()
    print("Expected: True")
    print("Status:", isinstance(card2, Card))
    
    print("Expected: True")
    print("Status:", check_number_of_cards(deck, 53))
    print("Expected: False")
    print("Status:", check_number_of_cards(deck, 51))
    
    print("\nTest function deck_has_card")
    print("Expected: True")
    print("Status:", deck.deck_has_cards())

    print("\nTest function deal_card / add_card_to_discard_pile")
    print("Expected: True")
    deck = empty_draw_deck(deck)
    print("Status:", check_if_empty(deck))
    
    print("\nTest function create_new_draw_deck")
    print("Expected: True")
    deck.create_new_draw_deck()
    print("Status:", deck.deck_has_cards())
    
    print("Expected: True")
    print("Status:", len(deck.discard_pile) == 0)

    print("\nTest function add_destroyed_card_to_discard_pile")
    card_type = "LIGHTNING_CONDUCTOR"
    deck.add_destroyed_card_to_discard_pile(card_type)
    print("Expected: True")
    print("Status:", len(deck.discard_pile) == 1)
    


    