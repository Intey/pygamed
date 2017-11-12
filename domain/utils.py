# -*- coding: utf-8 -*-

def collectResource(player, resource):
    collectSpeed = player.collectCount
    resource.value -= collectSpeed
    if player.inventory.get(resource.name):
        player.inventory[resource.name] += collectSpeed
    else:
        player.inventory[resource.name] = collectSpeed
    print("collected {} of {}. rest {}".format(player.inventory[resource.name], resource.name, resource.value))
