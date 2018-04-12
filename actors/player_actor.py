from cocos.collision_model import CollisionManagerGrid
from cocos.layer import ScrollableLayer
from pyglet.window import key
from pyglet.window.key import KeyStateHandler

from domain import Collector
from domain import Player, Sticks
from domain.utils import Accelerator
from .actor import Actor


class PlayerActor(Actor):

    def __init__(self, collide_manager: CollisionManagerGrid,
                 keyboard_handler: KeyStateHandler):
        """
        Create player actor
        :param collide_manager: collide manager, that can answer is player collide some objects.
         Used for collecting  sticks
        :param keyboard_handler: provide information about pressed keys. Used for collecting sticks
        """
        Actor.__init__(self, 'assets/user.png', position=(20, 20), domain=Player())
        self.cm = collide_manager
        self.key_handler = keyboard_handler
        self.schedule(self.update)
        self.collector = Collector()
        self.accelerator = Accelerator(150, 5, 40)
        self.layer = None

    def set_layer(self, layer: ScrollableLayer):
        self.layer = layer

    def update(self, dt):
        player_actor = self
        player_logic = self.domain
        keyboard = self.key_handler
        if not keyboard[key.E]:
            self.collector.stop()
        else:
            for maybeSticks in self.cm.objs_colliding(player_actor):
                if hasattr(maybeSticks, "domain") \
                        and isinstance(maybeSticks.domain, Sticks):
                    sticks = maybeSticks.domain
                    self.collector.collect(player_logic, sticks, dt)
                    if sticks.value <= 0 and self.layer.__contains__(maybeSticks):
                        self.layer.remove(maybeSticks)
                    # injected in generateSticks. update sprite image
        lastRect = self.get_rect()
        self.movementHandling(lastRect, dt)

    def movementHandling(self, lastRect, dt):
        """
        Controls user input in 'movement' aspect.
        """
        keyboard = self.key_handler
        dx, dy = self.velocity
        if keyboard[key.UP] + keyboard[key.DOWN] + keyboard[key.LEFT] + \
                keyboard[key.RIGHT] > 0:
            self.accelerator.accelerate()
        else:
            self.accelerator.reset()
        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) \
             * self.accelerator.speed * dt
        dy = (keyboard[key.UP] - keyboard[key.DOWN]) \
             * self.accelerator.speed * dt

        newRect = lastRect.copy()
        newRect.x += dx
        newRect.y += dy

        self.setPos(newRect.center)
