from domain.builder import Builder
from domain.inventory import Inventory
from domain.recipe import Recipe
from domain.rope import Rope
from domain.sticks import Sticks
from domain.trap import Trap


def test_subtracting():
    inventory = Inventory()
    sticks = Sticks(3)
    inventory.add(sticks)
    assert inventory.subtract({'sticks': 2}) and inventory.get('sticks') == 1, \
        "should subtract if exists"

    assert inventory.subtract({"sticks": 1}) and inventory.get('sticks') == 0, \
        "should subtract last item"

    inventory.add(Sticks(1))

    assert not inventory.subtract({'sticks': 4}) and inventory.get('sticks') == 1, \
        "Should not subtract more than exists item"

    assert not inventory.subtract({'rope': 3}) and inventory.get('sticks') == 1, \
        "should no subtract unexist item"

    inventory.add(Sticks(1), Rope(1))  # s: 2, r: 1

    assert inventory.subtract({"sticks": 1, "rope": 1}) \
           and inventory.get('sticks') == 1 and inventory.get('rope') == 0, \
        "should subtract, if all counts exists"

    assert not inventory.subtract({"sticks": 1, "rope": 1}) \
           and inventory.get('sticks') == 1, \
        "should not subtract, if not all counts exists"


def test_craft_trap():
    inventory = Inventory()
    sticks = Sticks(10)
    rope = Rope(3)

    inventory.add(sticks)
    inventory.add(rope)

    factory = lambda: Trap(10)
    justTrap = Recipe(factory, sticks=4, rope=1)

    builder = Builder(inventory, {'justTrap': justTrap})
    trap = builder.create('justTrap')
    expect = factory()
    assert trap == expect, "Expect build one trap"
    assert inventory.get('sticks') == 6,"By recipe, 4 Sticks should be subtracted"
    assert inventory.get('rope') == 2, "By recipe, 1 Rope should be subtracted"
