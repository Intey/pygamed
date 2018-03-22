# -*- coding: utf-8 -*-

class Unit:
    """
    Manages health state of unit.
    """
    def __init__(self, health=100):
        self.health = health
        self.alive = self.health > 0

    def hit(self, power):
        self.health -= power
        if self.health <= 0:
            self.health = 0
            self.alive = False
