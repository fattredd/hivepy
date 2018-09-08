#!/usr/bin/python

import pygame as pg
from pygame.locals import *
import sys
import map


pg.init()
pg.font.init()

dim = (700, 400)
scr = pg.display.set_mode(dim)
pg.display.set_caption("Hive")
clk = pg.time.Clock()

s = map.Point(15,15)
orient = map.layout_flat
origin = map.Point(dim[0]/2, dim[1]/2)
L = map.Layout(orient, s, origin)
M = map.Map(scr, L)
M.gen_map("hex", 5)
M.draw_map()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        pg.display.flip()
        clk.tick(20)
