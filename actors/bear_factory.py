from .bear_actor import BearActor

from domain import Factory

from logging import getLogger

logger = getLogger(__name__)


class BearFactory(Factory):
    """
    Creates bear at random position in area from 0,0 to `WIDTH`,`HEIGHT`.
    """
    def __init__(self, player) -> None:
        Factory.__init__(self, logger)
        self.player = player

    def _create_impl(self):
        pos = self.positioner.get_position()
        return BearActor(self.player, pos)
