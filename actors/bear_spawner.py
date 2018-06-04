from domain import Spawner, Player
from actors import BearFactory, AreaPositioner, TimerNotifier

import typing as t

class BearSpawner(Spawner):

    """
    Creates bears in given area.
    Parameters
    ----------
    player: Player
        player actor, that bear become to follow
    area: AreaPositioner.AREA
        area, where bears will be created
    seconds_interval: float
        interval between spawns
    """

    def __init__(self, player: Player, area: AreaPositioner.AREA,
                 seconds_interval: float, subscriber: t.Callable) -> None:
        positioner = AreaPositioner(area)
        factory = BearFactory(player, positioner)
        factory.subscribe(subscriber)
        timer = TimerNotifier(seconds_interval)
        Spawner.__init__(self, factory, timer)

    def start(self) -> None:
        self.timer.start()

    def stop(self) -> None:
        self.timer.stop()
