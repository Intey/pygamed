# Imports as usual

import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.tiles import load
from cocos.actions.move_actions import Move
from pyglet.window import key

from domain.player import Player
from domain.trap import Trap
from domain.bear import Bear
from domain.sticks import Sticks
from domain.collector import Collector
from sprites import getBearSprite
from init import generateSticks, generateTraps
from actor import Actor
#FIXME: WTF import
from init import updateSticksCountSprite

from gui.hud import HUD


from time import time
from math import sqrt
import logging

# does not affect any
TILE_WIDTH = 15

def followSpeed(subject:cm.CircleShape, subjectSpeed:int, target:cm.CircleShape):
    """
    Return speed(and direction implicit) as x,y, with with se should move for
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


class Accelerator:
    """Control speed function"""

    def __init__(self, maxAccel, initAccel, stepAccel):
        self.maxAccel = maxAccel
        self.minAccel = initAccel
        self.speed = initAccel
        self.stepAccel = stepAccel

    def accelerate(self):
        """
        Increment speed
        """
        if self.speed < self.maxAccel:
            self.speed += self.stepAccel
        if self.speed > self.maxAccel:
            self.speed = self.maxAccel

    def reset(self):
        """
        reset speed
        """
        self.speed = self.minAccel


class ActorsLayer(ScrollableLayer):
    def __init__(self, playerObject, width, height, collideMap=None):
        ScrollableLayer.__init__(self)

        self.height = height
        self.width = width
        self.player = playerObject
        self.accelerator = Accelerator(150, 5, 40)

        # collision with map (static objects)
        self.mapCollider = RectMapCollider()
        self.mapCollider.on_bump_handler = self.mapCollider.on_bump_slide
        self.collideMap = collideMap

        # dynamic objects collision. used in
        self.cm = cm.CollisionManagerGrid(0.0, self.width, 0.0, self.height,
                                          TILE_WIDTH, TILE_WIDTH)

        self.collectingSticks = False
        self.collectingStartTime = None
        # call update
        self.collector = Collector()
        self.schedule(self.update)

    def movementHandling(self, lastRect, dt):
        """
        Controls user input in 'movement' aspect.
        """
        dx = self.player.velocity[0]
        dy = self.player.velocity[1]

        if keyboard[key.UP] + keyboard[key.DOWN] + keyboard[key.LEFT] + \
                keyboard[key.RIGHT] > 0:
            self.accelerator.accelerate()
        else:
            self.accelerator.reset()

        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT])\
                * self.accelerator.speed * dt
        dy = (keyboard[key.UP] - keyboard[key.DOWN])\
                * self.accelerator.speed * dt

        newRect = lastRect.copy()
        newRect.x += dx
        newRect.y += dy

        self.player.setPos(newRect.center)

        return (newRect, dx, dy)

    def collideMapHandling(self, lastRect, newRect, dx, dy):
        """
        Handling collisions with static objects(trees, rocks, etc.)
        """
        if self.collideMap:
            collider = self.mapCollider
            self.player.velocity = collider.collide_map(self.collideMap,
                                                        lastRect,
                                                        newRect,
                                                        dx, dy)

    def collisionHandling(self, lastRect, newRect):
        """
        Handle collision of player/BearActor with traps
        """
        # handling collisions with dynamic objects
        from domain.collision import collide
        for left, right in self.cm.iter_all_collisions():
            leftStay, rightStay = collide(left.domain, right.domain, left.cshape.distance(right.cshape))
            if not leftStay:
                self.remove(left)
            if not rightStay:
                self.remove(right)
            if not self.player.domain.alive:
                self.gameOver()


    def sticksCollectingHandling(self, dt):
        playerActor = self.player
        playerLogic = self.player.domain
        if not keyboard[key.E]:
            self.collector.stop()
        else:
            for maybeSticks in self.cm.objs_colliding(playerActor):
                if hasattr(maybeSticks, "domain")\
                        and isinstance(maybeSticks.domain, Sticks):
                    sticks = maybeSticks.domain
                    self.collector.collect(playerLogic, sticks)
                    if maybeSticks.domain.value <= 0:
                        self.remove(maybeSticks)
                    # injected in generateSticks. update sprite image
                    updateSticksCountSprite(maybeSticks)

    def update(self, dt):
        # update list of collidable objects
        self.cm.clear()
        for z, node in self.children:
            self.cm.add(node)

        lastRect = self.player.get_rect()
        newRect, dx, dy = self.movementHandling(lastRect, dt)

        self.collisionHandling(lastRect, newRect)
        self.sticksCollectingHandling(dt)
        # self.collideMapHandling(lastRect, newRect, dx, dy)
        scroller.set_focus(self.player.x, self.player.y)

    def addCollidable(self, obj):
        assert hasattr(obj, "cshape") and isinstance(obj.cshape,
                                                     cm.CircleShape), \
            f"can't addCollidable with {obj}"
        ScrollableLayer.add(self, obj)
        print("addCollidable", obj.cshape.center)
        self.cm.add(obj)

    def gameOver(self):
        print("DIED")
        self.unschedule(self.update)
        pass


class BearActor(Actor):
    def __init__(self, player, position=(0,0)):
        Actor.__init__(self, getBearSprite(), position=position, domain=Bear())
        self.scale = 2
        self.player = player
        self.schedule_interval(self.update, .10)
        self.move = Move()
        # self.velocity = (0,0)
        self.do(self.move)
        self.accel = Accelerator(46, 5, 40)

    def update(self, dt):
        self.goTo(self.player)

    def goTo(self, target:Actor):
        self.accel.accelerate()
        self.velocity = followSpeed(self.cshape, self.accel.speed, target.cshape)
        self.setPos(self.position)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("start app")

    WIDTH = 800
    HEIGHT = 600
    director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=False)
    mapTMX = load("assets/map.tmx")
    mapLayer = mapTMX["terrain"]
    scroller = ScrollingManager()
    mapLayer.set_cell_opacity(3,3, 0)
    mapLayer.set_cell_opacity(4,4, 10000)
    scroller.add(mapLayer, z=1)
    # scroller.add(collideMap, z=1)

    player = Actor('assets/user.png', position=(20, 20),
                   domain=Player())  # ActorPlayer(collideMap)

    scrollLayer = ActorsLayer(player, mapLayer.px_width, mapLayer.px_height)
    scrollLayer.addCollidable(player)

    generateTraps(scrollLayer)
    generateSticks(scrollLayer)
    scroller.add(scrollLayer, z=2)

    bear = BearActor(player, (100, 100))

    scrollLayer.addCollidable(bear)

    scene = Scene(scroller)

    # scene.add(hudBackground, z=2)

    hud = HUD(player, WIDTH, HEIGHT)
    scene.add(hud, z=3)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
