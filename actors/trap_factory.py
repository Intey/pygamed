from .actor import Actor
from .map_positioner import MapPositioner
from domain import Trap, Factory
from random import randrange
from utils.random import randomPos

from logging import getLogger

logger = getLogger(__name__)

class TrapFactory(Factory):
    """
    Generages traps

    Parameters
    ----------
    WIDTH: int
        width of map
    HEIGTH: int
        height of map
    """
    def __init__(self, WIDTH: int, HEIGHT: int) -> None:
        Factory.__init__(self, logger, MapPositioner(WIDTH, HEIGHT))

    def _create_impl(self):
        domain = Trap(randrange(1, 30), randrange(Trap.MIN_RANGE, Trap.MAX_RANGE))
        position = self.positioner.get_position()
        return Actor('assets/trap.png', position=position, domain=domain)
