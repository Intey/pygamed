# -*- coding: utf-8 -*-

from domain.trap import Trap
from domain.sticks import Sticks
from domain.utils import splitPartition
from actor import Actor


from random import random, randrange

WIDTH = 800
HEIGHT = 600

def randomPos(w, h):
    return (int(random() * w), int(random() * h))


def generateTraps(scrollLayer):
    for i in range(0, 10):
        trap = Actor('assets/trap.png',
                     position=randomPos(WIDTH, HEIGHT),
                     domain=Trap(randrange(1, 30),
                                 randrange(Trap.MIN_RANGE, Trap.MAX_RANGE)))
        scrollLayer.addCollidable(trap)


def generateSticks(scrollLayer):
    for i in range(0, 10):
        sticks = Actor('assets/sticks.png',
                       position=randomPos(WIDTH, HEIGHT),
                       domain=Sticks(randrange(Sticks.MIN, Sticks.MAX)))
        updateSticksCountSprite(sticks)
        scrollLayer.addCollidable(sticks)


# which sprite show when count has value
def updateSticksCountSprite(sticks:Actor):
    from pyglet.resource import image as PImage
    """
    Update sticks sprite by count.
    """
    # partition - prtn
    keys = splitPartition(Sticks.MAX, Sticks.MIN, 4)
    spriteMap = {
            keys[0]: PImage('assets/sticks.png'),
            keys[1]: PImage('assets/sticks-mid.png'),
            keys[2]: PImage('assets/sticks-light.png'),
            keys[3]: PImage('assets/sticks-almost.png')
    }
    vals = spriteMap.keys()
    # if  50 < rest < 75 - show sticks-light
    filtered = list(filter(lambda v: v - sticks.domain.value < 0, vals))
    if not filtered:
        key = min(vals)
    else:
        key = max(filtered)
    print("got key {}, vals {}, real {}".format(key, filtered, sticks.domain.value))
    sticks.image = spriteMap[key]
