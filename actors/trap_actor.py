
from .actor import Actor
class TrapActor(Actor):
    def __init__(self, position, domain):
        Actor.__init__(self, 'assets/trap.png', position=position, domain=domain)
