from .actor import Actor
from domain import Trap
from random import randrange
from utils.random import randomPos

from .actor_factory import ActorFactory


class TrapFactory(ActorFactory):
    """Generages traps"""
    def __init__(self, WIDTH, HEIGHT):
        """
        :WIDTH: width of map
        :HEIGTH: height of map
        """
        ActorFactory.__init__(self)
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT

    def _create_impl(self):
        return Actor('assets/trap.png',
                     position=randomPos(self._WIDTH, self._HEIGHT),
                     domain=Trap(randrange(1, 30),
                                 randrange(Trap.MIN_RANGE, Trap.MAX_RANGE)))
