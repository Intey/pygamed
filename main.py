#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyglet.window import key
from pyglet import image
from pyglet.gl import *
from pyglet import font

from cocos.director import *
from cocos.layer import *
from cocos.menu import *
from cocos.scene import *
from cocos.sprite import *
from cocos.batch import *
from cocos.actions import *

import cocos.collision_model as cm

from game.utils import *

playerSprite = pyglet.resource.image('user.png')
trapSprite = pyglet.resource.image('trap.png')

WIDTH = 800
HEIGHT = 600

TRAP_SIZE = 20
class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.batch = BatchNode()
        self.schedule(self.update)

        cell_size = TRAP_SIZE
        self.collman = cm.CollisionManagerGrid(0.0, WIDTH,
                                               0.0, HEIGHT,
                                               cell_size, cell_size)

        self.player = Sprite(playerSprite)
        self.player.position = 10, 10
        self.player.velocity = 0, 0
        self.player.speed = 150
        self.player.size = 30
        self.batch.add(self.player)

        for t in range(0, 10):
            trap = Sprite(trapSprite)
            trap.position = randomPosition(TRAP_SIZE, WIDTH, HEIGHT)
            self.batch.add(trap)

        self.add(self.batch)

        self.player.do(Move())

    def on_key_press(self, symbol, modifiers):
        vx, vy = self.player.velocity
        if symbol == key.LEFT:
            self.player.velocity = -self.player.speed, vy
        elif symbol == key.RIGHT:
            self.player.velocity = self.player.speed, vy
        elif symbol == key.UP:
            self.player.velocity = vx, self.player.speed
        elif symbol == key.DOWN:
            self.player.velocity = vx, -self.player.speed
        elif symbol == key.SPACE:
            self.player.velocity = 0, 0


    def update(self, dt):
        pass
        # self.collman.clear()
        # for z, node in self.children:
        #     self.collman.add(node)

        # # interactions player - others
        # for other in self.collman.iter_colliding(self.player):
        #     self.toRemove.add(other)

        # for node in self.toRemove:
        #     self.remove(node)
        # self.toRemove.clear()



class RootMenu(Menu):
    def __init__(self):
        super(RootMenu, self).__init__('Guerilla')
        self.menu_valign = CENTER
        self.menu_haligh = BOTTOM

        items = [
        ( MenuItem('New Game',  self.on_newgame) ),
        ( MenuItem('Continue',  self.on_continue_game) ),
        ( MenuItem('Setings',   self.on_settings_open) ),
        ( MenuItem('Quit',      self.on_quit) ),
        ]

        self.create_menu(items, shake(), shake_back())

    def on_quit(self):
        pyglet.app.exit()

    def on_newgame(self):

        pass

    def on_continue_game(self):
        pass

    def on_settings_open(self):
        pass


if __name__ == "__main__":
    director.init(width=WIDTH, height=HEIGHT)
    # sceneRoot = Scene(RootMenu())
    sceneRoot = Scene(GameLayer())
    director.run(sceneRoot)
