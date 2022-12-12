# -*- coding: utf-8 -*-

""" upgrade card """

__author__     = 'Anja Edelmann'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Anja Edelmann'
__email__      = 'edelmanj@students.zhaw.ch'
__status__     = 'done'

 
from card import Card
from pigcard import PigCard


class UpgradeCard(Card):

    def __init__(self, card_type):
        super(UpgradeCard, self).__init__(card_type)

        upgradecard_func_map = {
        "STALL"                 : self.get_stall,
        "LIGHTNING_CONDUCTOR"   : self.get_lightning_conductor,
        "ANNOY_FARMER"          : self.annoy_farmer,
        } 

        self.func = upgradecard_func_map[self.card_type]

    def activate_card(self, card):
        """
        Method takes a PigCard as input and modifies its attributes depending
        on the function of the upgrade card. The modified card is returned.

        Parameters
        ----------
        card : PigCard
            An object of the class PigCard is given as input

        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.

        False: bool
            Second value in the form of a boolean is returned. This indicates
            that no card has been destroyed during the activation process of the
            upgrade card. (See example actioncard.py)

        """
        modified_card = self.func(card)
        return modified_card, False

    def get_stall(self, pigcard):
        """
        Function of the card "STALL". This method takes a pigcard as input and
        checks if it already has a stall (self.stall = True). A new stall is 
        built, if the pigcard does not have a stall (attribute self.stall is set
        to True)

        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input

        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.

        """
        if not pigcard.has_stall():
            pigcard.build_stall()
        return pigcard

    def get_lightning_conductor(self, pigcard):
        """
        Function of the card "LIGHTNING_CONDUCTOR". This method takes a pigcard
        as input and checks if it has a stall (self.stall = True) and if the
        stall has a lightning conductor (self.lightning_conductor = True).
        If has.stall is True and has.lightning_conductor is False a lightning
        conductor is built (attribute self.lightning_conductor is set to True).

        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input

        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.

        """
        if pigcard.has_stall() and not pigcard.has_lightning_conductor():
            pigcard.build_lightning_conductor()
        return pigcard

    def annoy_farmer(self, pigcard):
        """
        Function of the card "ANNOY_FARMER". This method takes a pigcard as input and
        checks if it has a stall (self.stall = True) and if it has a door
        (self.door = True).
        If self.stall is True and self.door is False a door is built.
        (attribute self.door is set to True)

        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input

        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
            
        """
        if pigcard.has_stall() and not pigcard.has_door():
            pigcard.build_door()
        return pigcard
        

if __name__ == "__main__":
    test_pig = PigCard(1)

    print("\nTesting STALL Card activation.")
    test_stall_card = UpgradeCard("STALL")
    print("After creating a pig card.")
    print("Pig has stall. (Expected value: False). Value:", test_pig.has_stall())
    print("After card is activated and STALL card is played:")
    test_pig, destroyed_cards = test_stall_card.activate_card(test_pig)
    print("Pig has stall. (Expected value: True). Value:", test_pig.has_stall())

    print("\nTesting LIGHTNING CONDUCTOR Card activation.")
    test_lightning_conductor_card = UpgradeCard("LIGHTNING_CONDUCTOR")
    print("After creating a pig card.")
    print("Pig has lightning conductor. (Expected value: False). Value:", test_pig.has_lightning_conductor())
    print("After card is activated and LIGHTNING CONDUCTOR card is played:")
    test_pig, destroyed_cards = test_lightning_conductor_card.activate_card(test_pig)
    print("Pig has lightning conductor. (Expected value: True). Value:", test_pig.has_lightning_conductor())

    print("\nTesting ANNOY FARMER Card activation.")
    test_annoy_farmer_card = UpgradeCard("ANNOY_FARMER")
    print("After creating a pig card.")
    print("Pig has door. (Expected value: False). Value:", test_pig.has_door())
    print("After card is activated and LIGHTNING CONDUCTOR card is played:")
    test_pig, destroyed_cards = test_annoy_farmer_card.activate_card(test_pig)
    print("Pig has door. (Expected value: True). Value:", test_pig.has_door())
