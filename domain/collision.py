# -*- coding: utf-8 -*-

"""
Collide resposibility is return actions, that
"""

from domain.player import Player
from domain.trap import Trap
from domain.bear import Bear
from domain.sticks import Sticks
from domain.unit import Unit
from collections import defaultdict
from domain.noop import noop

from logging import getLogger

logger = getLogger(__name__)

def collide(left:Unit, right:Unit, distance:int):
    """
    Collide wrapper. Call realCollider function by objects types.
    make collision action. Decrease health, buff, stun, decrease speed on time,
    etc.
    """

    logger.debug(f"collide: mapping: {__COLLIDE_MAP}")
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

__COLLIDE_MAP = defaultdict(noop)
__COLLIDE_MAP[(Bear  , Player)]   = noop
__COLLIDE_MAP[(Bear  , Sticks)]   = noop
__COLLIDE_MAP[(Bear  , Trap)]     = drop  # player sets traps. No damage him
__COLLIDE_MAP[(Player, Bear)]   = noop
__COLLIDE_MAP[(Player, Sticks)] = noop
__COLLIDE_MAP[(Player, Trap)]   = drop  # player sets traps. No damage him
__COLLIDE_MAP[(Sticks, Bear)]   = noop
__COLLIDE_MAP[(Sticks, Player)] = noop
__COLLIDE_MAP[(Sticks, Sticks)] = drop
__COLLIDE_MAP[(Sticks, Trap)]   = noop
__COLLIDE_MAP[(Trap  , Bear)]     = drop  # player sets traps. No damage him
__COLLIDE_MAP[(Trap  , Player)]   = damageUnitByTrap
__COLLIDE_MAP[(Trap  , Sticks)]   = noop
__COLLIDE_MAP[(Trap  , Trap)]     = drop
