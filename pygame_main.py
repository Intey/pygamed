#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)

def draws(screen):
    screen.fill(BLACK)
    pygame.draw.line(screen, GRAY, [0,1], [700,1], 20)
    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    size=[700,500]
    screen=pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    end = False
    while not end:
        
        for event in pygame.event.get():
            print("event", event.type)
            if event.type == pygame.QUIT:
                print("QUIT")
                end = True

        draws(screen)

        clock.tick(60)
        
    pygame.quit()
