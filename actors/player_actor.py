from abc import abstractmethod, ABCMeta

from cocos.collision_model import CollisionManagerGrid
from cocos.layer import ScrollableLayer
from pyglet.window import key
from pyglet.window.key import KeyStateHandler

from domain import Builder, Recipe, Trap, BuildException
from domain import Player, Sticks
from domain.utils import Accelerator
from .actor import Actor
from .trap_actor import TrapActor

TILE_WIDTH = 25  # FIXME: export to consts


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
        self.accelerator = Accelerator(150, 5, 40)
        self.layer = None
        self.builder = Builder(self.domain.inventory, {"trap": Recipe(lambda: Trap(10), sticks=4)})
        self.last_create_delta = 0
        self.create_cooldown = 0.5

    def set_layer(self, layer: ScrollableLayer):
        self.layer = layer

    def update(self, dt):
        player_actor = self
        player_logic = self.domain
        keyboard = self.key_handler
        # Buider part: if we create something before.
        if self.last_create_delta != 0:
            self.last_create_delta += dt

        last_rect = self.get_rect()
        new_rect = self._movement_handling(last_rect, dt)

        def normalize(vec):
            # default - up direction
            res = [0,1]
            if vec[0] == 0 and vec[1] == 0:
                return tuple(res)

            if vec[0]   < 0: res[0] = -1
            elif vec[0] > 0: res[0] = 1
            else:            res[0] = 0

            if vec[1]   < 0: res[1] = -1
            elif vec[1] > 0: res[1] = 1
            else:            res[1] = 0

            return tuple(res)

            return 1 if x >= 0 else -1

        direction = normalize( (last_rect.x - new_rect.x,
                                last_rect.y - new_rect.y))

        if not keyboard[key.E]:
            player_logic.stop_collecting()
        else:
            for maybeSticks in self.cm.objs_colliding(player_actor):
                if hasattr(maybeSticks, "domain") \
                        and isinstance(maybeSticks.domain, Sticks):
                    sticks = maybeSticks.domain
                    player_logic.collect(sticks, dt)
                    if sticks.value <= 0 and self.layer.__contains__(maybeSticks):
                        self.layer.remove(maybeSticks)
                    # injected in generateSticks. update sprite image

        if keyboard[key.T]:
            # Builder part: cooldowned?
            if self.last_create_delta == 0:
                try:
                    trap_domain = self.builder.create('trap')
                    offset = ((TILE_WIDTH + Trap.MAX_RANGE) * direction[0],
                              (TILE_WIDTH + Trap.MAX_RANGE) * direction[1])
                    trap_pos =(self.position[0] + offset[0],
                               self.position[1] + offset[1])
                    actor = TrapActor(trap_pos, trap_domain)
                    self.layer.addCollidable(actor)
                    # yeah, we had create something
                    self.last_create_delta = .01
                except BuildException as e:
                    print(e)

        # Builder part: cooldown finished. Reset
        if self.last_create_delta >= self.create_cooldown:
            self.last_create_delta = 0

    def _start_create_trap(self):
        pass

    def _movement_handling(self, last_rect, dt):
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

        new_rect = last_rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        self.setPos(new_rect.center)
        return new_rect
