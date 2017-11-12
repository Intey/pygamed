# -*- coding: utf-8 -*-

def collectResource(player, resource):
    collectSpeed = player.collectSpeed
    resource.value -= collectSpeed
    player.inventory[resource.name] = collectSpeed
