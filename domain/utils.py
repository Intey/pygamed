# -*- coding: utf-8 -*-
from math import ceil

def collectResource(player, resource):
    collectSpeed = player.collectCount
    resource.value -= collectSpeed
    if player.inventory.get(resource.name):
        player.inventory[resource.name] += collectSpeed
    else:
        player.inventory[resource.name] = collectSpeed
    print("collected {} of {}. rest {}".format(player.inventory[resource.name], resource.name, resource.value))


def splitPartition(minV:int, maxV:int, parts:int) -> list:
    """
    Generate distibution of @parts count integers, that lie in range(@minV,
    @maxV).
    Returned list has as first element @maxV, and as last @minV. values
    between distributed evenly.
    """
    p = ceil(maxV / parts)
    res = []
    res.append(maxV)
    for i in range(1, maxV//p):
        v = maxV - p * i
        res.append(v)
    if res[-1] != minV:
        res.append(minV)
    return res
