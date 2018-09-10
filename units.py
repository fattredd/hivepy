# Unit classes
import config

p = config.p

class Unit(object):
    def __init__(self, name, color, mode):
        self.name = name
        self.color = color
        self.mode = mode
        self.speed = []

units = [
    Unit("Move", p['u0'], -1), #Special
    Unit("Queen", p['u1'], 1),
    Unit("Ant", p['u2'], 2),
    Unit("Spider", p['u4'], 4),
    Unit("Beetle", p['u5'], 5),
    Unit("Grasshopper", p['u3'], 3)
    ]
