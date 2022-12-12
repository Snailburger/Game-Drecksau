# -*- coding: utf-8 -*-

""" Card """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'


class Card:
    # Cards are defined by their key words
    # This dict contains the key words for all action card types and maps
    # them to the card name of the game.
    action_card_types = { 
        "MUD"                   : "Matschkarte",
        "RAIN"                  : "Regenkarte",
        "LIGHTNING"             : "Blitzkarte",
        "FARMER_CLEANS"         : "Bauer-schrubbt-die-Sau-Karte",
        "STORM"                 : "Sturmkarte",
    }

    # This dict contains the key words for all upgrade card types and maps
    # them to the card name of the game.
    upgrade_card_types = {
        "STALL"                 : "Stallkarte",
        "LIGHTNING_CONDUCTOR"   : "Blitzableiterkarte",
        "ANNOY_FARMER"         : "Bauer-ärgere-dich-Karte",
    }

    # This dict contains the key words for the table card types and maps
    # them to the card name of the game.
    table_card_types = {
        "PIG"                   : "Schweinekarte",
    }

    # combining all the card type dicts
    all_types = {**table_card_types, **action_card_types, **upgrade_card_types}
    
    def __init__(self, card_type):
        self.card_type  = card_type
        # card type is given as an input when initiating an object of this class

        self.name       = self.all_types[card_type]

    def get_name(self):
        """
        Method returns the name of the card. 
    
        Parameters
        ----------
        None.

        Returns
        -------
        self.name : string
            name of the card
    
        """
        return self.name

    def get_card_type(self):
        """
        Method returns the card type of the card. 
    
        Parameters
        ----------
        None.

        Returns
        -------
        self.card_type : string
            Card type of the card
    
        """
        return self.card_type


if __name__ == "__main__":

    print("\nTest: init for a pig card (Key = PIG)")
    test_card = Card("PIG")

    # Test methods
    print("\nTest: methods of class Card")

    # Method: get_name
    card_name = test_card.get_name()
    print("\nTest: method get_name")
    print("(Expected value: Schweinekarte). Value:", card_name)

    # Method: get_card_type
    card_type = test_card.get_card_type()
    print("\nTest: method get_card_type")
    print("(Expected value: PIG). Value:", card_type)

