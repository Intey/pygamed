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
    Place resource in player inventory. Collecting use time() and player info
    about speed, and count. Should be called in update every time to check
    elapsed time
    """
    if not self.running:
      self.start()
    elapsed = abs(self.startTime - time()) 
    print("collect. elaps", elapsed)
    if elapsed >= player.collectSpeed:
      print("Here it is:")
      self.startTime = time()
      self.__direct_collect(player, resource)

  def __direct_collect(self, player, resource):
    collectSpeed = player.collectCount
    resource.value -= collectSpeed
    if player.inventory.get(resource.name):
      player.inventory[resource.name] += collectSpeed
    else:
      player.inventory[resource.name] = collectSpeed

    print("collected {} of {}. rest {}".format(player.inventory[resource.name],
                                               resource.name, resource.value))
