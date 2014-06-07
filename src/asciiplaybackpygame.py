#!/usr/bin/env python2

import pygame
from pygame.locals import *
from sys import exit, argv
import codecs
from asciiplayback import *

class ASCIIPlaybackPygame(object):
    def __init__(self):
        # Initialize Pygame
        pygame.display.init() 
        pygame.font.init()

        # Load the ASCIImation
        self.player = ASCIIPlayback(filename=argv[1])
        self.update_font()

        self.size = (
            int(self.font.size('M'*self.player.asciimation.size[0])[0]) + 2,
            int(self.font.get_height()*self.player.asciimation.size[1]) + 2
        )

        self.screen = pygame.display.set_mode(self.size, RESIZABLE)

        cross_strings = (
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "XXXXXXX.XXXXXXXX",
            ".......X........",
            "XXXXXXX.XXXXXXXX",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      X.X       ",
            "      XXX       ",
        )
        self.cursor = pygame.cursors.compile(cross_strings)
        pygame.mouse.set_cursor((16, 16), (7, 7), *self.cursor)

    def update_font(self):
        fontpath = pygame.font.match_font(''.join(
            self.player.asciimation.font_family.split(' ')),
            bold=self.player.asciimation.font_bold)
        self.font = pygame.font.Font(fontpath,
            self.player.asciimation.font_size)

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.restart()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        exit()
                    elif event.key == K_SPACE:
                        self.player.toggle_playing()
                    elif event.key == K_PAGEUP or event.key == K_KP9:
                        self.player.rewind()
                    elif event.key == K_PAGEDOWN or event.key == K_KP3:
                        self.player.fast_forward()

            current_frame = self.player.next_frame()

            self.screen.fill(pygame.Color(current_frame.background_color))

            fline = 0
            chpos = 0
            for char in current_frame.text:
                if char == "\n":
                    fline += 1
                    chpos = 0
                else:
                    self.screen.blit(
                        self.font.render(char, True,
                            pygame.Color(current_frame.foreground_color),
                            pygame.Color(current_frame.background_color)),
                        (
                            chpos*self.font.size("M")[0] + 1,
                            fline*self.font.get_height() + 1
                        )
                    )
                    chpos += 1

            pygame.display.update()
            pygame.time.delay(int(self.player.asciimation.speed))

if __name__ == "__main__":
    player = ASCIIPlaybackPygame()
    player.play()
