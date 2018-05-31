# -*- coding: utf-8 -*-

class Unit:
    """
    Manages health state of unit.
    """
    def __init__(self, health=100):
        self._health = health
        self.alive = self.health > 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value <= 0:
            self.alive = False
            self._health = 0
        else:
            self._health = value

    def hit(self, power):
        self.health -= power
