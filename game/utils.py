# -*- coding: utf-8 -*-
from .bot import Bot
from random import random


def distance(fromLoc, toLoc):
    pass


def location(object):
    pass


def inRange(trap, unit):
    return trap.range() <= distance(location(trap), location(unit))


def activateTrap(trap, unit):
    if inRange(trap, unit):
        unit.hit(trap.power())


def initializeGame(config):
    players = (Player(team=1), Bot(team=2))
    # prepare map
    gameMap = generateMap()


def randomPosition(size, width, height):
    cx = size + random() * (width - 2.0 * size)
    cy = size + random() * (height - 2.0 * size)
    return cx, cy
