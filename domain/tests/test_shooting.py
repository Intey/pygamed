from domain import Player, Bear

def test_shoot():
    player = Player()
    bear = Bear()
    player.shoot(bear)
    assert bear.health == 80

