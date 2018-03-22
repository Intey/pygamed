# -*- coding: utf-8 -*-
from domain.resource import Resource


class Test(metaclass=Resource):
    pass


def test_meta():
    r = Test(15)
    assert r.name == 'test'
    assert r.value == 15
