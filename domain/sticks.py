# -*- coding: utf-8 -*-

from .resource import ResourceMeta, Resource


class Sticks(Resource):
    MAX = 10
    MIN = 1

    def __init__(self, count: int):
        """
        Create Sticks object with given count
        :param count: count if sticks
        """
        Resource.__init__(self, self.__class__.__name__, count)
