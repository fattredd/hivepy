# Config

settings = {
    'coords': True,
    'outline': True,
    'colorPallet': 0,
    }


c = [] # Color dict
c.append({ #Primary
    "black": 0x000000,
    "white": 0xffffff,
    "selected": 0xc0c0c0,
    "swapl": 0xc0c5c1,
    "swapd": 0x343633,
    "u0"   : 0xdadafa, # Move
    "u1"   : 0xaf9b46, # yellow
    "u2"   : 0x003049, # blue
    "u3"   : 0x70a288, # green
    "u4"   : 0x4f3824, # brown
    "u5"   : 0x725ac1, # purple
    "h0"   : 0x55cc55, # highlight fg
    "h1"   : 0x00cc00  # highlight bg
    })




p = c[settings['colorPallet']] # Pallet
