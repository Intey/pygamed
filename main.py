#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

if __name__ == "__main__":
    pygame.init()
    size=[700,500]
    screen=pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    end = False
    while not end:
        for event in pygame.event.get():
            it event.type == pygame.QUIT:
                done = True
            clock.tick(20)

