from actors.sticks_actor import SticksActor

from domain import Factory
from .map_positioner import MapPositioner

from logging import getLogger
logger = getLogger(__name__)


class SticksFactory(Factory):
    """Generate q`sticks"""

    def __init__(self, WIDTH, HEIGHT) -> None:
        """
        :WIDTH: width of map
        :HEIGHT: height of map
        """
        positioner = MapPositioner(WIDTH, HEIGHT)
        Factory.__init__(self, logger, positioner)

    def _create_impl(self):
        return SticksActor(self.positioner.get_position())
