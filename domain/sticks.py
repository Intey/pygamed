# -*- coding: utf-8 -*-
from .resource import Resource


class Sticks(Resource):
    def __init__(self, value):
        Resource.__init__(self, __class__.__name__, value)
