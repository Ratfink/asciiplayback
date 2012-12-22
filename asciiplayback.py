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

# TODO: Be smart and figure out what these should really be after loading the
# ASCIImation
width = 640
height = 480

# Make the display surface
screen = pygame.display.set_mode((width, height), 0, 32)

# Main playback loop
# TODO: Make controls and input handling to operate them
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
