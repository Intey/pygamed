# -*- coding: utf-8 -*-


class ResourceMeta(type):
    """
    Auto generator of name, value fields.
    """
    def __call__(self, *args, **kwargs):
        """
        Metaclass for n-game resources. Whe create class wth metaclass=Resource,
        it's create `name` and `count` fields in "derived" classes.
        """
        obj = type.__call__(self)
        setattr(obj, 'name', obj.__class__.__name__.lower())
        count = args[0] if len(args) == 1 else 0
        setattr(obj, 'value', count)
        return obj


class Resource:
    """
    Manual generator of name, count fields
    """
    def __init__(self, name: str, count: int):
        self.name = name
        self.value = count
