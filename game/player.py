# -*- coding: utf-8 -*-


class Player:
    def __init__(self):
        self.health = 100
        self.alive = True
    
    def hit(self, power):
        self.health - power
        if self.health <= 0:
            self.health = 0
            self.alive = False
