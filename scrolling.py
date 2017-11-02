# Imports as usual
from pyglet.window import key

from cocos.actions import Action, AccelDeccel
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.text import Label

from game.player import Player
from game.trap import Trap
from random import random
import cocos.collision_model as cm
import cocos.euclid as eu

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

        self.toRemove = []
        # call update
        self.schedule(self.update)

    def movementHandling(self, lastRect, dt):
        dx = self.player.velocity[0]
        dy = self.player.velocity[1]

        if keyboard[key.UP] + keyboard[key.DOWN] + keyboard[key.LEFT] + keyboard[key.RIGHT] > 0:
            self.accelerator.accelerate()
        else:
            self.accelerator.deaccelerate()

        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.accelerator.accel * dt
        dy = (keyboard[key.UP] - keyboard[key.DOWN]) * self.accelerator.accel * dt

        newRect = lastRect.copy()
        newRect.x += dx
        newRect.y += dy

        self.player.setPos(newRect.center)

        return newRect

    def collideHandling(self, lastRect, newRect):

        # handling collisions with static objects(trees, rocks, etc.)
        if self.collideMap:
            collider = self.mapCollider
            self.player.velocity = collider.collide_map(self.collideMap,
                                                        lastRect,
                                                        newRect,
                                                        dx, dy)
        # handling collisions with dinamic objects
        cctr = self.player.cshape.center

        # for coll in self.cm.iter_colliding(self.player):
        #     print("some collide", coll)

        for neighbor in self.cm.objs_near(self.player, Trap.MAX_RANGE):
            if hasattr(neighbor, "trap"):
                trap = neighbor.trap
                if neighbor.cshape.near_than(self.player.cshape, trap.range()):
                    self.player.player.hit(trap.power)
                    self.toRemove.append(neighbor)

        for rm in self.toRemove:
            self.remove(rm)
        self.toRemove.clear()


    def update(self, dt):
        # update list of collidable objects
        self.cm.clear()
        for z, node in self.children:
            # print("update", type(node), node.cshape.center)
            self.cm.add(node)

        lastRect = self.player.get_rect()
        newRect = self.movementHandling(lastRect, dt)

        self.collideHandling(lastRect, newRect)

        scroller.set_focus(self.player.x, self.player.y)

    def addCollidable(self, obj):
        assert hasattr(obj, "cshape") and isinstance(obj.cshape, cm.CircleShape),\
            "cant addCollidable with %s" % obj
        ScrollableLayer.add(self, obj)
        print("addCollidable", obj.cshape.center)
        self.cm.add(obj)


class ActorTrap(Sprite):
    def __init__(self, power, range=Trap.MIN_RANGE, position=(0,0)):
        Sprite.__init__(self, "assets/trap.png")
        self.position = position
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), TILE_WIDTH)
        self.setPos(self.position)
        self.trap = Trap(power, range)

    def setPos(self, pos):
        staticSetPos(self, pos)


class ActorPlayer(Sprite):
    def __init__(self, collideMap=None):
        Sprite.__init__(self, "assets/user.png")
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), TILE_WIDTH)
        self.setPos(self.position)
        self.player = Player()
        self.velocity = 0, 0

    def setPos(self, pos):
        """ pos should be tuple"""
        staticSetPos(self, pos)


class Hud(ScrollableLayer):
    def __init__(self, player, width, height):
        super(Hud, self).__init__()
        self.width = width
        self.height = height
        self.player = player
        self.msg = Label('health %s' % self.player.player.health,
                         font_name='somebitch',
                         anchor_x='left',
                         anchor_y='top',
                         align='left')
        self.add(self.msg)
        self.schedule(self.update)

    def update(self, dt):
        self.msg = Label('health %s' % self.player.player.health,
                         font_name='somebitch',
                         anchor_x='left',
                         anchor_y='top',
                         align='left')

if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600

    director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=True)

    mapTMX = load("assets/map.tmx")
    mapLayer = mapTMX["terrain"]
    # if i have static collide objects, i should add them to collide layer in tmx file
    # collideMap = mapTMX['collide']
    player = ActorPlayer() # ActorPlayer(collideMap)
    player.setPos( (20, 20) )

    scrollLayer = ActorsLayer(player, WIDTH, HEIGHT)

    scrollLayer.addCollidable(player)

    scroller = ScrollingManager()

    scroller.add(mapLayer,  z=1)
    hud = Hud(player, WIDTH, HEIGHT)
    scroller.add(hud, z=2)

    # scroller.add(collideMap, z=1)

    for i in range(0, 10):
        trap = ActorTrap(10)
        trap.setPos( (int(random()*mapLayer.px_width), int(random()*mapLayer.px_height)) )
        scrollLayer.addCollidable(trap)

    scroller.add(scrollLayer, z=4)

    scene = Scene(scroller)
    # I also need to push the handlers from the window to the object from Pyglet
    # If I don't, it won't be able to handle the Cocos2D keyboard input!
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
