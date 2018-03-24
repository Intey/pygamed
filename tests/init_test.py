from init import selectKey


def test_selectKey():
    keys = [10, 7, 4, 1]
    assert 4 == selectKey(5, keys)
    assert 1 == selectKey(1, keys)
    assert 1 == selectKey(2, keys)
    assert 1 == selectKey(0, keys)


