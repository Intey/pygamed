# Imports as usual
from pyglet.window import key

from cocos.actions import Action, AccelDeccel
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.tiles import load

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


class PlayerMover (Action, RectMapCollider):

    def __init__(self, collideMap=None):
        self.collideMap = collideMap
        super().__init__()
        self.on_bump_handler = self.on_bump_slide

    def start(self):
        # We simply set the velocity of the target sprite to zero
        self.target.velocity = 0, 0
        self.accelerator = Accelerator(250, 5, 40, 4)

    def step(self, dt):
        """ moving player and check collide with static objects."""
        dx = self.target.velocity[0]
        dy = self.target.velocity[1]

        if keyboard[key.UP] + keyboard[key.DOWN] + keyboard[key.LEFT] + keyboard[key.RIGHT] > 0:
            self.accelerator.accelerate()
        else:
            self.accelerator.deaccelerate()

        dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.accelerator.accel * dt
        dy = (keyboard[key.UP] - keyboard[key.DOWN]) * self.accelerator.accel * dt

        lastRect = self.target.get_rect()
        newRect = lastRect.copy()
        newRect.x += dx
        newRect.y += dy

        # handling collisions with static objects(trees, rocks, etc.)
        if self.collideMap:
            self.target.velocity = self.collide_map(self.collideMap, lastRect, newRect, dx, dy)
        # handling ollisions with dinamic objects


        self.target.position = newRect.center
        # Lastly, this line simply tells the ScrollingManager to set the center of the screen on the sprite
        scroller.set_focus(self.target.x, self.target.y)


class ActorsLayer(ScrollableLayer):
    def __init__(self, playerObject, width, height):
        ScrollableLayer.__init__(self)

        self.height = height
        self.width = width
        self.player = playerObject
        self.cm = cm.CollisionManagerGrid(0.0, self.width, 0.0, self.height,
                                          TILE_WIDTH, TILE_WIDTH)
        # call update
        self.schedule(self.update)

    def addCollidable(self, obj):
        assert hasattr(obj, "cshape") and isinstance(obj.cshape, cm.CircleShape),\
            "cant addCollidable with %s" % obj
        ScrollableLayer.add(self, obj)

    def update(self, dt):
        # update list of collidable objects
        self.cm.clear()
        for z, node in self.children:
            self.cm.add(node)

        # collide!!!
        for coll in self.cm.iter_colliding(self.player):
            print("some collide", coll)

        for neighbor in self.cm.objs_near(self.player, 250):
            print("neighbor", neighbor)
            if hasattr(neighbor, "trap"):
                trap = neighbor.trap
                if neighbor.near_than(self.player, trap.range()):
                    self.player.hit(trap.power)


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
        self.do(PlayerMover(collideMap))

    def setPos(self, pos):
        """ pos should be tuple"""
        staticSetPos(self, pos)


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
    scroller.add(mapLayer,  z=0)

    # scroller.add(collideMap, z=1)

    for i in range(0, 10):
        trap = ActorTrap(10)
        trap.setPos( (int(random()*mapLayer.px_width), int(random()*mapLayer.px_height)) )
        scrollLayer.addCollidable(trap)

    scroller.add(scrollLayer, z=2)

    scene = Scene(scroller)
    # I also need to push the handlers from the window to the object from Pyglet
    # If I don't, it won't be able to handle the Cocos2D keyboard input!
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
