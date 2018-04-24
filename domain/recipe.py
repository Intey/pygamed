class Recipe:
    """
    Responsibility:
    - define build process params(ingridients, time, product count, etc.)
    - declare dependencies and how to build recipe target.
    """
    def __init__(self, prod_factory, result_count=1, **ingredients):
        self.factory = prod_factory
        self.product_count = result_count
        assert len(ingredients) > 0, "can't build without ingridients"

        self.ingridients = ingredients
