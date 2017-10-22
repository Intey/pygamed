# -*- coding: utf-8 -*-


def inRange(trap, unit):
    return trap.range() <= distance(location(trap) - location(unit))
    

def activateTrap(trap, unit):
    if inRange(trap, unit):        
        unit.hit(trap.power())
        
