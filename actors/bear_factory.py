from .bear_actor import BearActor
from .actor_factory import ActorFactory

from utils.random import randomPos
from logging import getLogger

logger = getLogger(__name__)


class BearFactory(ActorFactory):
    def __init__(self, WIDTH, HEIGHT, player):
        ActorFactory.__init__(self)
        self.width = WIDTH
        self.height = HEIGHT
        self.player = player

    def _create_impl(self):
        logger.debug("create bear")
        pos = randomPos(self.width, self.height)
        return BearActor(self.player, pos)
