class Inventory:
    """ Responsibility:
    - Limit weight
    - Limit items count
    - Contains items, that unit carry
    - Manage resources, stored in it
    """
    def __init__(self):
        self.items = {}

    def subtract(self, **resources):
        """ subtract resources from inventory. Used for building, crafting.
        Return true, if all resources available and subtracted. Otherwice - 
        false"""
        return False

    def add(self, resource):
        pass
