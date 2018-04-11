class Inventory:
    """ Responsibility:
    - Limit weight
    - Limit items count
    - Contains items, that unit carry
    - Manage resources, stored in it
    """
    def __init__(self):
        self.items = {}

    def __getitem__(self, key):
        return self.items.get(key, None)

    def add(self, *resources):
        for resource in resources:
            name = resource.name.lower()
            if self.items.get(name):
                self.items[name] += resource.value
            else:
                self.items[name] = resource.value

    def subtract(self, resources):
        """ subtract resources from inventory. Used for building, crafting.
        Return true, if all resources available and subtracted. Otherwice - 
        false"""
        for k, v in resources.items():
            # check that all resources exists
            count = self.items.get(k, 0) 
            if count < v:
                return False

        for k, v in resources.items():
            count = self.items[k] - v
            # it's okey.
            self.items[k] = count

        return True
