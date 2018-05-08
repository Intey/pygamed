from .trap import Trap

class SlowTrap(Trap):
    def __init__(self, max_speed, power, range_=Trap.MIN_RANGE):
        Trap.__init__(self, power, range_=range_)
        self.max_speed = max_speed
