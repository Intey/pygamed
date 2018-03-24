# -*- coding: utf-8 -*-

from domain.trap import Trap
from domain.sticks import Sticks
from domain.utils import splitPartition
from actor import Actor


from random import random, randrange

import logging

logger = logging.getLogger(__name__)

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

    # map count to sprite. Distribute 4 point between MIN-MAX
    keys = splitPartition(Sticks.MIN, Sticks.MAX, 4)
    spriteMap = {
            keys[0]: PImage('assets/sticks.png'),
            keys[1]: PImage('assets/sticks-mid.png'),
            keys[2]: PImage('assets/sticks-light.png'),
            keys[3]: PImage('assets/sticks-almost.png')
    }
    key = selectKey(sticks.domain.value, keys)
    sticks.image = spriteMap[key]


def selectKey(count:int, keys:list):
    # if  50 < rest < 75 - show sticks-light
    # get keys, that >= sticks.domain.value
    filtered = list(filter(lambda key: key - count <= 0, keys))
    # if count more than some key, get max key
    key = keys[0]
    if filtered:
        # have some
        key = max(filtered)
    else:
        # get lowest
        key = keys[-1]
    logger.debug(f"use sprite key {key} from mapped values {filtered}. Real sticks count - {count}")
    return key

