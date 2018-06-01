from domain import Positioner

from utils.random import randomPos

import typing as t

class MapPositioner(Positioner):
    """
    Positioner with all map coverage
    """
    def __init__(self, width: int, height: int) -> None:
        Positioner.__init__(self)
        self.width = width
        self.height = height

    def get_position(self) -> t.Tuple[int, int]:
        return randomPos(self.width, self.height)


