from abc import ABCMeta, abstractmethod

from logging import getLogger

logger = getLogger(__name__)

class Event:
    CREATE_TYPE = 'create'

    def __init__(self, type_, payload=None):
        self.type = type_
        self.payload = payload

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({"type": self.type, "payload": self.payload})


class ActorFactory(metaclass=ABCMeta):
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def _notify(self, object_):
        logger.debug("start notify")
        for s in self.subscribers:
            event = Event(Event.CREATE_TYPE, object_)
            logger.debug(f"notify {s} about {event}")
            s(event)

    @abstractmethod
    def _create_impl(self):
        """
        Should create new object and return it. Used only for creating object
        in internal workflow
        """

    def create(self):
        o = self._create_impl()
        logger.debug(f"created {o}")
        self._notify(o)
