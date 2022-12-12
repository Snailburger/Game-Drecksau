# -*- coding: utf-8 -*-

""" Game functionality """

__author__     = 'Ricky Raths'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Ricky Raths'
__email__      = 'rathsric@students.zhaw.ch'
__status__     = 'done'

from colorama import Fore, Back, Style
from validator import Validator
from pigcard import PigCard
from actioncard import ActionCard
from upgradecard import UpgradeCard
from player import Player
from deck import Deck


class Game:

    def __init__(self):
        self.validate = Validator()
        self.deck = Deck()

        self.players = list()  # a list of the players playing a game
        self.active_player = None
        self.running = False # True if done

        self.card_map = {
            "MUD": self.mud, "RAIN": self.rain, "LIGHTNING": self.lightning,
            "FARMER_CLEANS": self.farmer_cleans, "STORM": self.storm,
            "STALL": self.stall, "LIGHTNING_CONDUCTOR": self.lightning_conductor,
            "ANNOY_FARMER": self.annoy_farmer}

        
    def run_game(self):
        """
        The main method. It runs until the game is over (when a player wins)
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        # init game
        self.init_game()
        round_counter = 0

        # one players move
        while self.running:
            # define active player for this round
            self.active_player = self.players[round_counter % len(self.players)]
            # get the hand cards of the active player
            hand_cards = self.active_player.get_cards_hand()

            self.show_all_cards_on_table()
            print(Back.CYAN + "\n" + self.active_player.get_name() + "'s Zug:" + Style.RESET_ALL)
            self.active_player.show_cards_in_hand()

            if self.can_player_play_card(hand_cards):  #if player can play a card
                choice = self.choose_play_or_change_card()
                if choice == 1:
                    # play card
                    card, activations = self.play_card()
                    # make changes
                    destroyed_cards = self.activate_card(card, activations)
                    # replace the played card
                    self.replace_hand_card(card)
                    if not card.get_card_type() in list(card.upgrade_card_types.keys()):
                        self.deck.add_card_to_discard_pile(card)
                    # move destroyed cards to discard pile
                    if destroyed_cards:
                        self.add_destroyed_cards_to_discard_pile(destroyed_cards)
                else:
                    # change one card
                    n_card_to_change = self.choose_card(change=True)
                    card = self.active_player.get_card_hand(n_card_to_change)
                    self.replace_hand_card(card)
                    self.deck.add_card_to_discard_pile(card)
            else:
                # player has to change one card or all cards
                choice = self.choose_to_change_one_or_all_cards()
                if choice == 1:
                    # player chooses to change one card
                    n_card_to_change = self.choose_card(change=True)
                    card = self.active_player.get_card_hand(n_card_to_change)
                    self.replace_hand_card(card)
                    self.deck.add_card_to_discard_pile(card)
                else:
                    # player chooses to change all cards
                    cards = self.active_player.get_cards_hand()
                    cards_name = [card.get_name() for card in cards]
                    self.change_all_cards()
                    print("\n" + self.active_player.get_name() + " hat alle Karten gewechselt: " + ", ".join(cards_name))
            self.check_winner()
            round_counter += 1
        print("Ende des Spiels")

    # init game
    def init_game(self):
        """
        Initializes the game. Calls methods to initialize the players, the cards 
        on the table and the cards for the hands.
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        print("Wilkommen bei Drecksau!")
        self.init_players()
        self.init_cards_table()
        self.init_cards_hand()
        print("\nLass uns beginnen:")
        self.running = True

    def init_players(self):
        """
        Initializes the players. For every player it calls the method 
        create_player
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        n_players = self.number_of_players()
        for i in range(n_players):
            self.create_player(i)

    def number_of_players(self):
        """
        Gets the desired number of players from the input and validates the 
        input with the validator class
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        valid_input = False
        while not valid_input:
            n_players = input("Wie viele Spieler spielen mit? ")
            valid_input = self.validate.number_of_players(n_players)
        return int(n_players)

    def create_player(self, i):
        """
        Gets the desired name of the player, creates a Player object and appends
        it to the players list
    
        Parameters
        ----------
        i : int
            The number of the asked player.

        Returns
        -------
        None.

        """
        player_name = str(input("Was ist der Name des Spieler " + str(i + 1) + "? "))
        self.players.append(Player(player_name))

    # init cards table
    def init_cards_table(self):
        """
        Initializes the cards on the table for every player in the game.
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        n_pigs = self.number_of_pigs()
        for player in self.players:
            for n in range(n_pigs):
                player.add_card_to_table(PigCard(n + 1))

    def number_of_pigs(self):
        """
        Determine how many pigs each player should have.
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        n_players = len(self.players)
        if n_players == 2:
            n_pigs = 5
        elif n_players == 3:
            n_pigs = 4
        elif n_players == 4:
            n_pigs = 3
        return n_pigs

    # init cards hand
    def init_cards_hand(self):
        """
        Initializes the cards on the hand of every player in the game. This is 
        done by just getting 3 cards to every player and place them in their 
        hands.
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """
        for player in self.players:
            for i in range(3):
                new_card = self.deck.deal_card()
                player.add_card_to_hand(new_card)

# game
    def play_card(self):
        """
        Initializes the cards on the hand of every player in the game. This is 
        done by just getting 3 cards to every player and place them in their 
        hands.
    
        Parameters
        ----------
        None.

        Returns
        -------
        (card : Card , activations : list) : tuple

        """
        card, possible_moves = self.choose_card_to_play()
        card_type = card.get_card_type()
        if card_type == "RAIN" or card_type == "STORM":
            # activations contains all the player-card combos,
            # that the card is being used on
            activations = possible_moves
            # in this case: the card is being used on all the pigcards
        else:
            activations = [self.choose_move(possible_moves)]
            # the card is only being used on the move the player chose
        return card, activations

    def choose_card_to_play(self):
        """
        Lets the user choose a card to play and gets the possible moves.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        card, possible_moves : tuple
            The card which the user wants to play and the possible moves he can 
            do with this card

        """
        valid_input = False
        while not valid_input:
            n_card = self.choose_card()
            card = self.active_player.get_card_hand(n_card)
            possible_moves = self.get_possible_moves_for_card(card)
            valid_input = self.validate.move_is_possible(possible_moves)
        return card, possible_moves

    def activate_card(self, card, activations):
        """
        Activates the played card effect.
    
        Parameters
        ----------
        card : Card
            The played card, whose effect has to be executed
        activations :  tuple
            Tuple that contains the target pig and the target player of the card
            effect
        
        Returns
        -------
        destroyed_cards : list
            All the cards that got destroyed and have to be created again.

        """
        for target_player, target_pig in activations:
            updated_pig, destroyed_cards = card.activate_card(target_pig)
            target_player.update_card_table(updated_pig)
        return destroyed_cards

    def show_all_cards_on_table(self):
        """
        For every player in the game, the method show_cards_on_table is called, 
        which will display all pigs of the player.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.

        """
        for player in self.players:
            player.show_cards_on_table()

    def replace_hand_card(self, card):
        """
        Replaces a specific card from the players hand.
    
        Parameters
        ----------
        card: Card
            The card which will be replaced
        
        Returns
        -------
        None.

        """
        self.active_player.del_card_hand(card)
        new_card = self.deck.deal_card()
        self.active_player.add_card_to_hand(new_card)

    def change_all_cards(self):
        """
        Changes all three hand cards of the currentyl active player.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        None.

        """
        for i in range(3):
            old_card = self.active_player.get_card_hand(1)
            self.active_player.del_card_hand(old_card)
            self.deck.add_card_to_discard_pile(old_card)
            new_card = self.deck.deal_card()
            self.active_player.add_card_to_hand(new_card)

    def add_destroyed_cards_to_discard_pile(self, cards_type):
        """
        Adds the destroyed cards to the discard pile.
    
        Parameters
        ----------
        cards_tpye : list
            List of card types that got destroyed.
        
        Returns
        -------
        None.

        """
        for card_type in cards_type:
            self.deck.add_destroyed_card_to_discard_pile(card_type)

    def can_player_play_card(self, hand_cards):
        """
        Checks if the player can play a card on his hand.
    
        Parameters
        ----------
        hand_cards : list
            List of Cards in players hand.
        
        Returns
        -------
        he_can : bool
            Determines if player can play a card or not.

        """
        he_can = False
        for card in hand_cards:
            moves = self.get_possible_moves_for_card(card)
            if moves:
                he_can = True
        return he_can

    def check_winner(self):
        """
        Checks if a player has only dirty pigs and therefor has won the game. If 
        someone has won the game, it stops the game from running.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        None

        """
        winner = True
        for pig in self.active_player.get_cards_table():
            if not pig.is_dirty():
                winner = False
        if winner:
            self.running = False
            print(Back.GREEN + "\nDer Gewinner ist " + self.active_player.get_name() + Style.RESET_ALL)

# interaction players
    def choose_play_or_change_card(self):
        """
        Lets the user choose if he wants to play a card or if he wants to change 
        a card. It will retry until the user has entered a valid choice.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        choice : int
            The number which the player has entered. 1 for play a card, 2 for
            change a card.

        """
        valid_input = False
        while not valid_input:
            choice = input("\n1: Spiele eine Karte\n" +
                           "2: Wechsle eine Karte\n" +
                           "Willst du eine Karte spielen oder eine Karte wechseln? [1/2] ")
            valid_input = self.validate.choose_play_or_change_card(choice)
        return int(choice)

    def choose_to_change_one_or_all_cards(self):
        """
        Lets the user choose if he wants to change only one card, or all three 
        of his cards. It will retry until the user has entered a valid choice.
    
        Parameters
        ----------
        None.
        
        Returns
        -------
        choice : int
            The number which the player has entered. 1 for change one card, 2 
            for change all cards. It will retry until the user has entered a 
            valid choice.

        """
        print("Du kannst keine Karte spielen")
        valid_input = False
        while not valid_input:
            choice = input("\n1: Wechsle eine Karte\n" +
                           "2: Wechsle alle Karten\n" +
                           "Willst du eine Karte wechseln oder alle Karten wechseln? [1/2] ")
            valid_input = self.validate.choose_to_change_one_or_all_cards(choice)
        return int(choice)

    def choose_card(self, change=False):
        """
        Lets the user choose one of his cards to play or to change. It will 
        retry until the user has entered a valid choice.
    
        Parameters
        ----------
        change : bool
            Indicates if the player wants to change the card. If not given, this
            bool is set to False
        
        Returns
        -------
        choice : int
            The number which the player has entered. It associates with the 
            displayed card next to this number.

        """
        valid_input = False
        while not valid_input:
            if not change:
                choice = input("Welche Karte willst du spielen? [1/2/3] ")
            else:
                choice = input("Welche Karte willst du wechseln? [1/2/3] ")
            valid_input = self.validate.choose_card(choice)
        return int(choice)

    def choose_move(self, possible_moves):
        """
        Lets the user choose one of the possible moves. It will retry until the 
        user has entered a valid choice.
    
        Parameters
        ----------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        
        Returns
        -------
        move : tuple
            Contains the move, that the player has chosen. The tuple contains 
            the player and the associated pig.

        """
        valid_input = False
        while not valid_input:
            self.show_possible_moves(possible_moves)
            choice = input("Wo willst du diese Karte spielen? ")
            valid_input = self.validate.choose_move(choice, possible_moves)
        move = possible_moves[int(choice) - 1]
        return move

# possible moves
    def get_possible_moves_for_card(self, card):
        """
        Returns all the possible moves which are determined by the given card 
        which the player wants to play. This is done by calling the function of 
        the card with the card map.
    
        Parameters
        ----------
        card : Card
            Contains the card that the player wants to play.
        
        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.

        """
        card_type = card.get_card_type()
        possible_moves = self.card_map[card_type]()
        return possible_moves

    def show_possible_moves(self, possible_moves):
        """
        Prints all the possible moves for a specific card in order to give the 
        player a selection of moves
    
        Parameters
        ----------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        
        Returns
        -------
        None.

        """
        counter = 1
        print("\nMögliche Züge für diese Karte")
        for player, pig in possible_moves:
            n_pig = pig.get_pig_number()
            player_name = player.get_name()
            if player == self.active_player:
                player_name = "Eigenes"
            print(str(counter) + ": " + player_name + "'s Schwein " + str(n_pig))
            counter += 1

    def mud(self):
        """
        Method returns a list with all possible moves for playing the card mud
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        for player, pig in player_pigs:
            if not pig.is_dirty():
                possible_moves.append((player, pig))
        return possible_moves

    def rain(self):
        """
        Method returns a list with all possible moves for playing the card rain
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        opponents_pigs = self.get_opponents_pigs()
        players_pigs = player_pigs + opponents_pigs
        for player, pig in players_pigs:
            if pig.is_dirty() and not pig.has_stall():
                possible_moves.append((player, pig))
        return possible_moves

    def lightning(self):
        """
        Method returns a list with all possible moves for playing the card 
        lightning
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        opponents_pigs = self.get_opponents_pigs()
        for opponent, pig in opponents_pigs:
            if pig.has_stall() and not pig.has_lightning_conductor():
                possible_moves.append((opponent, pig))
        return possible_moves

    def farmer_cleans(self):
        """
        Method returns a list with all possible moves for playing the card 
        farmer cleans
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        opponents_pigs = self.get_opponents_pigs()
        for opponent, pig in opponents_pigs:
            if pig.is_dirty() and not pig.has_door():
                possible_moves.append((opponent, pig))
        return possible_moves

    def storm(self):
        """
        Method returns a list with all possible moves for playing the card storm
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        opponents_pigs = self.get_opponents_pigs()
        players_pigs = player_pigs + opponents_pigs
        for player, pig in players_pigs:
            if pig.has_stall():
                possible_moves.append((player, pig))
        return possible_moves

    def stall(self):
        """
        Method returns a list with all possible moves for playing the card stall
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        for player, pig in player_pigs:
            if not pig.has_stall():
                possible_moves.append((player, pig))
        return possible_moves

    def lightning_conductor(self):
        """
        Method returns a list with all possible moves for playing the card 
        lightning conductor
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        for player, pig in player_pigs:
            if pig.has_stall() and not pig.has_lightning_conductor():
                possible_moves.append((player, pig))
        return possible_moves

    def annoy_farmer(self):
        """
        Method returns a list with all possible moves for playing the card 
        annoy farmer
    
        Parameters
        ----------
        None.

        Returns
        -------
        possible_moves : list
            This list contains all the possible moves in form of a tuple. The 
            tuple contains the player and the associated pig.
        """
        possible_moves = list()
        player_pigs = self.get_active_player_pigs()
        for player, pig in player_pigs:
            if pig.has_stall() and not pig.has_door():
                possible_moves.append((player, pig))
        return possible_moves

    def get_active_player_pigs(self):
        """
        Method returns a list with tuples that contain the active player and the 
        pigs.
    
        Parameters
        ----------
        None.

        Returns
        -------
        player_pigs : list
            This list contains all the pigs of the currently active player. The 
            list entries are tuples which contain the player and the associated
            pig.
        """
        player_pigs = list()
        pigs = self.active_player.get_cards_table()
        for pig in pigs:
            player_pigs.append((self.active_player, pig))
        return player_pigs

    def get_opponents_pigs(self):
        """
        Method returns a list of all opposing pigs
    
        Parameters
        ----------
        None.

        Returns
        -------
        player_pigs : list
            This list contains all the pigs of the opposing players. The list 
            entries are tuples wich contain the player and the associated pig.
        """
        players_pigs = list()
        opponents = self.get_opponents()
        for opponent in opponents:
            pigs = opponent.get_cards_table()
            for pig in pigs:
                players_pigs.append((opponent, pig))
        return players_pigs

    def get_opponents(self):
        """
        Method returns a list of all opposing players
    
        Parameters
        ----------
        None.

        Returns
        -------
        opponents : list
            This list contains all the opposing players of the current player
        """
        opponents = list()
        for player in self.players:
            if player != self.active_player:
                opponents.append(player)
        return opponents


if __name__ == "__main__":
    drecksau = Game()
    drecksau.players = [Player("P1"), Player("P2")]
    
    # Test methods
    print("\nTest: methods of class Game")

    # Method: number_of_pigs
    print("\nTest: method number_of_pigs")
    print("(Expected value: 5). Value: ", drecksau.number_of_pigs())

    # Method: init_cards_table
    print("\nTest: method init_cards_table")
    drecksau.init_cards_table()
    print("(Expected value: 5). Value: ", len(drecksau.players[0].cards_table))
    print("(Expected value: 5). Value: ", len(drecksau.players[1].cards_table))

    # Method: init_cards_hand
    print("\nTest: method init_cards_hand")
    drecksau.init_cards_hand()
    print("(Expected value: 3). Value: ", len(drecksau.players[0].cards_hand))
    print("(Expected value: 3). Value: ", len(drecksau.players[1].cards_hand))

    # Method: activate_card
    activations = [(drecksau.players[1], drecksau.players[1].cards_table[0])]
    drecksau.activate_card(ActionCard("MUD"), activations)
    
    # Method: show_all_cards_on_table
    print("\nTest: method show_all_cards_on_table")
    drecksau.show_all_cards_on_table()

    # Method: replace_hand_card
    print("\nTest: method replace_hand_card")
    drecksau.active_player = drecksau.players[1]
    print("First card in hand before:", drecksau.players[1].get_card_hand(0).name)
    drecksau.replace_hand_card(drecksau.players[1].get_card_hand(0))
    print("First card in hand after:", drecksau.players[1].get_card_hand(0).name)

    # Method: change_all_cards
    print("\nTest: method change_all_cards")
    print("Cards in hand before:")
    drecksau.players[1].show_cards_in_hand()
    drecksau.change_all_cards()
    print("\nCards in hand after:")
    drecksau.players[1].show_cards_in_hand()

    # Method: add_destroyed_cards_to_discard_pile

    # Method: can_player_play_card
    print("\nTest: method can_player_play_card")
    drecksau.players[1].cards_hand[0] = ActionCard("MUD")
    print("(Expected value: True). Value: ", drecksau.can_player_play_card(drecksau.players[1].cards_hand))

    # Method: check_winner
    print("\nTest: method check_winner")
    drecksau.running = True
    print("(Expected value: True). Value: ", drecksau.running)
    activations = [(drecksau.players[1], drecksau.players[1].cards_table[1]), (drecksau.players[1], drecksau.players[1].cards_table[2]), (drecksau.players[1], drecksau.players[1].cards_table[3]), (drecksau.players[1], drecksau.players[1].cards_table[4])]
    drecksau.activate_card(ActionCard("MUD"), activations)
    drecksau.check_winner()
    print("(Expected value: False). Value: ", drecksau.running)

    # Method: get_possible_moves_for_card and show_possible_moves
    print("\nTest: method get_possible_moves_for_card and show_possible_moves")
    print("(Expected value: []). Value: ", drecksau.get_possible_moves_for_card(ActionCard("MUD")))
    print("\nPossible pigs for card stall:")
    drecksau.show_possible_moves(drecksau.get_possible_moves_for_card(UpgradeCard("STALL")))

    # Method: farmer_cleans
    print("\nTest: method farmer_cleans")
    activations = [(drecksau.players[0], drecksau.players[0].cards_table[0])]
    drecksau.activate_card(ActionCard("MUD"), activations)
    possible_moves = drecksau.farmer_cleans()
    drecksau.show_possible_moves(possible_moves)

    # Method: mud
    print("\nTest: method mud")
    activations = [(drecksau.players[1], drecksau.players[1].cards_table[0])]
    drecksau.activate_card(ActionCard("FARMER_CLEANS"), activations)

    possible_moves = drecksau.mud()
    drecksau.show_possible_moves(possible_moves)

    # Method: rain
    print("\nTest: method rain")
    possible_moves = drecksau.rain()
    drecksau.show_possible_moves(possible_moves)
    
    # Method: lightning
    print("\nTest: method lightning")
    activations = [(drecksau.players[0], drecksau.players[0].cards_table[0])]
    drecksau.activate_card(UpgradeCard("STALL"), activations)

    possible_moves = drecksau.lightning()
    drecksau.show_possible_moves(possible_moves)

    # Method: storm
    print("\nTest: method storm")
    activations = [(drecksau.players[1], drecksau.players[1].cards_table[4])]
    drecksau.activate_card(UpgradeCard("STALL"), activations)

    possible_moves = drecksau.storm()
    drecksau.show_possible_moves(possible_moves)

    # Method: annoy_farmer
    print("\nTest: method annoy_farmer")
    activations = [(drecksau.players[1], drecksau.players[1].cards_table[2])]
    drecksau.activate_card(UpgradeCard("STALL"), activations)
    possible_moves = drecksau.annoy_farmer()
    drecksau.show_possible_moves(possible_moves)

    # Method: stall
    print("\nTest: method stall")
    possible_moves = drecksau.stall()
    drecksau.show_possible_moves(possible_moves)

    


    


    



    


    
    

