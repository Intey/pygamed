import typing as tp
class Notifier:
    """
    Notify subscribers when you say
    """

    def __init__(self) -> None:
        self.subscribers:list = []

    def notify(self) -> None:
        """
        Walk through subscribers and call each
        """
        for s in self.subscribers:
            s()

    def subscribe(self, action: tp.Callable) -> int:
        """
        Call `action`
        Parameters
        ----------
        action: Callable
            function, that was called, on interval tick
        Returns
        -------
        index of added subscriber
        """
        idx = len(self.subscribers)
        self.subscribers.append(action)
        return idx
