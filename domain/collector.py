from math import ceil, floor
from time import time

from domain.player import Player
from domain.resource import Resource


class Collector:
    """
    Provide logic for collecting resources for player. Use internal timer with incoming dt
    """

    def __init__(self):
        self.running = False
        self.elapsed = 0

    def start(self):
        self.running = True
        self.elapsed = 0

    def stop(self):
        self.running = False
        self.elapsed = 0

    def collect(self, player: Player, resource: Resource, dt=0.1):
        """
        Collect resource in player inventory. Collecting use dt as collection speed and player
        about speed, and count. Should be called in update every time
        """
        if not self.running:
            self.start()

        self.elapsed += dt

        if self.elapsed >= 1.0:
            collect_count = player.collectSpeed * floor(self.elapsed)
            collected = 0
            if resource.value < collect_count:
                collected = resource.value
                resource.value = 0
            else:
                collected = collect_count
                resource.value -= collect_count

            player.inventory.add(Resource(resource.name, collected))
            self.elapsed = round(self.elapsed % 1, 1)
