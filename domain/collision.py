# -*- coding: utf-8 -*-

"""
Collide resposibility is return actions, that
"""

from itertools import permutations, combinations_with_replacement
from logging import getLogger
from collections import defaultdict

from domain.player import Player
from domain.trap import Trap
from domain.bear import Bear
from domain.sticks import Sticks
from domain.unit import Unit
from domain.noop import noop


logger = getLogger(__name__)


def collide(left:Unit, right:Unit, distance:int):
    """
    Collide wrapper. Call realCollider function by objects types.
    make collision action. Decrease health, buff, stun, decrease speed on time,
    etc.
    """

    lcls = left.__class__
    rcls = right.__class__
    # left to right function
    lrf = __COLLIDE_MAP[(lcls, rcls)]
    # right to left function
    rlf = __COLLIDE_MAP[(rcls, lcls)]
    rightStay = lrf(left, right)
    leftStay = rlf(right, left)

    logger.debug(f"collide({lrf}, {rlf}): lclass(stay),rclass(stay): {left.__class__.__name__}({leftStay}), {right.__class__.__name__}({rightStay}).")
    return leftStay, rightStay


def drop(left, right):
    return False


def damageUnitByTrap(trap:Trap, unit:Unit):
    oldh = unit.health
    unit.hit(trap.power)
    logger.debug(f"damage {trap.power}:{oldh} -> {unit.health}")
    return unit.alive

def slowDownUnit(trap:Trap, unit:Unit):
    unit_alive = damageUnitByTrap(trap, unit)
    if unit_alive:
        unit.speed -= 5
    return unit_alive


def hitByBear(bear: Bear, unit:Unit):
    unit.hit(bear.power)
    return unit.alive


# function should return True, if second(right) argument shouldStay in game or
# False if it should be removed
def create_collide_map():
    collide_map = dict()
    # dummy fill

    class_list = [Bear, Player, Sticks, Trap]
    variants = set(list(permutations(class_list, 2)) + \
                   list(combinations_with_replacement(class_list, 2)))
    for pair in variants:
        logger.debug(f"fill cm with {pair}")
        collide_map[pair] = noop

    collide_map[(Bear  , Player)]   = hitByBear
    # collide_map[(Bear  , Sticks)]   = noop
    collide_map[(Bear  , Trap)]     = drop  # remove trap, when bear touch trap
    # collide_map[(Player, Bear)]   = noop
    # collide_map[(Player, Sticks)] = noop
    collide_map[(Player, Trap)]   = drop  # player sets traps. No damage him

    # collide_map[(Sticks, Bear)]   = noop
    # collide_map[(Sticks, Player)] = noop
    collide_map[(Sticks, Sticks)] = drop
    # collide_map[(Sticks, Trap)]   = noop
    # how trap change object, that touch it
    collide_map[(Trap  , Bear)]     = drop  #
    collide_map[(Trap  , Player)]   = damageUnitByTrap
    # collide_map[(Trap  , Sticks)]   = noop
    collide_map[(Trap  , Trap)]     = drop

    return collide_map

__COLLIDE_MAP = create_collide_map()
