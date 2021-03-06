#!/usr/bin/python

import pygame as pg
from pygame.locals import *
import sys
import map


pg.init()
pg.font.init()

game = map.Game(450, 450, "Hive")

while True:
    if pg.event.peek():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYUP:
                print("Keyup",event.key)
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            pg.display.flip()
            #print(event.type)
