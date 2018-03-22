from domain.collision import collide
from domain.player import Player
from domain.trap import Trap
from domain.bear import Bear


def test_collision():
    p = Player()
    tr = Trap(5, range=10)
    player_stay, trap_stay = collide(p, tr, 8)
    assert p.health == 95
    assert player_stay and not trap_stay

    trap_stay, player_stay = collide(tr, p, 8)
    assert p.health == 90
    assert player_stay and not trap_stay

def test_bear_cathed_by_trap():
    b = Bear()
    tr = Trap(5, range=10)

    bear_stay, trap_stay = collide(b, tr, 8)
