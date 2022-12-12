# -*- coding: utf-8 -*-

""" pig card """

__author__     = 'Salah Xaaji'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '28.11.2022'
__maintainer__ = 'Salah Xaaji'
__email__      = 'xaajisal@students.zhaw.ch'
__status__     = 'done'


from card import Card


class PigCard(Card):

    def __init__(self, n_pig):
        # A pig card can have different attributes depending on the action
        # and upgrade cards played.
        self.dirty = False
        self.stall = False
        self.door = False
        self.lightning_conductor = False

        # Each object of this class gets a Number to identify which pig
        # of the game it is. Number is taken as input from the game (see
        # class "Game").
        self.n_pig = n_pig

        super(PigCard, self).__init__("PIG")

        self.status_bool = list()
        # status_bool is a list containing the different pig attributes
        # as booleans.

        self.status = ("Dreckssau", "Stall", "Türe", "Blitzableiter")
        # All the possible statuses a pig can have. Depending on the
        # boolean list 'status_bool'.

    def is_dirty(self):
        """
        Returns True if the pig is dirty (self.dirty = True) and False if it's clean (self.dirty = False).

        Parameters
        ----------
        None.

        Returns
        -------
        self.dirty : bool
            boolean indicates if pig is dirty or clean

        """
        return self.dirty

    def make_dirty(self):
        """
        Changes the attribute self.dirty to True (indicates a dirty pig)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig is dirty (self.dirty = True) True is returned

        """
        self.dirty = True
        return True

    def clean(self):
        """
        Changes the attribute self.dirty to False (indicates a clean pig)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig is clean (self.dirty = False) True is returned.

        """
        self.dirty = False
        return True

    def has_stall(self):
        """
        Returns True if the pig has a stall (self.stall = True) and False if it does not (self.stall = False).

        Parameters
        ----------
        None.

        Returns
        -------
        self.stall : bool
            boolean indicates if pig has a stall or not

        """
        return self.stall

    def build_stall(self):
        """
        Changes the attribute self.stall to True (pig has a stall)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig has stall (self.stall = True) True is returned

        """
        self.stall = True
        return True

    def destroy_stall(self):
        """
        Changes the attribute self.stall to False (pig has no stall)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig has no stall (self.stall = False) True is returned

        """
        self.stall = False
        return True

    def has_door(self):
        """
        Returns True if the pig stall has a door (self.door = True) and False if it does not (self.door = False).

        Parameters
        ----------
        None.

        Returns
        -------
        self.door : bool
            boolean indicates if pig stall has a door or not

        """
        return self.door

    def build_door(self):
        """
        Changes the attribute self.door to True (pig stall has a door)

        Parameters
        ----------
        None.

        Returns
        -------
        True : boolean
            If pig has door (self.door = True) True is returned

        """
        self.door = True
        return True

    def destroy_door(self):
        """
        Changes the attribute self.door to False (pig stall has no door)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig has no door (self.door = False) True is returned

        """
        self.door = False
        return True

    def has_lightning_conductor(self):
        """
        Returns True if the pig stall has a lightning conductor (self.lightning_conductor = True)
        and False if it does not (self.lightning_conductor = False).

        Parameters
        ----------
        None.

        Returns
        -------
        self.lightning_conductor : bool
            boolean indicates if pig stall has a lightning conductor or not

        """
        return self.lightning_conductor

    def build_lightning_conductor(self):
        """
        Changes the attribute self.lightning_conductor to True
        (pig stall has a lightning conductor)

        Parameters
        ----------
        None.

        Returns
        -------
        True : boolean
            If pig stall has lightning conductor (self.lightning_conductor = True) True is returned

        """
        self.lightning_conductor = True
        return True

    def destroy_lightning_conductor(self):
        """
        Changes the attribute self.lightning_conductor to False
        (pig stall has no lightning conductor)

        Parameters
        ----------
        None.

        Returns
        -------
        True : bool
            If pig stall has no lightning conductor (self.lightning_conductor = False) True is returned

        """
        self.lightning_conductor = False
        return True

    def get_pig_number(self):
        """
        Returns the number of the pig.

        Parameters
        ----------
        None.

        Returns
        -------
        self.n_pig : int
            The number of the pig in a given game.

        """
        return self.n_pig

    def get_current_status(self):
        """
        Method returns a list of all the acquired attributes of the pig.
        The list contains only the statuses where the according attribute of
        the pig is set on True.

        Parameters
        ----------
        None.

        Returns
        -------
        current_status : bool
            Returns list of names according to the boolean status of all possible attributes of a pig card

        """
        self.update_status_bool()
        counter = 0
        current_status = ["Sauberschwein"]
        for element in self.status_bool:
            if element:
                if not counter:
                    current_status.remove("Sauberschwein")
                current_status.append(self.status[counter])
            counter += 1
        return current_status

    def update_status_bool(self):
        """
        Updates the status_bool list of the pig.

        Parameters
        ----------
        None.

        Returns
        -------
        self.status_bool : list
            Returns list of boolean status of all possible attributes of a pig card
            
        """
        self.status_bool =  [
            self.dirty, self.stall, self.door, self.lightning_conductor
                            ]
        return self.status_bool


if __name__ == "__main__":
    first_pig = PigCard(1)
    second_pig = PigCard(2)
    third_pig = PigCard(3)

    print("\nGet current status of pig card")
    print("Expected: Sauberschwein")
    print("Status:", first_pig.get_current_status())

    print("\nTest method is_dirty")
    print("Expected value: False")
    print("Value:", first_pig.is_dirty())

    print("\nTest method make_dirty")
    first_pig.make_dirty()
    print("Get current status of pig card")
    print("Expected: Drecksau")
    print("Status:", first_pig.get_current_status())

    print("\nTest method is_dirty")
    print("Expected value: True")
    print("Value:", first_pig.is_dirty())

    print("\nTest method clean")
    first_pig.clean()
    print("Get current status of pig card")
    print("Expected: Sauberschwein")
    print("Status:", first_pig.get_current_status())

    print("\nTest method has_stall")
    print("Expected value: False")
    print("Value:", first_pig.has_stall())

    print("\nTest method build_stall")
    first_pig.build_stall()
    print("Get current status of pig card")
    print("Expected: Sauberschwein, Stall")
    print("Status:", first_pig.get_current_status())

    print("\nTest method has_stall")
    print("Expected value: True")
    print("Value:", first_pig.has_stall())

    print("\nTest method destroy_stall")
    first_pig.destroy_stall()
    print("Get current status of pig card")
    print("Expected: Sauberschwein")
    print("Status:", first_pig.get_current_status())

    print("\nTest method has_door")
    print("Expected value: False")
    print("Value:", first_pig.has_stall())

    print("\nTest method build_door")
    first_pig.build_door()
    print("Get current status of pig card")
    print("Expected: Sauberschwein, Türe")
    print("Status:", first_pig.get_current_status())
    print("Hint: Validation of possible moves is implemented in game.py")

    print("\nTest method has_door")
    print("Expected value: True")
    print("Value:", first_pig.has_door())

    print("\nTest method destroy_door")
    first_pig.destroy_door()
    print("Get current status of pig card")
    print("Expected: Sauberschwein")
    print("Status:", first_pig.get_current_status())

    print("\nTest method has_door")
    print("Expected value: False")
    print("Value:", first_pig.has_door())

    print("\nTest method has_lightning_conductor")
    print("Expected value: False")
    print("Value:", first_pig.has_lightning_conductor())

    print("\nTest method build_lightning_conductor")
    first_pig.build_lightning_conductor()
    print("Get current status of pig card")
    print("Expected: Sauberschwein, Blitzableiter")
    print("Status:", first_pig.get_current_status())
    print("Hint: Validation of possible moves is implemented in game.py")

    print("\nTest method has_lightning_conductor")
    print("Expected value: True")
    print("Value:", first_pig.has_lightning_conductor())

    print("\nTest method has_lightning_conductor")
    print("Expected value: True")
    print("Value:", first_pig.has_lightning_conductor())

    print("\nTest method destroy_lightning_conductor")
    first_pig.destroy_lightning_conductor()
    print("Get current status of pig card")
    print("Expected: Sauberschwein")
    print("Status:", first_pig.get_current_status())

    print("\nTest method has_lightning_conductor")
    print("Expected value: False")
    print("Value:", first_pig.has_lightning_conductor())

    print("\nTest method get_pig_number")
    print("Pig Number 1:", first_pig.get_pig_number())
    print("Pig Number 2:", second_pig.get_pig_number())
    print("Pig Number 3:", third_pig.get_pig_number())

    first_pig.make_dirty()
    first_pig.build_stall()
    first_pig.build_door()
    first_pig.build_lightning_conductor()

    second_pig.build_stall()

    third_pig.build_lightning_conductor()

    print("\nTest method update_status_bool")
    print("Status:", first_pig.update_status_bool())
    print("Status:", second_pig.update_status_bool())
    print("Status:", third_pig.update_status_bool())
    print("Hint: Validation of possible moves is implemented in game.py")

