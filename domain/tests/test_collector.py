from domain import Collector, Sticks, Player


def test_collector():
    p = Player()
    c = Collector()
    r = Sticks(20)
    c.collect(p, r, 1.0)
    assert r.value == 18
    assert p.inventory.get('sticks') == 2

    c.collect(p, r, 2)
    assert r.value == 14
    assert p.inventory.get('sticks') == 6


def test_collector_continuation():
    p = Player()
    c = Collector()
    r = Sticks(20)

    c.collect(p, r, 0.5)
    assert r.value == 20
    assert p.inventory.get('sticks') == 0

    c.collect(p, r, 0.5)
    assert r.value == 18
    assert p.inventory.get('sticks') == 2

    c.collect(p, r, 1.1)
    assert r.value == 16, "1.1 delta should collect only as 1.0"
    assert p.inventory.get('sticks') == 4

    assert c.elapsed == 0.1, "collector should save rest time if not stopped"

    c.collect(p, r, 0.9)

    assert r.value == 14, "should continue collect after over second collection"
    assert p.inventory.get('sticks') == 6


def test_collector_stopping():
    p = Player()
    c = Collector()
    r = Sticks(20)

    c.collect(p, r, 0.8)
    c.stop()  # player release collection key
    c.collect(p, r, 0.3)
    assert r.value == 20
    assert p.inventory.get('sticks') == 0


def test_collector_float():
    p = Player()
    c = Collector()
    r = Sticks(20)

    c.collect(p, r, 1.5)
    assert r.value == 18
    assert p.inventory.get('sticks') == 2
