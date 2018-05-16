from abc import abstractmethod, ABCMeta

from cocos.collision_model import CollisionManagerGrid
from cocos.actions import MoveTo
from pyglet.window import key
from pyglet.window.key import KeyStateHandler

from domain import Builder, Recipe, Trap, BuildException, Bullet
from domain import Player, Sticks
from domain.utils import Accelerator
from .actor import Actor
from .bear_actor import BearActor
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
        self.accelerator = Accelerator(100, 5, 40)
        self.last_create_delta = 0
        self.create_cooldown = 500
        self.last_shoot_dt = 0
        self.shoot_rate = 500

    def update(self, dt):
        player_actor = self
        player_logic = self.domain
        keyboard = self.key_handler
        # Buider part: if we create something before.
        last_rect = self.get_rect()
        new_rect = self._handle_movement(last_rect, dt)

        direction = normalize( (last_rect.x - new_rect.x,
                                last_rect.y - new_rect.y))

        self._handle_collecting(dt)
        self._handle_build(direction, dt)
        self._handle_shoot( dt)
        # Actor.update(self, dt)

    def _handle_shoot(self, dt):
        if self.last_shoot_dt != 0:
            self.last_shoot_dt += dt

        keyboard = self.key_handler
        if keyboard[key.SPACE]:
            if self.last_shoot_dt == 0:
                bear_actor = None
                objs = self.cm.ranked_objs_near(self, self.domain.shoot_distance)
                # reduce(lambda x, acc: [...acc, x] if isinstance(x[0], Bear) else acc, objs, [])
                for obj, distance in objs:
                    if isinstance(obj, BearActor):
                        bear_actor = obj
                        # create bullet
                        # set move action for it's. Sprite with cshape. When it's move check
                        bullet = Actor('assets/bullet.png', position=self.position, domain=Bullet())
                        self.layer.addCollidable(bullet)
                        action = MoveTo(bear_actor.position, 0.08)
                        bullet.do(action)

                        self.layer.collide_map
                        # collisions with map(trees)
                        # on collide - drop bullet
                        # on collide with bear call next
                        self.domain.shoot(bear_actor.domain)
        if self.last_shoot_dt >= self.shoot_rate:
            self.last_shoot_dt = 0

    def _handle_movement(self, last_rect, dt):
        """
        Controls user input in 'movement' aspect.
        """
        keyboard = self.key_handler
        # dx, dy = self.velocity
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

        # change new_rect to not overlap collide-map
        # dx_f, dy_f - changes of velocity?
        dx_f, dy_f = self.layer.collide_map(last_rect, new_rect, dx, dy)

        self.setPos(new_rect.center)
        return new_rect

    def _handle_build(self, direction, dt):
        keyboard = self.key_handler
        if self.last_create_delta != 0:
            self.last_create_delta += dt

        if keyboard[key.T]:
            if self.last_create_delta == 0:
                try:
                    trap_domain = self.domain.create(self.domain.RECIPE_SLOW_TRAP)
                    offset = ((TILE_WIDTH + Trap.MAX_RANGE) * direction[0],
                                (TILE_WIDTH + Trap.MAX_RANGE) * direction[1])
                    trap_pos =(self.position[0] + offset[0],
                                self.position[1] + offset[1])
                    actor = TrapActor(trap_pos, trap_domain)
                    self.layer.addCollidable(actor)
                except BuildException as e:
                    print(e)
            # Builder part: cooldown finished. Reset
            if self.last_create_delta >= self.create_cooldown:
                self.last_create_delta = 0

    def _handle_collecting(self, dt):
        keyboard = self.key_handler
        player_logic = self.domain
        if not keyboard[key.E]:
            player_logic.stop_collecting()
        else:
            for maybeSticks in self.cm.objs_colliding(self):
                if hasattr(maybeSticks, "domain") \
                        and isinstance(maybeSticks.domain, Sticks):
                    sticks = maybeSticks.domain
                    player_logic.collect(sticks, dt)
                    if sticks.value <= 0 and self.layer.__contains__(maybeSticks):
                        self.layer.remove(maybeSticks)



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

