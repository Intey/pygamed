# -*- coding: utf-8 -*-
from .inventory import Inventory
from .unit import Unit


class Player(Unit):
    """
    Player login.
    collectSpeed - how many resource player can collect in second
    """
    def __init__(self, health=100):

        Unit.__init__(self, health=health)
        # TODO: extract to collector
        self.collectSpeed = 2
        self.inventory = Inventory()
