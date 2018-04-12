from domain import Collector, Sticks, Player


def test_collector():
    p = Player()
    c = Collector()
    r = Sticks(20)
    c.collect(p, r, 1.0)
    assert r.value == 18
    assert p.inventory['sticks'] == 2

    c.collect(p, r, 2)
    assert r.value == 14
    assert p.inventory['sticks'] == 6


def test_collector_continuation():
    p = Player()
    c = Collector()
    r = Sticks(20)

    c.collect(p, r, 0.5)
    assert r.value == 20
    assert p.inventory['sticks'] is None

    c.collect(p, r, 0.5)
    assert r.value == 18
    assert p.inventory['sticks'] == 2

    c.collect(p, r, 1.5)
    assert r.value == 15
    assert p.inventory['sticks'] == 5


def test_collector_stopping():
    p = Player()
    c = Collector()
    r = Sticks(20)

    c.collect(p, r, 0.8)
    c.stop()  # player release collection key
    c.collect(p, r, 0.3)
    assert r.value == 20
    assert p.inventory['sticks'] is None