# -*- coding: utf-8 -*-
from .collector import Collector
from .inventory import Inventory
from .unit import Unit
from .resource import Resource


class Player(Unit):
    """
    Player login.
    collectSpeed - how many resource player can collect in second
    """
    def __init__(self, health=100):

        Unit.__init__(self, health=health)
        self.inventory = Inventory()
        self.collector = Collector(2)

    def collect(self, resource: Resource, dt):
        collected = self.collector.collect(resource, dt)
        self.inventory.add(collected)

    def stop_collecting(self):
        self.collector.stop()
