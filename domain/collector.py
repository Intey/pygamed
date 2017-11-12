from time import time


class Collector:
    def __init__(self):
        self.running = False
        self.startTime = None

    def start(self):
        self.startTime = time()
        self.running = True
        pass

    def stop(self):
        pass

    def collectResource(player, resource):
        collectSpeed = player.collectCount
        resource.value -= collectSpeed
        if player.inventory.get(resource.name):
            player.inventory[resource.name] += collectSpeed
        else:
            player.inventory[resource.name] = collectSpeed
        print("collected {} of {}. rest {}".format(player.inventory[resource.name], resource.name, resource.value))
