
import typing as t
from domain import Positioner
from random import randint


class AreaPositioner(Positioner):
    """
    Generate position in given area
    """

    AREA = t.Tuple[t.Tuple[int, int], t.Tuple[int, int]]

    def __init__(self, area: AREA) -> None:
        Positioner.__init__(self)
        self.area = area

    def get_position(self) -> t.Tuple[int, int]:
        x = randint(*self.area[0])
        y = randint(*self.area[1])
        return x, y
