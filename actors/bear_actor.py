from math import sqrt

from cocos.actions.move_actions import Move
import cocos.collision_model as cm

from domain import Bear
from domain.utils import Accelerator
from sprites import getBearSprite

from .actor import Actor


def followSpeed(subject:cm.CircleShape, subjectSpeed:int, target:cm.CircleShape):
    """
    Return speed(and direction implicit) as x,y, with with we should move for
    follow target.
    """
    distance = subject.distance(target)
    if distance < 550 and distance > 5:

        # x = target.x - subj.x. then we devide this on dir_size(normalization)
        # and next use gotten vector as direction - multipy on subjectSpeed.
        # (x/dir_size)*subjectSpeed == (x*subjectSpeed) / dir_size
        x = target.center.x - subject.center.x
        y = target.center.y - subject.center.y
        dir_size = sqrt(x**2 + y**2)
        return x/dir_size * subjectSpeed, y/dir_size * subjectSpeed
    else:  # near player
        return 0, 0


class BearActor(Actor):
    def __init__(self, player, position=(0,0)):
        Actor.__init__(self, getBearSprite(), position=position, domain=Bear(health=50))
        # scaling changes self.get_rect()
        self.player = player
        self.schedule(self.update)
        self.accel = Accelerator(80, 5, 5)

    def update(self, dt):
        target = self.player
        if self.cshape.distance(target.cshape) <= 5:
            self.accel.reset()
        else:
            self.accel.accelerate()

        dx, dy = followSpeed(self.cshape, self.accel.speed, target.cshape)

        last_rect = self.get_rect()
        new_rect = last_rect.copy()
        dx *= dt
        dy *= dt
        new_rect.x += dx
        new_rect.y += dy
        _, _ = self.layer.collide_map(last_rect, new_rect, dx, dy)

        self.setPos(new_rect.center)  # update domain logic position

