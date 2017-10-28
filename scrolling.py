# Imports as usual
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action, AccelDeccel
from pyglet.window import key

from cocos.mapcolliders import RectMapCollider

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

    def __init__(self, mapLayer):
        self.map = mapLayer
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

        # handling collisions
        self.target.velocity = self.collide_map(self.map, lastRect, newRect, dx, dy)

        self.target.position = newRect.center
        # Lastly, this line simply tells the ScrollingManager to set the center of the screen on the sprite
        scroller.set_focus(self.target.x, self.target.y)



class UserLayer(ScrollableLayer):
    def __init__(self, mapLayer):
        super(UserLayer, self).__init__()

        self.sprite = Sprite("assets/user.png")
        self.sprite.position = 20, 20
        self.add(self.sprite)
        self.sprite.do(PlayerMover(mapLayer))


if __name__ == "__main__":

    director.init(width=800, height=600, autoscale=False, resizable=True)

    mapLayer = load("assets/map.tmx")["terrain"]
    userLayer = UserLayer(mapLayer)

    scroller = ScrollingManager()
    # Order is important! 
    scroller.add(mapLayer)
    scroller.add(userLayer)
    scene = Scene(scroller)
    # I also need to push the handlers from the window to the object from Pyglet
    # If I don't, it won't be able to handle the Cocos2D keyboard input!
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
