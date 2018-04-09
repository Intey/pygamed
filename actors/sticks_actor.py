from random import randrange

from pyglet.resource import image as p_image

from domain import Sticks
from domain.utils import splitPartition
from init import selectKey
from .actor import Actor


class SticksActor(Actor):
    def __init__(self, position: tuple, count: int = None):
        """
        Sticks Actor in game world
        :param position: position, where placed object
        :param count: count of sticks. If None, create random in range Sticks.MIN, Sticks.MAX
        """
        if count is None:
            count = randrange(Sticks.MIN, Sticks.MAX)
        sticks = Sticks(count)
        Actor.__init__(self, 'assets/sticks.png', position=position, domain=sticks)
        self.schedule_interval(self._update_sprite, 0.05)

    # override Resource count attribute
    # @property
    # def value(self):
    #    return self._value
    #
    ## ad-hoc update sprite
    # @value.setter
    # def value(self, value):
    #    self._value = value
    #    self.update_sprite()

    def _update_sprite(self, dt: float):
        """
        Update sticks sprite by count.
        """
        # map count to sprite. Distribute 4 point between MIN-MAX
        keys = splitPartition(Sticks.MIN, Sticks.MAX, 4)
        sprite_map = {
            keys[0]: p_image('assets/sticks.png'),
            keys[1]: p_image('assets/sticks-mid.png'),
            keys[2]: p_image('assets/sticks-light.png'),
            keys[3]: p_image('assets/sticks-almost.png')
        }
        key = selectKey(self.domain.value, keys)
        self.image = sprite_map[key]
