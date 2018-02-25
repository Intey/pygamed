# -*- coding: utf-8 -*-

"""
Collide resposibility is return actions, that
"""

from .player import Player
from .trap import Trap
from .bear import Bear
from .sticks import Sticks
from collections import defaultdict

from logging import getLogger

logger = getLogger(__name__)

def collide(left, right, distance:int):
    """
    Collide wrapper. Call realCollider function by objects types.
    make collision action. Decrease health, buff, stun, decrease speed on time,
    etc.
    """
    lc = left.__class__
    rc = right.__class__

    logger.debug(f"collide {lc}, {rc}")

    rightStay = __COLLIDE_MAP[(lc, rc)](left, right)
    leftStay = __COLLIDE_MAP[(rc, lc)](right, left)

    logger.debug(f"stay: left {leftStay}, right {rightStay}")
    return leftStay, rightStay


def noop(left, right):
    return True


def drop(left, right):
    return False


def damagePlayerByTrap(trap:Trap, player:Player):
    oldh = player.health
    player.hit(trap.power)
    logger.debug(f"damage {trap.power}:{oldh} -> {player.health}")
    return player.alive


# should return state of right(object) of action: removed or stay in game
__COLLIDE_MAP = defaultdict(lambda: noop)
__COLLIDE_MAP[(Trap, Trap)]   = drop
__COLLIDE_MAP[(Trap, Player)] = damagePlayerByTrap
__COLLIDE_MAP[(Player, Trap)] = drop
__COLLIDE_MAP[(Player, Bear)] = noop
__COLLIDE_MAP[(Bear, Player)] = noop
__COLLIDE_MAP[(Player, Sticks)] = noop
__COLLIDE_MAP[(Sticks, Player)] = noop
__COLLIDE_MAP[(Sticks, Sticks)] = drop


