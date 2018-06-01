from .bear_actor import BearActor

from domain import Factory, Positioner, Player

from logging import getLogger

logger = getLogger(__name__)


class BearFactory(Factory):
    """
    Creates bear at random position in area from `MapPositioner`
    """
    def __init__(self, player: Player, positioner: Positioner) -> None:
        Factory.__init__(self, logger, positioner)
        self.player = player

    def _create_impl(self):
        pos = self.positioner.get_position()
        return BearActor(self.player, pos)
