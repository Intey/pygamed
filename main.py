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
import cocos.euclid as eu

import cocos.collision_model as cm

from game.utils import *

playerSprite = pyglet.resource.image('user.png')
trapSprite = pyglet.resource.image('trap.png')

WIDTH = 800
HEIGHT = 600

TRAP_SIZE = 20

fe = 1.0e-4
consts = {
    "window": {
        "width": 800,
        "height": 600,
        "vsync": True,
        "resizable": True
    },
    "world": {
        "width": 400,
        "height": 300,
        "rPlayer": 8.0,
        "wall_scale_min": 0.75,  # relative to player
        "wall_scale_max": 2.25,  # relative to player
        "topSpeed": 100.0,
        "angular_velocity": 240.0,  # degrees / s
        "accel": 85.0,
        "bindings": {
            'left'  : key.A,
            'right' : key.D,
            'up'    : key.W,
            'down'  : key.S,
        }
    },
    "view": {
        # as the font file is not provided it will decay to the default font;
        # the setting is retained anyway to not downgrade the code
        "font_name": 'Axaxax',
        "palette": {
            'bg': (0, 65, 133),
            'player': (237, 27, 36),
            'wall': (247, 148, 29),
            'gate': (140, 198, 62),
            'food': (140, 198, 62)
        }
    }
}


class GameLayer(Layer):
    is_event_handler = True

    def init
    def __init__(self):
        super(GameLayer, self).__init__()

        world = consts['world']
        self.bindings = world['bindings']
        buttonsPressed = set()
        for direction in self.bindings:
            buttonsPressed[direction] = False
        self.buttonsPressed = buttonsPressed

        cell_size = TRAP_SIZE
        self.collman = cm.CollisionManagerGrid(0.0, WIDTH,
                                               0.0, HEIGHT,
                                               cell_size, cell_size)

        self.batch = BatchNode()

        self.player = Sprite(playerSprite)
        self.player.position = 10, 10
        self.player.velocity = 0, 0
        self.batch.add(self.player)

        for t in range(0, 10):
            trap = Sprite(trapSprite)
            trap.position = randomPosition(TRAP_SIZE, WIDTH, HEIGHT)
            self.batch.add(trap)

        self.add(self.batch)

        self.schedule(self.update)

    def on_key_press(self, k, m):
        binds = self.bindings
        for action, key in binds.items():
            if key == k:
                self.buttonsPressed[action] = True
                return True
        return False

    def on_key_release(self, k, m):
        binds = self.bindings
        for action, key in binds.items():
            if key == k:
                self.buttonsPressed[action] = False
                return True
        return False

    def update(self, dt):
        newVel = self.player.velocity

        buttonsPressed = self.buttonsPressed
        if buttonsPressed['up'] or buttonsPressed['down']:
            newVel += dt * self.player.accel * self.impulse_dir
            nv = newVel.magnitude()
            if nv > self.topSpeed:
                newVel *= self.topSpeed / nv

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
