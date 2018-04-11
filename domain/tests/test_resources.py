# -*- coding: utf-8 -*-
from domain.resource import ResourceMeta


class Test(metaclass=ResourceMeta):
    pass


def test_meta():
    r = Test(15)
    assert r.name == 'test'
    assert r.value == 15
