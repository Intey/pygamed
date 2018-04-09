from actors.sticks_actor import SticksActor
from utils.random import randomPos

from .actor_factory import ActorFactory


class SticksFactory(ActorFactory):
    """Generate q`sticks"""

    def __init__(self, WIDTH, HEIGHT):
        """
        :WIDTH: width of map
        :HEIGHT: height of map
        """
        ActorFactory.__init__(self)
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT

    def _create_impl(self):
        return SticksActor(randomPos(self._WIDTH, self._HEIGHT))
