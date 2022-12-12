# -*- coding: utf-8 -*-

""" Player """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'


from pigcard import PigCard
from actioncard import ActionCard
from upgradecard import UpgradeCard


class Player:

    def __init__(self, name):
        self.name = name
        self.cards_hand = list()
        self.cards_table = list()
    
    def get_name(self):
        """
        Gets name of the players.

        Parameters
        ----------
        None.

        Returns
        -------
        self.name : str
            Name of player.

        """
        return self.name

    # Cards on table
    def add_card_to_table(self, card):
        """
        Adds initial pig cards to the table.

        Parameters
        ----------
        card : PigCard
            An object of the class PigCard is given as input

        Returns
        -------
        None.

        """
        self.cards_table.append(card)

    def get_cards_table(self):
        """
        Checks cards on table.

        Parameters
        ----------
        None.

        Returns
        -------
        self.cards_table : list
             Returns list of cards on table
        """
        return self.cards_table

    def update_card_table(self, updated_pig):
        """
        Updates a pig card on the table. The updated_pig is a PigCard of this
        player which has been modified by an ActionCard or an UpgradeCard. This
        method loops throught the PigCards of this player and checks
        which of the PigCards on the table is equal to the updated_pig and
        replaces the first one with the latter.

        Parameters
        ----------
        updated_pig : PigCard
            An object of the class PigCard is given as input. 

        Returns
        -------
        None.
        """
        self.cards_table = [updated_pig if updated_pig == pig 
                                        else pig for pig in self.cards_table]
        return

    def show_cards_on_table(self):
        """
        Shows current players cards on table.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        print("\n" + self.name + "'s Tischkarten:")
        for pig in self.cards_table:
            pig_number = pig.get_pig_number()
            current_status = pig.get_current_status()
            print("Schwein " + str(pig_number) + ": " + ", ".join(current_status))

    # Cards on hand
    def get_card_hand(self, n_card):
        """
        Method to choose the card that will be played or changed.

        Parameters
        ----------
        n_card : int
            Number of card


        Returns
        -------
        card : list
            Returns the card, that is played or changed
        """
        card = self.cards_hand[n_card - 1]
        return card

    def get_cards_hand(self):
        """
        Get cards in hand of current player.

        Parameters
        ----------
        None.

        Returns
        -------
        cards_hand : list
            Cards that can be played or changed
        """
        return self.cards_hand

    def add_card_to_hand(self, card):
        """
        Adds card to hand of current player.

        Parameters
        ----------
        card : list
            Any type of card but pig card can be added to the list of cards in players hand

        Returns
        -------
        None.
        """
        self.cards_hand.append(card)

    def del_card_hand(self, card):
        """
        Deletes one or all cards from hand of player if he chooses to change one
        or all cards.

        Parameters
        ----------
        card : list
            Deletes one or all of the cards on players hand.

        Returns
        -------
        None.
        """
        self.cards_hand.remove(card)

    def show_cards_in_hand(self):
        """
        Prints cards in hands of current player.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        counter = 1
        print("\nHandkarten:")
        for card in self.cards_hand:
            print(str(counter) + ": " + card.get_name())
            counter += 1


if __name__ == "__main__":

    player_1 = Player("Schweinebauer")

    # test methods
    print("\nTest methods of class Player")

    # get_name
    print("\nTest method get_name")
    player_name = player_1.get_name()
    print("Expected value: Schweinebauer. Value:", player_name)

    # show_cards_on_table
    print("\nTest method show_cards_on_table before cards are added.")
    print("Expected value: None")
    print("Value: ", player_1.show_cards_on_table())

    # add_card_table
    print("\nTest method add_card_table")
    card_pig_1 = PigCard(1)
    card_pig_2 = PigCard(2)
    player_1.add_card_to_table(card_pig_1)
    player_1.add_card_to_table(card_pig_2)

    # get_cards_table
    print("\nTest method get_cards_table")
    print("Expected values: pigcard, pigcard (all cards on table)")
    print(player_1.get_cards_table())

    # show_cards_on_table
    print("\nTest method show_cards_on_table after cards are added.")
    print("Expected value: Schwein 1: Sauberschwein, Schwein 2: Sauberschwein")
    player_1.show_cards_on_table()

    # get_cards_hand before cards are added
    print("\nTest method get_cards_hand before cards are added")
    print("Expected value: Empty list")
    print("Value:", player_1.get_cards_hand())

    # add_card_hand
    print("\nTest method add_card_hand")
    card_action_1 = ActionCard("MUD")
    card_action_2 = ActionCard("RAIN")
    card_upgrade_1 = UpgradeCard("STALL")
    player_1.add_card_to_hand(card_action_1)
    player_1.add_card_to_hand(card_action_2)
    player_1.add_card_to_hand(card_upgrade_1)

    # get_cards_hand after cards are added
    print("\nTest method get_cards_hand after cards are added")
    print("Expected value: actioncard, actioncard, upgradecard (all cards on hand)")
    print("Value:", player_1.get_cards_hand())

    # get_card_hand
    print("\nTest method get_card_hand")
    print("Expected value: upgradecard (chosen card to play or change). Value:", player_1.get_card_hand(0))

    # show_cards_in_hand
    print("\nTest method show_cards_in_hand")
    print("Expected values: 1: Matschkarte, 2: Regenkarte, 3: Stallkarte")
    player_1.show_cards_in_hand()

    # del_card_hand
    player_1.del_card_hand(card_action_2)
    print("\nTest method del_card_hand")
    print("Deleted card: '2: Regenkarte'")
    print("Expected values: 1: Matschkarte, 2: Stallkarte")
    player_1.show_cards_in_hand()
