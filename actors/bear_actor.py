from math import sqrt

from cocos.actions.move_actions import Move
import cocos.collision_model as cm

from domain import Bear
from domain.utils import Accelerator
from sprites import getBearSprite

from .actor import Actor

class BearActor(Actor):

    def followSpeed(self, subject:cm.CircleShape, subjectSpeed:int, target:cm.CircleShape):
        """
        Return speed(and direction implicit) as x,y, with with we should move for
        follow target.
        """
        distance = subject.distance(target)
        if distance < 550 and distance > 15:

            x = target.center.x - subject.center.x
            y = target.center.y - subject.center.y
            dir_size = sqrt(x**2 + y**2)
            vel = x/dir_size, y/dir_size
            return vel[0] * subjectSpeed, vel[1] * subjectSpeed
        else:  # distance <= 15:
            return 0, 0


    def __init__(self, player, position=(0,0)):
        Actor.__init__(self, getBearSprite(), position=position, domain=Bear(health=50))
        self.scale = 2
        self.player = player
        self.schedule_interval(self.update, .10)
        self.move = Move()
        # self.velocity = (0,0)
        self.do(self.move)
        self.accel = Accelerator(100, 5, 15)

    def update(self, dt):
        self.goTo(self.player)

    def goTo(self, target:Actor):
        self.accel.accelerate()
        self.velocity = self.followSpeed(self.cshape, self.accel.speed, target.cshape)
        self.setPos(self.position)


