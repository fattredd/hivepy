# Hive Classes
import math as m
import pygame as pg

debug = True

class Hex(object):
    def __init__(self, q,r,s):
        assert(q+r+s == 0)
        self.loc = (q,r,s)
        self.q = q
        self.r = r
        self.s = s
        self.bgcolor = 0x00FFF0
        self.fgcolor = 0xFFFFFF
    
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
        if isInstance(other, Hex):
            return self.loc == other.loc
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
    def __eq__(self, other):
        if isInstance(other, Hex):
            return self.loc == other.loc
        return false
    def __ne__(self, other):
        return not self.__eq__(other)    


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
    def __init__(self, orient, size, origin):
        self.orientation = orient
        self.size = size
        self.origin = origin
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
        return FactionalHex(q, r, -q - r)
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
    
hex_directions = [
    Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1),
    Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
        

# Standalone Functions:

def length(self, hex):
    return int((m.abs(hex.q) + m.abs(hex.r) + m.abs(hex.s)) / 2)

def distance(self, a, b):
    return length(a-b)

def direction(direction):
    return self.hex_directions[direction % 6]

def neighbor(hex, direc):
    return hex + direction(direc)

def FractionalHex(q, r, s):
    q_ = round(q)
    r_ = round(r)
    s_ = round(s)
    q_diff = m.abs(q_ - q)
    r_diff = m.abs(r_ - r)
    s_diff = m.abs(r_ - r)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r -s
    elif r_diff > s_diff:
        s = -q -r
    return Hex(q, r, s)

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
        self.map = [
            Hex(0,0,0),
            Hex(1,-1,0),
            Hex(-1,1,0),
            Hex(0,1,-1),
            Hex(0,-1,1)
        ]
        self.fnt = pg.font.SysFont('freemono', 12)
    def draw_hex(self, hex):
        ptl = self.L.polygon_corners(hex)
        #pg.draw.polygon(self.scr, hex.bgcolor, ptl)
        pg.draw.polygon(self.scr, hex.fgcolor, ptl, 1)
        if debug:
            ct = "{},{}".format(hex.q, hex.r)
            s = self.fnt.size(ct)
            txt = self.fnt.render(ct, True, (255,255,0))
            loc = self.L.hex_to_pixel(hex).l()
            loc[0] = loc[0] - int(s[0]/2)
            loc[1] = loc[1] - int(s[1]/2)
            self.scr.blit(txt, loc)
            
    def draw_map(self):
        for h in self.map:
            self.draw_hex(h)

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
                        self.map[-1].bgcolor = 0xFF0000
        elif t == "rect": # Two args, w,h
            for r in range(0,xargs[1]):
                r_offset = m.floor(r/2)
                for q in range(-r_offset, xargs[0] - r_offset):
                    self.map.append(Hex(q, r, -q-r))
        self.draw_map()
        pg.display.flip()
