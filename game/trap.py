# -*- coding: utf-8 -*-


class Trap:
    MIN_RANGE = 1
    MAX_RANGE = 10
    def __init__(self, power, range=MIN_RANGE):
        self._power = power
        self._range = range

    def power(self):
        return self._power

    def range(self):
        return self._range
