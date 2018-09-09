#!/usr/bin/python

import pygame as pg
from pygame.locals import *
import sys
import map


pg.init()
pg.font.init()

dim = (450, 400)
scr = pg.display.set_mode(dim)

pg.display.set_caption("Hive")
clk = pg.time.Clock()

s = map.Point(23,23)
orient = map.layout_pointy
origin = map.Point(dim[0]/2, dim[1]/2)
L = map.Layout(orient, s, origin)
M = map.Map(scr, L)
#M.gen_map("hex", 6)
#M.draw_map()

while True:
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
            p = map.Point(event.pos[0], event.pos[1])
            newHex = L.pixel_to_hex(p)
            newHex.bgcolor = 0x0F0F0F
            M.draw_hex(newHex)
        pg.display.flip()
        #print(event.type)
