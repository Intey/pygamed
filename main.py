#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyglet import image
from pyglet.gl import *
from pyglet import font

from cocos.director import *
from cocos.layer import *
from cocos.menu import *
from cocos.scene import *

playerSprite = pyglet.resource.image('player7.png')
trapSprite = pyglet.resource.image('circle6.png')


class GameLayer(Layer):
    def __init__(self):
        super(GameLayer, self).__init__()
        self.schedule(self.update)

    def update(self, dt):
        pass


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
    director.init(resizable=True)
    sceneRoot = Scene(RootMenu())
    director.run(sceneRoot)
