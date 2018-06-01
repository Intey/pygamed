"""
scrolling.py - scroller game about you, bear, traps and sticks
Usage:
    scrolling.py [options]

Options:
    -d --debug  debug mode with logging
"""
import logging

import cocos.collision_model as cm
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.mapcolliders import RectMapCollider
from cocos.scene import Scene
from cocos.tiles import load
from docopt import docopt
from pyglet.window import key

from actors import BearFactory, TrapFactory, BearActor, MapPositioner
from domain import Event
from actors import PlayerActor
from actors.sticks_factory import SticksFactory
from gui.hud import HUD

# does not affect any
TILE_WIDTH = 25

logger = logging.getLogger(__name__)


class ActorsLayer(ScrollableLayer):
    def __init__(self, playerObject, width, height, collide_manager=None, collideMap=None):
        ScrollableLayer.__init__(self)

        self.height = height
        self.width = width
        self.player = playerObject

        # collision with map (static objects)
        self.mapCollider = RectMapCollider()
        self.mapCollider.on_bump_handler = self.mapCollider.on_bump_slide
        self.collideMap = collideMap

        # call update
        self.schedule(self.update)
        self.cm = collide_manager

    def collide_map(self, lastRect, newRect, dx, dy):
        """
        Handling collisions with static objects(trees, rocks, etc.)
        """
        if self.collideMap:
            collider = self.mapCollider
            return collider.collide_map(self.collideMap,
                                        lastRect,
                                        newRect,
                                        dx, dy)
        else:
            return 0,0

    def collisionHandling(self):
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
                    # self.cm.remove_tricky(left)
            if not rightStay:
                if self.__contains__(right):
                    self.remove(right)
                    # self.cm.remove_tricky(right)
            if not self.player.domain.alive:
                self.gameOver()

    def update(self, dt):
        # update list of collidable objects
        self.cm.clear()
        for z, node in self.children:
            self.cm.add(node)

        self.collisionHandling()
        scroller.set_focus(self.player.x, self.player.y)

    def addCollidable(self, obj):
        assert hasattr(obj, "cshape") and isinstance(obj.cshape,
                                                     cm.CircleShape), \
            f"can't addCollidable with {obj}"
        obj.link_layer(self)
        ScrollableLayer.add(self, obj)
        logger.debug(f"addCollidable {obj.cshape.center}")
        self.cm.add(obj)

    def gameOver(self):
        logger.debug("DIED")
        self.unschedule(self.update)


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
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    mapTMX = load("assets/map.tmx")
    mapLayer = mapTMX["terrain"]
    collideLayer = mapTMX['blocks']
    scroller = ScrollingManager()
    scroller.add(mapLayer, z=1)
    # scroller.add(collideMap, z=1)
    collide_manager = cm.CollisionManagerGrid(0.0, mapLayer.px_width, 0.0, mapLayer.px_height,
                                              TILE_WIDTH * 3, TILE_WIDTH * 3)

    player = PlayerActor(collide_manager, keyboard)  # ActorPlayer(collideMap)

    scrollLayer = ActorsLayer(player, mapLayer.px_width, mapLayer.px_height, collide_manager, collideLayer)
    scroller.add(scrollLayer, z=2)

    scrollLayer.addCollidable(player)


    def layer_subscriber(event: Event):
        logger.debug(f"handle event {event}")
        if event.type == Event.CREATE_TYPE:
            scrollLayer.addCollidable(event.payload)


    map_positioner = MapPositioner(WIDTH, HEIGHT)
    bear_factory = BearFactory(player, map_positioner)
    bear_factory.set_positioner(map_positioner)
    bear = BearActor(player, (200, 200))
    layer_subscriber(Event(Event.CREATE_TYPE, bear))
    # bear_factory.subscribe(layer_subscriber)
    # for i in range(15):
    #     bear_factory.create()

    trap_factory = TrapFactory(mapLayer.px_width, mapLayer.px_height)
    trap_factory.subscribe(layer_subscriber)
    for i in range(3):
        trap_factory.create()

    sticks_factory = SticksFactory(mapLayer.px_width, mapLayer.px_height)
    sticks_factory.subscribe(layer_subscriber)
    for i in range(3):
        sticks_factory.create()

    scene = Scene(scroller)

    # scene.add(hudBackground, z=2)

    hud = HUD(player, WIDTH, HEIGHT)
    scene.add(hud, z=3)

    director.run(scene)
