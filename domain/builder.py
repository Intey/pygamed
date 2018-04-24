

class Builder:
    """ Responsibility:
    - create instance of craft object
    - controller between Inventory, Recipe and Player
    """

    def __init__(self, inventory, recipes):
        """ define which reciepes can be build with this builder """
        self.recipes = recipes
        self.inventory = inventory
        self.elapsed = 0
        self.running = False
        self.speed = 1.0

    def create(self, recipe_name: str):
        """
        Creates object for recipe_name. Can raise Exception if no recipe or no resources
        :param recipe_name: name of recipe, that was builded
        :return: BuildProto object
        """
        recipe = self.recipes.get(recipe_name)
        if recipe is None:
            return Exception(f"No recipe for {recipe_name}")
        if not self.inventory.subtract(recipe.ingridients):
            raise Exception(f"No resources for recipe {recipe}")
        return recipe.factory()
