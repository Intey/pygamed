from domain import Collector, Sticks, Player


def test_collector():
    p = Player()
    c = Collector(2)
    r = Sticks(20)
    collected = c.collect(r, 1.0)
    assert r.value == 18
    assert collected.value == 2

    collected = c.collect(r, 2)
    assert r.value == 14
    assert collected.value == 4


def test_collector_continuation():
    p = Player()
    c = Collector(2)
    r = Sticks(20)

    collected = c.collect(r, 0.5)
    assert r.value == 20
    assert collected.value == 0

    collected = c.collect(r, 0.5)
    assert r.value == 18
    assert collected.value == 2

    collected = c.collect(r, 1.1)
    assert r.value == 16, "1.1 delta should collect only as 1.0"
    assert collected.value == 2

    assert c.elapsed == 0.1, "collector should save rest time if not stopped"

    collected = c.collect(r, 0.9)
    assert r.value == 14, "should continue collect after over second collection"
    assert collected.value == 2


def test_collector_stopping():
    p = Player()
    c = Collector(2)
    r = Sticks(20)

    n1 = c.collect(r, 0.8)
    c.stop()  # player release collection key
    n2 = c.collect(r, 0.3)
    assert r.value == 20
    assert n1.value == 0
    assert n2.value == 0


def test_collector_float():
    p = Player()
    c = Collector(2)
    r = Sticks(20)

    res = c.collect(r, 1.5)
    assert r.value == 18
    assert res.name == r.name
    assert res.value == 2
