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
        self.player = ASCIIPlayback(argv[1])


    def set_font(self):
        fontpath = pygame.font.match_font(''.join(
            self.player.asciimation.font_family.split(' ')),
            bold=self.player.asciimation.font_bold)
        self.font = pygame.font.Font(fontpath,
            self.player.asciimation.font_size)

    def play(self):
        pass

if __name__ == "__main__":
    player = ASCIIPlaybackPygame()
    player.play()
