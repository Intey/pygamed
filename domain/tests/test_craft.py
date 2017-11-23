from domain import Inventory
from domain import Recipe
from domain import Builder

from domain import Resource
from domain import Sticks
from domain import Rope


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


    justTrap = Recipe(createTrapFactory(10), sticks=4, rope=1)

    builder = Builder(inventory, {'justTrap': justTrap})
    result = builder.build('justTrap')
    assert result == [justTrap], "Expect build one trap"
