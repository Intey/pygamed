class Builder:
    """ Responsibility:
    - create instance of craft object
    - controller between Inventory, Recipe and Player
    """
    def __init__(self, **recipies):
        """ define which reciepes can be build with this builder """
        self.recipies = recipies

    def set_inventory(self, inventory):
        self.inventory = inventory

    def build(self, recipe_name):
        """ craft
        """
        recipe = self.recipies.get(recipe_name)
        if recipe is None:
            print("can't craete %s" % recipe_name)
            return
        if self.inventory.subtract(recipe.ingridients):
            results = []
            for i in range(recipe.product_count):
                results.append(recipe.Product())
                
            
            # check that all ingridients available 
            # if so, subtract resources, and create item






