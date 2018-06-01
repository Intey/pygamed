from .actor import Actor
from domain import Trap, Factory
from random import randrange
from utils.random import randomPos

from logging import getLogger

logger = getLogger(__name__)

class TrapFactory(Factory):
    """Generages traps"""
    def __init__(self, WIDTH, HEIGHT):
        """
        :WIDTH: width of map
        :HEIGTH: height of map
        """
        Factory.__init__(self, logger)
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT

    def _create_impl(self):
        return Actor('assets/trap.png',
                     position=randomPos(self._WIDTH, self._HEIGHT),
                     domain=Trap(randrange(1, 30),
                                 randrange(Trap.MIN_RANGE, Trap.MAX_RANGE)))
