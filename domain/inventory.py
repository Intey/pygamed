class Inventory:
    """ Responsibility:
    - Limit weight
    - Limit items count
    - Contains items, that unit carry
    - Manage resources, stored in it
    """
    def __init__(self):
        self.items = {}

    def subtract(self, resources):
        """ subtract resources from inventory. Used for building, crafting.
        Return true, if all resources available and subtracted. Otherwice - 
        false"""
        for k, v in resources.items():
            # check that all resources exists
            all_found = True
            if self.items.get(k):
                count = self.items[k] - v
                if count < 0:
                    return False
                # it's okey.
                self.items[k] = count

            return True


        return False

    def add(self, resource):
        pass
