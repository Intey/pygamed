# -*- coding: utf-8 -*-


class Resource(type):
    def __call__(self, *args, **kwargs):
        """ Вызов класса создает новый объект. """
        obj = type.__call__(self)
        setattr(obj, 'name', obj.__class__.__name__.lower())
        count = args[0] if len(args) == 1 else 0
        setattr(obj, 'value', count)
        return obj
