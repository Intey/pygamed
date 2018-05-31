# -*- coding: utf-8 -*-

class Unit:
    """
    Manages health state of unit.
    """
    def __init__(self, health=100):
        self._health = health
        self.alive = self.health > 0

    def health():
        doc = "The health property."
        def fget(self):
            return self._health
        def fset(self, value):
            self._health = value
            if value <= 0:
                self.alive = False
        def fdel(self):
            del self._health
        return locals()
    health = property(**health())

    def hit(self, power):
        self.health -= power
        if self.health <= 0:
            self.health = 0
            self.alive = False
