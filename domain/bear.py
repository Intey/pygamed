# -*- coding: utf-8 -*-

from domain.unit import Unit

class Bear(Unit):
    def __init__(self, power=5, **kwargs):
        Unit.__init__(self, **kwargs)
        self.power = power

