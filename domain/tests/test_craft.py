from domain import Inventory
from domain import Recipe
from domain import Builder

from domain import Resource
from domain import Sticks


def createTrapFactory(power):
    def trapFactory():
        return Trap(power)
    return trapFactory


def test_craft_trap():
    inventory = Inventory()
    sticks = Sticks(10)
    rope = Rope(3)
    inventory.add(sticks)
    inventory.add(rope)
    recipe = Recipe(createTrapFactory(10), sticks=4, rope=1)
