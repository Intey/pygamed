# -*- coding: utf-8 -*-
from domain.unit import Unit


class Player(Unit):
    def __init__(self, health=100):
        Unit.__init__(self, health=health)
        # TODO: extract to collector
        self.collectSpeed = 0.5
        self.collectCount = 2
        self.inventory = {}
