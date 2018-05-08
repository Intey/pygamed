# -*- coding: utf-8 -*-


class Trap:
    MIN_RANGE = 1
    MAX_RANGE = 10
    def __init__(self, power=0, range_=MIN_RANGE):
        print(power, range_)
        self.power = power
        self.range_ = range_

    def range(self):
        return self.range_

    def __eq__(self, o):
        return type(self) == type(o) and self.power == o.power \
                and self._range == o._range
