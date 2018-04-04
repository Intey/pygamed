# -*- coding: utf-8 -*-

from cocos.collision_model import CircleShape
import cocos.euclid as eu
from cocos.sprite import Sprite

TILE_WIDTH = 15

class Actor(Sprite):

    def __init__(self, spriteFilepath:str, position:tuple=(0, 0), domain=None):
        Sprite.__init__(self, spriteFilepath)
        self.position = position
        self.cshape = CircleShape(eu.Vector2(*self.position), TILE_WIDTH)
        self.setPos(self.position)
        self.domain = domain
        self.velocity = 0, 0

    def setPos(self, position:tuple):
        """
        Locate sprite with it's collide part on given position.
        Cshape will be centered on position
        """
        assert isinstance(position, tuple), "should be tuple"
        self.position = position
        self.cshape.center = eu.Vector2(*position)
