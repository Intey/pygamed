from abc import ABCMeta, abstractmethod
from .positioner import Positioner

import typing as t

class Event:
    """
    Factory event
    """
    CREATE_TYPE = 'create'

    def __init__(self, type_, payload=None):
        self.type = type_
        self.payload = payload

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({"type": self.type, "payload": self.payload})


class Factory(metaclass=ABCMeta):
    """
    Docstring for Factory.
    """
    def __init__(self, logger, positioner: Positioner) -> None:
        self.subscribers:t.List[t.Callable] = []
        self.logger = logger
        self.positioner = positioner

    def subscribe(self, subscriber):
        """
        Add subscriber on creation `Event`s
        """
        self.subscribers.append(subscriber)

    def _notify(self, object_):
        self.logger.debug("start notify")
        for s in self.subscribers:
            event = Event(Event.CREATE_TYPE, object_)
            self.logger.debug(f"notify {s} about {event}")
            s(event)

    @abstractmethod
    def _create_impl(self):
        """
        Should create new object and return it. Used only for creating object
        in internal workflow
        """

    def create(self):
        """
        Creates element with _create_impl realization
        """
        o = self._create_impl()
        self.logger.debug(f"created {o}")
        self._notify(o)

    def set_positioner(self, positioner) -> None:
        self.positioner = positioner

