# Imports as usual
from random import random, randrange
import time

import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.layer.util_layers import ColorLayer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.tiles import load
from pyglet.window import key

from domain.player import Player
from domain.trap import Trap
from domain.sticks import Sticks
from domain.utils import collectResource

from time import time
from domain.collector import Collector

def staticSetPos(obj, position):
    """ position is tuple"""
    assert isinstance(position, tuple), "should be tuple"
    obj.position = position
    obj.cshape.center = eu.Vector2(*position)


TILE_WIDTH = 15


class Accelerator:
    """Control acceleration function"""

    def __init__(self, maxAccel, initAccel, subAccel, upSpeed):
        self.maxAccel = maxAccel
        self.minAccel = initAccel
        self.accel = initAccel
        self.subAccel = subAccel
        self.upSpeed = 4

    def accelerate(self):
        if self.accel < self.maxAccel:
            self.accel += self.subAccel
        if self.accel > self.maxAccel:
            self.accel = self.maxAccel

    def deaccelerate(self):
        self.accel = self.minAccel


class ActorsLayer(ScrollableLayer):
    def __init__(self, playerObject, width, height, collideMap=None):
        ScrollableLayer.__init__(self)

        self.height = height
        self.width = width
        self.player = playerObject
        self.accelerator = Accelerator(250, 5, 40, 4)

        self.mapCollider = RectMapCollider()
        self.mapCollider.on_bump_handler = self.mapCollider.on_bump_slide
        self.collideMap = collideMap

        self.cm = cm.CollisionManagerGrid(0.0, self.width, 0.0, self.height,
                                          TILE_WIDTH, TILE_WIDTH)

        self.collectingSticks = False
        self.collectingStartTime = None
        # call update
        self.collector = Collector()
        self.schedule(self.update)

    def movementHandling(self, lastRect, dt):
        dx = self.player.velocity[0]
        dy = self.player.velocity[1]

        if keyboard[key.UP] + keyboard[key.DOWN] + keyboard[key.LEFT] + \
                keyboard[key.RIGHT] > 0:
            self.accelerator.accelerate()
        else:
            self.accelerator.deaccelerate()

        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT])\
                * self.accelerator.accel * dt
        dy = (keyboard[key.UP] - keyboard[key.DOWN])\
                * self.accelerator.accel * dt

        newRect = lastRect.copy()
        newRect.x += dx
        newRect.y += dy

        self.player.setPos(newRect.center)

        return (newRect, dx, dy)

    def collideMapHandling(self, lastRect, newRect, dx, dy):
        # handling collisions with static objects(trees, rocks, etc.)
        if self.collideMap:
            collider = self.mapCollider
            self.player.velocity = collider.collide_map(self.collideMap,
                                                        lastRect,
                                                        newRect,
                                                        dx, dy)

    def trapCollideHandling(self, lastRect, newRect):
        # handling collisions with dynamic objects
        for maybeTrap in self.cm.objs_near(self.player, Trap.MAX_RANGE):
            if hasattr(maybeTrap, "domain") \
                    and isinstance(maybeTrap.domain, Trap):
                trap = maybeTrap.domain
                if maybeTrap.cshape.near_than(self.player.cshape, trap.range()):
                    self.player.domain.hit(trap.power)
                    self.remove(maybeTrap)

    def sticksCollectingHandling(self, dt):
        playerActor = self.player
        playerLogic = player.domain 
        if not keyboard[key.E]:
            self.collector.stop()
        else:
            for maybeSticks in self.cm.objs_colliding(playerActor):
                if hasattr(maybeSticks, "domain")\
                        and isinstance(maybeSticks.domain, Sticks):
                    sticks = maybeSticks.domain
                    self.collector.collect(playerLogic, sticks)

    def update(self, dt):
        # update list of collidable objects
        self.cm.clear()
        for z, node in self.children:
            self.cm.add(node)

        lastRect = self.player.get_rect()
        newRect, dx, dy = self.movementHandling(lastRect, dt)

        self.trapCollideHandling(lastRect, newRect)
        self.sticksCollectingHandling(dt)
        # self.collideMapHandling(lastRect, newRect, dx, dy)
        scroller.set_focus(self.player.x, self.player.y)

    def addCollidable(self, obj):
        assert hasattr(obj, "cshape") and isinstance(obj.cshape,
                                                     cm.CircleShape), \
            "can't addCollidable with %s" % obj
        ScrollableLayer.add(self, obj)
        print("addCollidable", obj.cshape.center)
        self.cm.add(obj)


class Actor(Sprite):
    def __init__(self, spriteFilepath, position=(0, 0), domain=None):
        Sprite.__init__(self, spriteFilepath)
        self.position = position
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), TILE_WIDTH)
        self.setPos(self.position)
        self.domain = domain
        self.velocity = 0, 0

    def setPos(self, pos):
        staticSetPos(self, pos)


class Hud(Layer):
    def __init__(self, player, width, height):
        Layer.__init__(self)
        self.width = width
        self.height = height
        self.player = player.domain
        self.playerOldHp = self.player.health
        msg = Label('health %s, sticks: %s' % (self.player.health, 
                                               self.player.inventory.get('sticks', 0)),
                    font_name='somebitch',
                    anchor_x='left',
                    anchor_y='top',  # really - it's top of screen
                    width=width,
                    height=25,
                    x=5,
                    y=height-3,
                    )

        hudBackground = ColorLayer(73, 106, 44, 255, width=WIDTH, height=25)
        hudBackground.position= (0, HEIGHT-25)
        self.add(hudBackground)
        self.add(msg, name='msg')
        self.schedule(self.update)

    def update(self, dt):
        p = self.player
        hp = p.health
        label = self.get('msg').element
        label.begin_update()
        label.text = 'health {}, sticks: {}'.format(hp,
                                                    p.inventory.get('sticks', 0))
        label.end_update()


def randomPos(w, h):
    return (int(random() * w), int(random() * h))


def generateTraps(scrollLayer):
    for i in range(0, 10):
        trap = Actor('assets/trap.png',
                     position=randomPos(WIDTH, HEIGHT),
                     domain=Trap(randrange(1, 30),
                                 randrange(Trap.MIN_RANGE, Trap.MAX_RANGE)))
        scrollLayer.addCollidable(trap)


def generateSticks(scrollLayer):
    for i in range(0, 10):
        sticks = Actor('assets/sticks.png',
                       position=randomPos(WIDTH, HEIGHT),
                       domain=Sticks(randrange(5, 20)))
        scrollLayer.addCollidable(sticks)

if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600
    director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=True)
    mapTMX = load("assets/map.tmx")
    mapLayer = mapTMX["terrain"]
    scroller = ScrollingManager()
    scroller.add(mapLayer, z=1)
    # scroller.add(collideMap, z=1)

    player = Actor('assets/user.png', position=(20, 20),
                   domain=Player())  # ActorPlayer(collideMap)
    scrollLayer = ActorsLayer(player, mapLayer.px_width, mapLayer.px_height)
    scrollLayer.addCollidable(player)
    generateTraps(scrollLayer)
    generateSticks(scrollLayer)
    scroller.add(scrollLayer, z=2)

    scene = Scene(scroller)

    # scene.add(hudBackground, z=2)

    hud = Hud(player, WIDTH, HEIGHT)
    scene.add(hud, z=3)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
