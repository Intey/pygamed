# -*- coding: utf-8 -*-


class Player:
    def __init__(self):
        self.health = 100
        self.alive = True
        # TODO: extract to collector
        self.collectSpeed = 0.5
        self.collectCount = 2
        self.inventory = {}

    def hit(self, power):
        self.health -= power
        if self.health <= 0:
            self.health = 0
            self.alive = False

        print("hit!", self.health)
