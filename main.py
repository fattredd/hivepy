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

hexs = [
    map.Hex(0,0,0),
    map.Hex(1,-1,0),
    map.Hex(-1,1,0),
    map.Hex(0,1,-1),
    map.Hex(0,-1,1)
    ]
for h in hexs:
    ptl = L.polygon_corners(h)
    pg.draw.polygon(scr, 0x00FF00, ptl)
    pg.draw.polygon(scr, 0xFFFFFF, ptl, 1)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.K_UP:
            print("UP")
        pg.display.flip()
        clk.tick(20)
