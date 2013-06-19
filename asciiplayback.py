#!/usr/bin/env python2
# asciiplayback.py - Play animations from ASCIImator.net
# Copyright (c) 2012-2013 Clayton G. Hobbs
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
import codecs

# Initialize Pygame
pygame.display.init() 
pygame.font.init()

# If you want to play a file called '-h' or '--help', use ./ before its name
if argv[1] == '-h' or argv[1] == '--help':
    print 'asciiplayback.py - Play animations from ASCIImator.net'
    print 'Usage: %s [filename]' % argv[0]
    exit()
# Load the animation
am = codecs.open(argv[1], 'rb', 'utf-8')

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
        # TODO: Use ffamily instead of always choosing one font.
        if ls[0] == 'FFamily':
            ffamily = ls[2][1:-2]
        # Font size
        elif ls[0] == 'FSize':
            fsize = int(ls[2][:-1])
        # Font weight
        elif ls[0] == 'FWeight':
            if ls[2][1:-2] == 'normal':
                fweight = False
            else:
                fweight = True
        # Line height
        # TODO: Figure out why it's better to force lheight to 1.
        elif ls[0] == 'LH':
            lheight = 1.
            #lheight = int(ls[2][1:-3]) / 100.
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
            frame = line.strip(',')[1:-1].encode('utf-8').decode('string-escape').decode('utf-8')
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
                frinfo[1] = pygame.Color(str(frinfo[1]))
            except ValueError:
                # This probably means it's already a pygame.Color, so there's
                # no need to worry
                pass
            try:
                frinfo[2] = pygame.Color(str(frinfo[2]))
            except ValueError:
                # This probably means it's already a pygame.Color, so there's
                # no need to worry
                pass
            cparams.append(frinfo)

font = pygame.font.SysFont('DejaVu Sans Mono', fsize, fweight)
fht = font.get_height()
fwd = font.size('M'*frwidth)[0]/float(frwidth)

width = int(fwd*frwidth) + 2
height = int(fht*lheight*frheight) + 2

# Make the display surface
screen = pygame.display.set_mode((width, height), 0, 32)

# Timekeeping
frame = 0
subframe = 0

animend = len(content) - 1
playing = True
wasplaying = True
forward = True
spfactor = 1.0

# Main playback loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            # ESC: quit
            if event.key == K_ESCAPE:
                exit()
            # Space: Pause/play
            if event.key == K_SPACE:
                playing = not playing
            # Left: Step backward
            if (event.key == K_LEFT or event.key == K_KP4) and frame > 0:
                frame -= 1
                subframe = 0
            # Right: Step forward
            if (event.key == K_RIGHT or event.key == K_KP6) and \
               frame < animend:
                frame += 1
                subframe = 0
            # Home: Skip to beginning
            if event.key == K_HOME or event.key == K_KP7:
                frame = 0
                subframe = 0
            # End: Skip to end
            if event.key == K_END or event.key == K_KP1:
                frame = animend
                subframe = 0
            # Page Up: Rewind
            if event.key == K_PAGEUP or event.key == K_KP9:
                forward = False
                wasplaying = playing
                playing = True
                spfactor = 0.5
            # Page Down: Fast-forward
            if event.key == K_PAGEDOWN or event.key == K_KP3:
                forward = True
                wasplaying = playing
                playing = True
                spfactor = 0.5
            # L: toggle loop
            if event.key == K_l:
                looped = not looped
                if looped and frame == animend and not playing:
                    playing = True
        if event.type == KEYUP:
            # Page Up: Rewind
            if event.key == K_PAGEUP or event.key == K_KP9:
                forward = True
                playing = wasplaying
                spfactor = 1.0
            # Page Down: Fast-forward
            if event.key == K_PAGEDOWN or event.key == K_KP3:
                forward = True
                playing = wasplaying
                spfactor = 1.0

    # Draw the current frame
    screen.fill(cparams[frame][2])

    fline = 0
    for line in content[frame].split('\n'):
        screen.blit(font.render(line, True, cparams[frame][1],
                    cparams[frame][2]), (1, fline*fht*lheight + 1))
        fline += 1

    pygame.display.update()

    # Delay regardless of playing status so we don't use 100% of the CPU time
    # while paused
    pygame.time.delay(int(sp*spfactor))

    # If playing, play in the appropriate direction.
    if playing:
        subframe += 1 if forward else -1
        if subframe >= cparams[frame][0] or subframe < 0:
            if frame < animend and forward:
                frame += 1
            elif frame > 0 and not forward:
                frame -= 1
            elif looped:
                frame = 0 if forward else animend
            else:
                playing = False
            subframe = 0 if forward else cparams[frame][0] - 1
