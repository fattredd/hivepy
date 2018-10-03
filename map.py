# Hive Classes
import math as m
import pygame as pg
import config
import units

settings = config.settings
p = config.p


def rgb(value):
    value = hex(value).lstrip('0x')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

class Hex(object):
    def __init__(self, q,r,s):
        try:
            assert(q+r+s == 0)
        except:
            print("Error making hex at {}, {}, {}".format(q,r,s))
            raise AssertionError
        self.loc = (q,r,s)
        self.q = q
        self.r = r
        self.s = s
        self.bgcolor = p['u1']
        self.fgcolor = p['u2']
    
    def __add__(self, other):
        a = self.loc[0] + other.loc[0]
        b = self.loc[1] + other.loc[1]
        c = self.loc[2] + other.loc[2]
        return Hex(a,b,c)
    def __sub__(self, other):
        a = self.loc[0] - other.loc[0]
        b = self.loc[1] - other.loc[1]
        c = self.loc[2] - other.loc[2]
        return Hex(a,b,c)
    def __mul__(self, k):
        a = self.loc[0] * k
        b = self.loc[1] * k
        c = self.loc[2] * k
        return Hex(a,b,c)
    def __eq__(self, other):
        try:
            return self.loc == other.loc
        except TypeError:
            print("TypeError comparing hexes")
            return False
        return false
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __add__(self, other):
        a = self.loc[0] + other.loc[0]
        b = self.loc[1] + other.loc[1]
        c = self.loc[2] + other.loc[2]
        return Hex(a,b,c)
    def __sub__(self, other):
        a = self.loc[0] - other.loc[0]
        b = self.loc[1] - other.loc[1]
        c = self.loc[2] - other.loc[2]
        return Hex(a,b,c)
    def __mul__(self, k):
        a = self.loc[0] * k
        b = self.loc[1] * k
        c = self.loc[2] * k
        return Hex(a,b,c)
    def __repr__(self):
        return "<Hex at {}, {}, {}>".format(self.q, self.r, self.s)


# Helper class
class Orientation(object):
    def __init__(self,f0,f1,f2,f3, b0,b1,b2,b3, start_angle):
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.start_angle = start_angle
layout_pointy = Orientation(m.sqrt(3.0), m.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0,
                            m.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
layout_flat = Orientation(3.0 / 2.0, 0.0, m.sqrt(3.0) / 2.0, m.sqrt(3.0),2.0 / 3.0,
                          0.0, -1.0 / 3.0, m.sqrt(3.0) / 3.0, 0.0)
class Point(object):
    def __init__(self, x, y):
        self.x = x * 1.0
        self.y = y * 1.0
    def l(self):
        return [self.x, self.y]

class Layout(object):
    def __init__(self, orient, size, origin, w, h):
        self.orientation = orient
        self.size = size
        self.origin = origin
        self.w = w
        self.h = h

        self.map_rect = pg.Rect(0, 50, w, h-50)
        self.menu_rect = pg.Rect(0, 0, w, 50)
    def hex_to_pixel(self, h):
        M = self.orientation
        x = (M.f0 * h.q + M.f1 * h.r) * self.size.x
        y = (M.f2 * h.q + M.f3 * h.r) * self.size.y
        return Point(x + self.origin.x, y + self.origin.y)
    def pixel_to_hex(self, p):
        M = self.orientation
        pt = Point((p.x - self.origin.x) / self.size.x,
                   (p.y - self.origin.y) / self.size.y)
        q = M.b0 * pt.x + M.b1 * pt.y
        r = M.b2 * pt.x + M.b3 * pt.y
        return FractionalHex(q, r, -q - r)
    def hex_corner_offset(self, corner):
        size = self.size
        M = self.orientation
        angle = 2.0 * m.pi * (M.start_angle + corner) / 6
        return Point(size.x * m.cos(angle), size.y * m.sin(angle))
    def polygon_corners(self, h):
        corners = []
        center =self.hex_to_pixel(h)
        for i in range(6):
            offset = self.hex_corner_offset(i)
            corners.append(Point(center.x + offset.x,
                                 center.y + offset.y).l())
        return corners

class Icon(object):
    def __init__(self, scr, loc, text, mode, color, altcolor=p['selected']):
        self.txtcolor = p['u1']
        self.color = color
        self.altcolor = altcolor
        self.curColor = color
        self.outline = p['white']
        self.wi = 60
        self.loc = (loc[0]*self.wi, loc[1]*self.wi)
        self.scr = scr
        self.text = text
        self.tcolor = p['white']
        self.mode = mode
        self.selected = False
        l, t = self.loc
        self.fnt = pg.font.SysFont('freemono', 15)
        s = self.fnt.size(self.text)[0]
        self.w = (s//55 + 1)*self.wi
        self.rect = pg.Rect(l,t , self.w, 50)
    def draw(self):
        pg.draw.rect(self.scr, self.curColor, self.rect)
        pg.draw.rect(self.scr, self.outline, self.rect, 1)
        s = self.fnt.size(self.text)
        txt = self.fnt.render(self.text, True, rgb(self.tcolor))
        loc = (self.loc[0]+(self.w//2)-(s[0]//2), 25-(s[1]//2))
        self.scr.blit(txt, loc)
    def clear(self):
        self.selected = False
        self.outline = p['white']
        self.tcolor = p['white']
        self.curColor = self.color
        self.draw()
    def click(self):
        if not self.selected:
            self.selected = True
            self.curColor = self.altcolor
            self.outline = self.color
            self.tcolor = self.color
            self.draw()
        else:
            self.clear()
        return self
        
    
class Menu(object):
    def __init__(self, h, w, scr, units):
        self.size = (h,w)
        self.units = units
        self.icons = []
        swapI = Icon(scr,(8,0), "Player", 0, p['swapl'], p['swapd'])
        for i, u in enumerate(units):
            self.icons.append(Icon(scr,(i,0), u.name, u.mode, u.color))
            '''
            Icon(scr,(0,0), "Queen", 1, p['u1']),
            Icon(scr,(1,0), "Ant", 2, p['u2']),
            Icon(scr,(2,0), "Grasshopper", 3, p['u3']),
            Icon(scr,(4,0), "Spider", 4, p['u4']),
            Icon(scr,(5,0), "Beetle", 5, p['u5']),
            Icon(scr,(8,0), "Player", 0, p['swapl'], p['swapd'])
            '''
        self.icons.append(swapI)
    def draw(self):
        for item in self.icons:
            item.draw()
    def click_button(self, pos):
        try: # Because button isn't always set
            for icon in self.icons: # find hit button
                if icon.rect.collidepoint(pos):
                    button = icon
            for bttn in self.icons: #clear all other bttns
                if not button.mode == 0:
                    if not bttn.mode == 0:
                        bttn.clear()
            return button.click()
        except UnboundLocalError:
            print("No button found at", pos)
    
hex_directions = [
    Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1),
    Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
        

# Standalone Functions:

def length(hex):
    return int((abs(hex.q) + abs(hex.r) + abs(hex.s)) / 2)

def distance(self, a, b):
    return length(a-b)

def direction(direction):
    return hex_directions[direction % 6]

def hex_neighbor(hex, direc):
    return hex + direction(direc)

def FractionalHex(q, r, s):
    q_ = round(q)
    r_ = round(r)
    s_ = round(s)
    q_diff = abs(q_ - q)
    r_diff = abs(r_ - r)
    s_diff = abs(s_ - s)
    if q_diff > r_diff and q_diff > s_diff:
        q_ = -r_ -s_
    elif r_diff > s_diff:
        s_ = -q_ -r_
    else:
        s_ = -q_ -r_
    return Hex(q_, r_, s_)

def lerp(a, b, t): # linear interpolation
    return a* (1-t) + b * t
def hex_lerp(ha, hb, t):
    return FractionalHex(lerp(ha.q, hb.q, t),
                         lerp(ha.r, hb.r, t),
                         lerp(ha.s, hb.s, t))



class Map(object):
    def __init__(self, scr, layout):
        self.scr = scr
        self.L = layout
        self.map = []
        self.highlight = []
        self.fnt = pg.font.SysFont('freemono', 12)
        self.clear_map()
    def draw_hex(self, hex, highlight=False):
        ptl = self.L.polygon_corners(hex)
        if highlight:
            hex.fgcolor = p['h0']
            hex.bgcolor = p['h1']
        pg.draw.polygon(self.scr, hex.fgcolor, ptl)
        if settings['outline']:
            pg.draw.polygon(self.scr, hex.bgcolor, ptl, 1)
        if settings['coords']:
            ct = "{},{}".format(hex.q, hex.r)
            s = self.fnt.size(ct)
            txt = self.fnt.render(ct, True, rgb(hex.bgcolor))
            loc = self.L.hex_to_pixel(hex).l()
            loc[0] = loc[0] - int(s[0]/2)
            loc[1] = loc[1] - int(s[1]/2)
            self.scr.blit(txt, loc)
        elif not highlight:
            loc = self.L.hex_to_pixel(hex).l()
            loc[0] = int(loc[0]+1)
            loc[1] = int(loc[1]+1)
            pg.draw.circle(self.scr, hex.bgcolor, loc, 15)
    def hex_exists(self, hex):
        for val in self.map:
            if hex == val:
                return True
        return False
    def get_hex(self, hex):
        for val in self.map:
            if hex == val:
                return val
        return False
    def hex_distance(self, a, b):
        # 3D Manhatan Distance
        return ( abs(a.q - b.q) + abs(a.r - b.r) + abs(a.s - a.s) ) / 2
    def hex_adjacent(self, hex):
        # If there's at least one adjacent hex
        for i in range(6):
            if self.hex_exists(hex + hex_neighbor(hex, i)):
                self.add_hex(hex+hex_neighbor(hex,i), self.highlight)
                return True
        return False
    def add_hex(self, hex, map):
        # Replace any preexisting hexes
        replacement = False
        for i, val in enumerate(self.map):
            if val == hex:
                self.map[i] = hex
                replacement = True
        if not replacement: # or add a new one
            self.map.append(hex)
        self.draw_map()
    def rm_hex(self, hex):
        self.map.remove(hex)
        self.draw_map()
    def toggle_hex(self, hex):
        if not self.hex_exists(hex):
            self.add_hex(hex)
        else:
            self.rm_hex(hex)
    def find_moves(self, piece):
        self.highlight = []
        for x in range (-10,10):
            for y in range(-10,10):
                h = Hex(x,y,-x-y)
                a = self.hex_adjacent(h)
                b = self.hex_distance(piece,h) == 3
                c = not self.hex_exists(h)
                if a and c:
                    print(x,y,a,b)
                if a and b and c:
                    self.highlight.append(h)
        self.draw_map()
    def clear_map(self):
        rect = self.L.map_rect
        pg.draw.rect(self.scr, 0, rect)
    def draw_map(self):
        self.clear_map()
        for h in self.map:
            self.draw_hex(h)
        for h in self.highlight:
            self.draw_hex(h, True)

    def gen_map(self, t="parallel", *xargs):
        t = t.lower()
        self.map = []
        if t == "para": # Four args, x1,y1, x2,y2
            for q in range(xargs[0], xargs[1]+1):
                for r in range(xargs[2], xargs[3]):
                    self.map.append(Hex(q, r, -q-r))
        elif t == "vtri": # One arg, height
            for q in range(0, xargs[0]):
                for r in range(0, xargs[0]):
                    self.map.append(Hex(q, r, -q-r))
        elif t == "htri": # One arg, height
            for q in range(0, xargs[0]):
                for r in range(xargs[0]-q, xargs[0]):
                    self.map.append(Hex(q, r, -q-r))
        elif t == "hex": # One arg, radius
            for q in range(-1*xargs[0] + 1, xargs[0]):
                r1 = max(-1*xargs[0], -q - xargs[0])
                r2 = min(xargs[0], -q + xargs[0])
                for r in range(r1 + 1, r2):
                    self.map.append(Hex(q, r, -q-r))
                    if q == 0 and r == 0:
                        self.map[-1].bgcolor = 0x71bab6
        elif t == "rect": # Two args, w,h
            for r in range(0,xargs[1]):
                r_offset = m.floor(r/2)
                for q in range(-r_offset, xargs[0] - r_offset):
                    self.map.append(Hex(q, r, -q-r))
        self.draw_map()
        pg.display.flip()

class Game(object):
    def __init__(self, h, w, name="", size=23):
        self.scr = pg.display.set_mode((h,w))
        pg.display.set_caption(name)
        self.clk = pg.time.Clock()
        s = Point(size,size)
        orient = layout_flat
        origin = Point(h/2, (w-50)/2 + 50)
        self.units = units.units
        self.L = Layout(orient, s, origin, w, h)
        self.M = Map(self.scr, self.L)
        self.Me =Menu(50, w, self.scr, self.units)
        self.Me.draw()
        #M.gen_map("hex", 6)
        #M.draw_map()

        self.mode = 0
        self.playerColor = p['swapl']

    def handle_click(self, pos):
        if pos[1] > 50: # if clicked in hex region
            print("Mode:",hex(self.mode), hex(self.playerColor))
            point = Point(pos[0], pos[1])
            newHex = self.L.pixel_to_hex(point)
            newHex.bgcolor = self.mode
            newHex.fgcolor = self.playerColor
            if self.mode > 0: # Place mode
                self.M.toggle_hex(newHex)
            elif self.mode < 0: # Move mode
                piece = self.M.get_hex(newHex)
                self.M.find_moves(newHex)
        if pos[1] < 50: # if clicked in menu region
            bttn = self.Me.click_button(pos)
            if not bttn:
                return False
            if bttn.mode == 0:
                # Switch Player
                if bttn.selected:
                    self.playerColor = p['swapd']
                else:
                    self.playerColor = p['swapl']
            if bttn.mode == -1:
                self.mode = -1
            else:
                self.mode = bttn.color
