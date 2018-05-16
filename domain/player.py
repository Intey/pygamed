# -*- coding: utf-8 -*-
from .collector import Collector
from .inventory import Inventory
from .unit import Unit
from .resource import Resource
from .builder import Builder
from .recipe import Recipe
from .slow_trap import SlowTrap
from .exceptions import InitializationException


class Player(Unit):
    """
    Player login.
    collectSpeed - how many resource player can collect in second
    """
    RECIPE_TRAP = 'trap'
    RECIPE_SLOW_TRAP = 'slowtrap'

    RECIPES = {
        RECIPE_TRAP: Recipe(lambda: Trap(10), sticks=4),
        RECIPE_SLOW_TRAP: Recipe(lambda: SlowTrap(max_speed=10, power=10), sticks=2)
    }

    def __init__(self, health=100):

        Unit.__init__(self, health=health)
        self._inventory = Inventory()
        self._inventory.add(Resource('sticks', 2))
        self._collector = Collector(speed=2)
        self._builder = Builder(self._inventory, Player.RECIPES)
        self.damage = 20
        self.shoot_distance = 100

    def collect(self, resource: Resource, dt):
        collected = self._collector.collect(resource, dt)
        self._inventory.add(collected)

    def stop_collecting(self):
        self._collector.stop()

    def create(self, recipe_name):
        return self._builder.create(recipe_name)

    def shoot(self, target):
        target.health -= self.damage
