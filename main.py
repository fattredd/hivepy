#!/usr/bin/python

import pygame as pg
from pygame.locals import *
import sys
from map import *
from units import *


pg.init()
pg.font.init()

dim = (700, 400)
scr = pg.display.set_mode(dim)
pg.display.set_caption("Hive")
clk = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.M_CLICK:
            print("UP")
        pg.display.flip()
        clk.tick(20)
