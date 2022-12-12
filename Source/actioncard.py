# -*- coding: utf-8 -*-

""" action card """

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


class ActionCard(Card):

    def __init__(self, card_type):
        super(ActionCard, self).__init__(card_type)

        actioncard_func_map = {
        "MUD"                   : self.mud_on_pig,
        "RAIN"                  : self.rain_on_pig,
        "LIGHTNING"             : self.lightning_on_stall,
        "FARMER_CLEANS"         : self.farmer_cleans_pig,
        "STORM"                 : self.storm,
        }

        # dictionary that maps the method to the action card type
        # keys: Key Word (type) of an action card
        # values: corresponding method that action card type

        self.func = actioncard_func_map[self.card_type]
        # the method of a give action card is defined

    def activate_card(self, pigcard):
        """
        Method takes a PigCard as input and modifies its attributes depending
        on the function of the action card. The modified card is returned. 
        If the pig card was equipped with an upgrade card, the upgrade card is
        destroyed. The key word of the destroyed upgrade card is returned. 
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """
        modified_card, destroyed_cards_keywords = self.func(pigcard)
        return modified_card, destroyed_cards_keywords

    def mud_on_pig(self, pigcard):
        """
        Function of the card "MUD". This method takes a pigcard as input and 
        makes the pig dirty (attribute dirty is set True)
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """

        destroyed_cards = list()
        if not pigcard.is_dirty():
            pigcard.make_dirty()
        return pigcard, destroyed_cards

    def rain_on_pig(self, pigcard):
        """
        Function of the card "RAIN". This method takes a pigcard as input and 
        makes the pig clean (attribute dirty is set False)
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """

        destroyed_cards = list()
        if not pigcard.has_stall():
            pigcard.clean()
        return pigcard, destroyed_cards

    def lightning_on_stall(self, pigcard):
        """
        Function of the card "LIGHTNING". This method takes a pigcard as input
        and destroys its stall if it does not have a lightning conductor. In
        case of the destruction, if it has a door, the door will also be
        destroyed. 
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """

        destroyed_cards = list()
        if pigcard.has_stall() and not pigcard.has_lightning_conductor():
            pigcard.destroy_stall()
            destroyed_cards.append("STALL")
            if pigcard.has_door():
                pigcard.destroy_door()
                destroyed_cards.append("ANNOY_FARMER")
        return pigcard, destroyed_cards

    def farmer_cleans_pig(self, pigcard):
        """
        Function of the card "FARMER CLEANS". This method takes a pigcard as
        input and cleans it, if the pig has no stall with a door.
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """
        # card "FARMER_CLEANS"
        # pigs without door get cleaned by farmer
        destroyed_cards = list()
        if not pigcard.has_door() and pigcard.is_dirty():
            pigcard.clean()
        return pigcard, destroyed_cards

    def storm(self, pigcard):
        """
        Function of the card "STORM". This method takes a pigcard as
        input and destroys its stall, door and lightning conductor.
        
        Parameters
        ----------
        pigcard : PigCard
            An object of the class PigCard is given as input
    
        Returns
        -------
        modified_card : PigCard
            The pig card, which is taken as input, will be returned after
            modification.
        
        destroyed_cards_keywords: list
            The keywords of the destroyed upgrade cards, if the pig was equipped
            with it.

        """

        destroyed_cards = list()
        if pigcard.has_stall():
            pigcard.destroy_stall()
            destroyed_cards.append("STALL")
            if pigcard.has_door():
                pigcard.destroy_door()
                destroyed_cards.append("ANNOY_FARMER")
            if pigcard.has_lightning_conductor():
                pigcard.destroy_lightning_conductor()
                destroyed_cards.append("LIGHTNING_CONDUCTOR")
        return pigcard, destroyed_cards


if __name__ == "__main__":
    test_pig = PigCard(1)

    print("\nTesting MUD Card activation")
    test_mud_card = ActionCard("MUD")
    print("After creating a pig card:")
    print("Pig is dirty. (Expected value: False). Value:", test_pig.is_dirty())
    test_pig, destroyed_cards = test_mud_card.activate_card(test_pig)
    print("After playing MUD card:")
    print("Pig is dirty. (Expected value: True). Value:", test_pig.is_dirty())
    print("Destroyed card. (Expected: Empty list):", destroyed_cards)

    print("\nTesting RAIN Card activation")
    test_rain_card = ActionCard("RAIN")
    print("Pig is dirty. (Expected value: True). Value:", test_pig.is_dirty())
    test_pig, destroyed_cards = test_rain_card.activate_card(test_pig)
    print("After playing RAIN card:")
    print("Pig is dirty. (Expected value: False). Value:", test_pig.is_dirty())
    print("Destroyed card. (Expected: Empty list):", destroyed_cards)

    print("\nTesting LIGHTNING Card activation")
    test_rain_card = ActionCard("LIGHTNING")
    test_pig.build_stall()  # for testing purposes
    print("Pig has stall. (Expected value: True). Value:", test_pig.has_stall())
    test_pig, destroyed_cards = test_rain_card.activate_card(test_pig)
    print("After playing LIGHTNING card:")
    print("Pig has stall. (Expected value: False). Value:", test_pig.has_stall())
    print("Destroyed card: (Expected: STALL):", destroyed_cards)

    print("\nTesting FARMER CLEANS Card activation")
    test_farmer_cleans_card = ActionCard("FARMER_CLEANS")
    test_pig.is_dirty()  # for testing purposes
    print("Pig is dirty. (Expected value: True). Value:", test_pig.is_dirty())
    test_pig, destroyed_cards = test_farmer_cleans_card.activate_card(test_pig)
    print("After playing FARMER CLEANS card:")
    print("Pig is dirty. (Expected value: False). Value:", test_pig.has_stall())
    print("Destroyed card. (Expected: Empty list):", destroyed_cards)

    print("\nTesting STORM Card activation")
    test_storm_card = ActionCard("STORM")
    test_pig.build_stall()  # for testing purposes
    test_pig.build_lightning_conductor()  # for testing purposes
    test_pig.build_door()  # for testing purposes
    print("Pig has stall. (Expected value: True). Value:", test_pig.has_stall())
    print("Pig has door. (Expected value: True). Value:", test_pig.has_door())
    print("Pig has lightning conductor. (Expected value: True). Value:", test_pig.has_lightning_conductor())
    test_pig, destroyed_cards = test_storm_card.activate_card(test_pig)
    print("After playing STORM card:")
    print("Pig has stall. (Expected value: False). Value:", test_pig.has_stall())
    print("Pig has door. (Expected value: False). Value:", test_pig.has_door())
    print("Pig has lightning conductor. (Expected value: False). Value:", test_pig.has_lightning_conductor())
    print("Destroyed cards. (Expected: STALL, ANNOY_FARMER, LIGHTNING_CONDUCTOR):", destroyed_cards)
