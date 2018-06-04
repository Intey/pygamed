from domain import Notifier
from cocos.cocosnode import CocosNode


class TimerNotifier(Notifier):
    """
    Notify subscribers each 5 seconds
    Parameters
    ==========
    seconds_interval: float
        Seconds for tick. When `seconds_interval` seconds elapsed,
        `self.notify` will be called
    """

    def __init__(self, seconds_interval: float) -> None:
        Notifier.__init__(self)
        self.timer = CocosNode()
        self.notify_func = lambda dt: self.notify()
        self.timer.schedule_interval(self.notify_func, seconds_interval)
        self.timer.pause_scheduler()

    def start(self) -> None:
        self.timer.resume_scheduler()

    def stop(self) -> None:
        self.timer.pause_scheduler()

    def set_interval(self, seconds: float):
        self.timer.unschedule(self.notify_func)
        self.timer.schedule_interval(self.notify_func, seconds)
