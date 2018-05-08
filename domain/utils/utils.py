# -*- coding: utf-8 -*-
from math import ceil


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
