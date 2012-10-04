#!/usr/bin/env python

from __future__ import division

import itertools
import pickle
import sys

import Image

def get_color(value):
    v = int(value * 255)
    if value > 0.9:
        return (255, 51, 204) # violet
    elif value > 0.8:
        return (255, 204, 0) # gold
    elif value > 0.7:
        return (255, 255, 204) # silver
    elif value > 0.6:
        return (v, 255, v) # greens
    elif value > 0.4:
        return (204, v + 51, v + 51) # reds
    elif value > 0.2:
        return (v + 102, v + 51, 102) # blues
    elif value > 0.05:
        return (v + 51, v + 51, v + 51) # grays
    else:
        return (0, 0, 0) # blacks

def fair_color(value):
    v = int(value * 768)
    r = max(v - 512, 0)
    g = min(255, v)
    b = min(255, max(v - 256, 0))

    return (r, g, b)

filenames = sys.argv[1:]

pixel_arrays = []

for filename in filenames:
    pixels = pickle.load(open(filename, "r"))
    WIDTH, HEIGHT = len(pixels), len(pixels[0])
    print "Loaded %dx%d array of values!" % (WIDTH, HEIGHT)
    pixel_arrays.append(pixels)

pixels = pixel_arrays[0]

out = Image.new("RGB",(WIDTH, HEIGHT))

maxdepth = 0

print "Calculating max depth..."

maxdepth = max(max(j for j in i) for i in pixels)

print "Max depth is %d" % maxdepth

for (i, j) in itertools.product(xrange(WIDTH), xrange(HEIGHT)):
    value = pixels[i][j] / maxdepth
    #out.putpixel((i, j), get_color(value))
    out.putpixel((i, j), fair_color(value))

print "Resampling..."

out = out.resize((WIDTH//2, HEIGHT//2), Image.ANTIALIAS)
out.save("buddha.png")
