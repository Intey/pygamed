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
    def __init__(self):
        cell_size = 15
        self.cm = cm.CollisionManagerGrid(0.0, self.width, 
                                          0.0, self.height, 
                                          cell_size, cell_size)
        # call update 
        self.schedule(self.update)


    def update(self, dt):
        # update list of collidable objects
        self.collman.clear()
        for z, node in self.children:
            self.collman.add(node)

        # collide!!!
        for trap in self.traps:
            maybePlayer = self.cm.any_near(trap, trap.range)
            if isinstance(maybePlayer, Player):
                pass
                





class ActorTrap(Trap, Sprite):
    def __init__(self, power, range=Trap.MIN_RANGE):
        Trap.__init__(self, power, range)
        Sprite.__init__(self, "assets/trap.png")
        self.cshape = cm.CircleShape(self.widht/2, self.height/2)


class ActorPlayer(Player, Sprite):
    def __init__(self, collideMap=None):
        Sprite.__init__(self, "assets/user.png")
        self.position = 20, 20
        Player.__init__(self)
        self.do(PlayerMover(collideMap))
        self.cshape = cm.CircleShape(self.width/2, self.height/2)
        

if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600

    director.init(width=WIDTH, height=HEIGHT, autoscale=False, resizable=True)

    mapTMX = load("assets/map.tmx")
    mapLayer = mapTMX["terrain"]
    # if i have static collide objects, i should add them to collide layer in tmx file
    # collideMap = mapTMX['collide']
    scrollLayer = ActorsLayer()
    player = ActorPlayer() # ActorPlayer(collideMap)

    scrollLayer.add(player)
    cm.add(player)

    scroller = ScrollingManager()
    scroller.add(mapLayer,  z=0)

    # scroller.add(collideMap, z=1)

    for i in range(0, 10):
        trap = ActorTrap(10)
        trap.position = int(random()*WIDTH), int(random()*HEIGHT)
        scrollLayer.add(trap)
        cm.add(trap)

    scroller.add(scrollLayer, z=2)

    scene = Scene(scroller)
    # I also need to push the handlers from the window to the object from Pyglet
    # If I don't, it won't be able to handle the Cocos2D keyboard input!
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
