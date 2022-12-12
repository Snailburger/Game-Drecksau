# -*- coding: utf-8 -*-

""" Validator """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'


class Validator:

    def __init__(self):
        # parameters
        self.min_players = 2
        self.max_players = 4
    
    def number_of_players(self, input_player):
        """
        Checks the input of the player. The value should indicate how many 
        players will play the game.
    
        Parameters
        ----------
        input_player : int
            The input from the player.

        Returns
        -------
        validation : bool
            Indicates if the given input is valid

        """
        validation = False
        try:
            input_player = int(input_player)
            if self.min_players <= input_player <= self.max_players:
                validation = True
            else:
                raise
        except:
            print("Fehler: Anzahl der Spieler ist ungültig! (Mögliche Anzahl: 2-4).")
        return validation

    def choose_play_or_change_card(self, input_player):
        """
        Checks the input of the player. The value should indicate if the player 
        wants to play or change a card.
    
        Parameters
        ----------
        input_player : int
            The input from the player.

        Returns
        -------
        validation : bool
            Indicates if the given input is valid
            
        """
        validation = False
        try:
            input_player = int(input_player)
            if input_player in [1, 2]:
                validation = True
            else:
                raise
        except:
            print("Fehler: Wähle eine Karte wechseln (1) oder alle Karten wechseln (2).")
        return validation

    def move_is_possible(self, possible_moves):
        """
        Checks if there is any possible move for the player.

        Parameters
        ----------
        possible_moves : list
            List of possible moves

        Returns
        -------
        validation : bool
            Indicates if there are possible moves for the player

        """
        validation = False
        if possible_moves:
            validation = True
        else:
            print("Karte kann nicht platziert werden, da keine passende Karte auf dem Brett liegt.")
        return validation

    def choose_card(self, input_player):
        """
        Method to choose card

        Parameters
        ----------
        input_player : int
            The given input from the player

        Returns
        -------
        validation : bool
            Indicates if the given value is valid
            
        """
        validation = False
        try:
            input_player = int(input_player)
            if input_player in [1, 2, 3]:
                validation = True
            else:
                raise
        except:
            print("Fehler: Wähle eine gültige Karte (1-3)")
        return validation

    def choose_move(self, input_player, possible_moves):
        """
        Checks if the given input from the user is in the range of the possible 
        moves

        Parameters
        ----------
        input_player : string
            The given input from the player
        possible_moves : list
            List of possible moves

        Returns
        -------
        validation : bool
            Indicates if the given value is valid
            
        """
        validation = False
        try:
            input_player = int(input_player)
            if input_player in list(range(1, len(possible_moves)+1)):
                validation = True
            else:
                raise
        except:
            print("Fehler: Wähle deinen Zug")
        return validation

    def choose_to_change_one_or_all_cards(self, input_player):
        """
        Checks the input of the player. The value should indicate if the player 
        wants to change one card or all cards in his hand.

        Parameters
        ----------
        input_player : string
            The given input from the player

        Returns
        -------
        validation : bool
            Indicates if the given value is valid
            
        """
        validation = False
        try:
            input_player = int(input_player)
            if input_player in [1, 2]:
                validation = True
            else:
                raise
        except:
            print("Fehler: Wähle eine Karte wechseln (1) oder alle Karten wechseln (2)")
        return validation


if __name__ == "__main__":
    validator = Validator()

    # test method number_of_players
    print("\nTest method number_of_players")
    print("Set number to 2. Expected value: True")
    print("Value:", validator.number_of_players(2))
    print("Set number to 3. Expected value: True")
    print("Value:", validator.number_of_players(3))
    print("Set number to 4. Expected value: True")
    print("Value:", validator.number_of_players(4))
    print("Set number to 0. Expected value: False")
    print("Value:", validator.number_of_players(0))
    print("Set number to 1. Expected value: False")
    print("Value:", validator.number_of_players(1))
    print("Set number to 5. Expected value: False")
    print("Value:", validator.number_of_players(5))

    # test method choose_play_or_change_card
    print("\nTest method choose_play_or_change_card")
    print("Choices are: 1 for playing or 2 for changing card")
    print("Choose 1. Expected value: True")
    print("Value:", validator.choose_play_or_change_card(1))
    print("Choose 2. Expected value: True")
    print("Value:", validator.choose_play_or_change_card(2))
    print("Choose 0. Expected value: False")
    print("Value:", validator.choose_play_or_change_card(0))
    print("Choose 3. Expected value: False")
    print("Value", validator.choose_play_or_change_card(3))

    print("\nTest method move_is_possible")
    print("Card MUD to card PIG. Expected value: True")
    print("Value:", validator.move_is_possible(["PIG", "MUD"]))
    print("Card STALL to card PIG. Expected value: True")
    print("Value:", validator.move_is_possible(["PIG", "STALL"]))
    print("Card PIG to card STALL. Expected value: False")
    print("Value:", validator.move_is_possible(["LIGHTNING_CONDUCTOR", "STALL"]))
    print("Value:", validator.move_is_possible(["LIGHTNING_CONDUCTOR", "STALL"]))

    # test method choose_card
    print("\nTest method choose_card")
    print("Player has 3 cards to choose from")
    print("Choose 1. Expected value: True")
    print("Value:", validator.choose_card(1))
    print("Choose 2. Expected value: True")
    print("Value:", validator.choose_card(2))
    print("Choose 3. Expected value: True")
    print("Value:", validator.choose_card(3))
    print("Choose 0. Expected value: False")
    print("Value:", validator.choose_card(0))
    print("Choose 4. Expected value: False")
    print("Value:", validator.choose_card(4))

    # test method choose_to_change_one_or_all_cards
    print("\nTest method choose_to_change_one_or_all_cards")
    print("Choices are: 1 for changing one card or 2 for changing all cards")
    print("Choose 1. Expected value: True")
    print("Value:", validator.choose_to_change_one_or_all_cards(1))
    print("Choose 2. Expected value: True")
    print("Value:", validator.choose_to_change_one_or_all_cards(2))
    print("Choose 0. Expected value: False")
    print("Value:", validator.choose_to_change_one_or_all_cards(0))
    print("Choose 3. Expected value: False")
    print("Value:", validator.choose_to_change_one_or_all_cards(3))


