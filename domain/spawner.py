from domain import Factory, Notifier


class Spawner:
    """
    Spawn logic. Spawns objects with given factory on given timing
    Parameters
    ----------
    factory: Factory
        factory, that builds objects
    timing: Notifier
        timer, that call `spawn` on tick
    """

    def __init__(self, factory: Factory, timer: Notifier) -> None:
        self.timer = timer
        self._factory = factory
        self.timer.subscribe(self._spawn)

    def _spawn(self):
        """
        Creates object from `self._factory` on `self._timer` tick and place it
        in `self._area`
        """
        return self._factory.create()
