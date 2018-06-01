from abc import ABCMeta, abstractmethod
import typing as tp


class Positioner(metaclass=ABCMeta):
    """
    Generate random position
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_position(self) -> tp.Any:
        """
        Should return position of object
        """

