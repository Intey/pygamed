from time import time

from domain.player import Player
from domain.resource import Resource


class Collector:
  def __init__(self):
    self.running = False
    self.startTime = None

  def start(self):
    self.startTime = time()
    print("start", self.startTime)
    self.running = True

  def stop(self):
    self.running = False
    self.startTime = None

  def collect(self, player: Player, resource: Resource):
    """
    Collect resource in player inventory. Collecting use time() and player info
    about speed, and count. Should be called in update every time to check
    elapsed time
    """
    if not self.running:
      self.start()
    elapsed = abs(self.startTime - time())
    if elapsed >= player.collectSpeed:
      print("collect. elaps", elapsed)
      self.startTime = time()
      self.__direct_collect(player, resource)

  def __direct_collect(self, player, resource):
    collectSpeed = player.collectCount
    collected = collectSpeed
    if resource.value < collectSpeed:
        collected = resource.value
        resource.value = 0
    else:
        resource.value -= collectSpeed

    if player.inventory.get(resource.name):
      player.inventory[resource.name] += collected
    else:
      player.inventory[resource.name] = collected

    print("collected {} of {}. rest {}".format(player.inventory[resource.name],
                                               resource.name, resource.value))
