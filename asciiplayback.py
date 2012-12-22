#!/usr/bin/env python2
# asciiplayback.py - Play animations from ASCIImator.net
# Copyright (c) 2012 Clayton G. Hobbs
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pygame
from pygame.locals import *
# I really doubt we need optparse for a program this simple.  sys.argv should
# do just fine.
from sys import exit, argv

# Initialize Pygame
pygame.display.init() 
pygame.font.init()

# Load the animation
am = open(argv[1])

# Create the lists of frame information now
content = []
cparams = []
frinfo = []

# There are different modes for parsing the file
#     meta: read variables
#     content: read frames
#     cparams: read frame lengths and colors
# The initial mode is meta, which not only reads information about the
# animation, but also enters the other modes when appropriate.
parsemode = 'meta'
for line in am:
    ls = line.split()
    # Read information about the animation
    if parsemode == 'meta':
        # Font family
        if ls[0] == 'FFamily':
            ffamily = ls[2][1:-2]
        # Font size
        elif ls[0] == 'FSize':
            fsize = int(ls[2][:-1])
        # Font weight
        elif ls[0] == 'FWeight':
            if ls[2] == 'normal':
                fweight = False
            else:
                fweight = True
        # TODO: Figure out what LH does and implement it
        elif ls[0] == 'LH':
            pass
        # Milliseconds per frame
        elif ls[0] == 'sp':
            sp = int(ls[2][:-1])
        # Should the animation loop ceaselessly?
        elif ls[0] == 'looped':
            if ls[2][0] == 'f':
                looped = False
            else:
                looped = True
        # Width of the animation
        elif ls[0] == 'FrWidth':
            frwidth = int(ls[2][:-1])
        # Height of the animation
        elif ls[0] == 'FrHeight':
            frheight = int(ls[2][:-1])
        # The animation frames follow
        elif ls[0] == 'content':
            parsemode = 'content'
            continue
        elif ls[0] == 'contentParams':
            parsemode = 'cparams'
            continue
    elif parsemode == 'content':
        line = line.strip()
        if line == '];':
            parsemode = 'meta'
            continue
        # If there's no frame on the line, use the frame from last time
        elif line == ',':
            content.append(frame)
        else:
            # Remove the trailing comma (if any), take off the quotes, and
            # strip out the escape sequences
            frame = line.strip(',')[1:-1].decode('string_escape')
            content.append(frame)
    elif parsemode == 'cparams':
        line = line.strip()
        if line == '];':
            parsemode = 'meta'
            continue
        # If there's no frame on the line, use the frame from last time
        elif line == '[,,],':
            cparams.append(frinfo)
        else:
            friold = frinfo
            # Strip off the comma and brackets, then split by the remaining
            # commas and store in a list
            frinfo = line.strip(',')[1:-1].split(',')
            for i in range(3):
                if frinfo[i] == '':
                    frinfo[i] = friold[i]
                else:
                    frinfo[i] = frinfo[i].strip("'")
            frinfo[0] = int(frinfo[0])
            try:
                frinfo[1] = pygame.Color(frinfo[1])
            except ValueError:
                # This probably means it's already a pygame.Color, so there's
                # no need to worry
                pass
            try:
                frinfo[2] = pygame.Color(frinfo[2])
            except ValueError:
                # This probably means it's already a pygame.Color, so there's
                # no need to worry
                pass
            cparams.append(frinfo)

font = pygame.font.SysFont('DejaVu Sans Mono', fsize, fweight)
fht = font.get_height()

# TODO: Be smart and figure out what these should really be after loading the
# ASCIImation
width = 640
height = 480

# Make the display surface
screen = pygame.display.set_mode((width, height), 0, 32)

# Timekeeping
frame = 0

# Main playback loop
# TODO: Make controls and input handling to operate them
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill(cparams[frame][2])

    fline = 0
    for line in content[frame].split('\n'):
        screen.blit(font.render(line, True, cparams[frame][1],
                    cparams[frame][2]), (0, fline*fht))
        fline += 1

    pygame.display.update()

    pygame.time.delay(sp * cparams[frame][0])
    frame += 1
