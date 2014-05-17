import codecs
import json
from asciimation import *

class ASCIIPlayback(object):
    def __init__(self, filename):
        # Open and load the file
        f = codecs.open(filename, 'rb', 'utf-8')
        data = json.load(f)
        f.close()

        # Create the ASCIImation object
        self.asciimation = ASCIImation(
            font_family=data["style"]["family"],
            font_size=data["style"]["size"],
            font_bold=True if data["style"]["weight"]=="bold" else False,
            speed=data["speed"],
            looped=data["loop"],
            size=[data["width"], data["height"]]
        )

        # Add all the frames
        text = ""
        repeat = 1
        foreground_color = "#000000"
        background_color = "#ffffff"
        for frame in data["content"]:
            if "text" in frame:
                text = frame["text"]
            if "repeat" in frame:
                repeat = frame["repeat"]
            if "fontColor" in frame:
                foreground_color = str(frame["fontColor"])
            if "backgroundColor" in frame:
                background_color = str(frame["backgroundColor"])
            self.asciimation.frames.append(Frame(
                text=text,
                repeat=repeat,
                foreground_color=foreground_color,
                background_color=background_color
            ))

        self.current_frame = 0
        self.speed = 1
        self._last_speed = 1


    def next_frame(self):
        if self.current_frame >= len(self.asciimation):
            if self.asciimation.looped:
                self.current_frame = \
                    self.current_frame % (len(self.asciimation) - 1)
            else:
                self.current_frame = len(self.asciimation) - 1
                self.speed = 0
        elif self.current_frame < 0:
            if self.asciimation.looped:
                self.current_frame = len(self.asciimation) - 1 - \
                    -self.current_frame % (len(self.asciimation) - 1)
            else:
                self.current_frame = 0
                self.speed = 0
        else:
            self.current_frame += self.speed
        return self.asciimation[int(self.current_frame-self.speed) % \
                                len(self.asciimation)]

    def restart(self):
        self.current_frame = 0
        self.speed = 1

    def toggle_playing(self):
        if self.speed == 0:
            self.speed = 1
        else:
            self.speed = 0

    def rewind(self):
        if self.speed > -2:
            if self.speed == 1 or self.speed == -1:
                self._last_speed = self.speed
            self.speed = -2
        elif self.speed > -4:
            self.speed = -4
        elif self.speed > -8:
            self.speed = -8
        else:
            self.speed = self._last_speed
            self.last_speed = 0

    def fast_forward(self):
        if self.speed < 2:
            if self.speed == 1 or self.speed == -1:
                self._last_speed = self.speed
            self.speed = 2
        elif self.speed < 4:
            self.speed = 4
        elif self.speed < 8:
            self.speed = 8
        else:
            self.speed = self._last_speed
            self.last_speed = 0
