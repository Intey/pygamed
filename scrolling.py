"""
scrolling.py - scroller game about you, bear, traps and sticks
Usage:
    scrolling.py [options]

Options:
    -d --debug  debug mode with logging
"""
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.tiles import load
from pyglet.window import key

from domain import Player
from domain import Trap
from domain import Bear
from domain import Sticks
from domain import Collector
from domain.utils import Accelerator
from actors import Actor, BearFactory, TrapFactory
from actors import Event
# from init import generateSticks, generateTraps
#FIXME: WTF import
from init import updateSticksCountSprite

from gui.hud import HUD


import logging

from docopt import docopt
from utils.random import randomPos

# does not affect any
TILE_WIDTH = 15

logger = logging.getLogger(__name__)

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
        Handle collision of objects
        """
        # handling collisions with dynamic objects
        from domain.collision import collide
        for left, right in self.cm.iter_all_collisions():

            leftStay, rightStay = collide(left.domain, right.domain, left.cshape.distance(right.cshape))
            if not leftStay:
                if self.__contains__(left):
                    self.remove(left)
            if not rightStay:
                if self.__contains__(right):
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
        logger.debug(f"addCollidable {obj.cshape.center}")
        self.cm.add(obj)

    def gameOver(self):
        logger.debug("DIED")
        self.unschedule(self.update)
        pass



if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")

    level = logging.CRITICAL
    if args['--debug']:
        level = logging.DEBUG

    logging.basicConfig(level=level)

    logger.info("start scrolling")

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
    scroller.add(scrollLayer, z=2)

    scrollLayer.addCollidable(player)

    # generateTraps(scrollLayer)
    # generateSticks(scrollLayer)

    def layer_subscriber(event:Event):
        logger.debug(f"handle event {event}")
        if event.type == Event.CREATE_TYPE:
            scrollLayer.addCollidable(event.payload)

    bear_factory = BearFactory(WIDTH, HEIGHT, player)
    bear_factory.subscribe(layer_subscriber)
    for i in range(5):
        bear_factory.create()

    trap_factory = TrapFactory(WIDTH, HEIGHT)
    trap_factory.subscribe(layer_subscriber)
    for i in range(10):
        trap_factory.create()

    scene = Scene(scroller)

    # scene.add(hudBackground, z=2)

    hud = HUD(player, WIDTH, HEIGHT)
    scene.add(hud, z=3)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    director.run(scene)
