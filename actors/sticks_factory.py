from actors.sticks_actor import SticksActor
from utils.random import randomPos

from domain import Factory

from logging import getLogger
logger = getLogger(__name__)

class SticksFactory(Factory):
    """Generate q`sticks"""

    def __init__(self, WIDTH, HEIGHT):
        """
        :WIDTH: width of map
        :HEIGHT: height of map
        """
        Factory.__init__(self, logger)
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT

    def _create_impl(self):
        return SticksActor(randomPos(self._WIDTH, self._HEIGHT))
