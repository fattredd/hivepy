# Hive Classes
import math as m

class Hex(object):
    hex_directions = [
        Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1),
        Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)
    ]
    
    def __init__(self, q,r,s):
        assert(q+r+s == 0)
        self.loc = (q,r,s)

    def length(self, hex):
        return int((m.abs(hex.q) + m.abs(hex.r) + m.abs(hex.s)) / 2)
    def distance(self, a, b):
        return length(a-b)
    def direction(direction):
        return hex_directions[direction % 6]
    def neighbor(hex, direc):
        return hex + direction(direc)
        
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


class Map(object):
    pass

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
                          0.0, -1.0 / 3.0, sqrt(3.0) / 3.0, 0.0)
class Point(object):
    def __init__(self, x, y):
        self.x = x * 1.0
        self.y = y * 1.0

class Layout(object):
    def __init__(self, orient, size, origin):
        self.orientation = orient
        self.size = size
        self.origin = origin
    
            
