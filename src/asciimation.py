import codecs
import json

class ASCIImation(object):
    def __init__(self, font_family="courier new", font_size=12,
                 font_bold=False, speed=500, looped=True, size=[20, 10],
                 filename=None):
        if filename is None:
            self.font_family = font_family
            self.font_size = font_size
            self.font_bold = font_bold
            self.speed = speed
            self.looped = looped
            self.size = size
            self.frames = []
        else:
            # Open and load the file
            f = codecs.open(filename, 'rb', 'utf-8')
            data = json.load(f)
            f.close()

            # Get properties of the ASCIImation
            self.font_family = data["style"]["family"]
            self.font_size = data["style"]["size"]
            self.font_bold = True if data["style"]["weight"] == "bold" else False
            self.speed = data["speed"]
            self.looped = data["loop"]
            self.size = [data["width"], data["height"]]
            self.frames = []

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
                self.frames.append(Frame(
                    text=text,
                    repeat=repeat,
                    foreground_color=foreground_color,
                    background_color=background_color
                ))

    def __getitem__(self, key):
        if key < 0 or key > len(self):
            raise IndexError("Index outside length of ASCIImation")
        current_frame = 0
        while key >= self.frames[current_frame].repeat:
            key -= self.frames[current_frame].repeat
            current_frame += 1
        return self.frames[current_frame]

    def __len__(self):
        length = 0
        for f in self.frames:
            length += f.repeat
        return length

    def __str__(self):
        s = "font_family: {0}\n".format(self.font_family)
        s += "font_size: {0}\n".format(self.font_size)
        s += "font_bold: {0}\n".format(self.font_bold)
        s += "speed: {0}\n".format(self.speed)
        s += "looped: {0}\n".format(self.looped)
        s += "size: {0}".format(self.size)
        return s

class Frame(object):
    def __init__(self, text="", repeat=1, foreground_color="#000000",
                 background_color="#ffffff"):
        self.text = text
        self.repeat = repeat
        self.foreground_color = foreground_color
        self.background_color = background_color

    def __str__(self):
        s = "repeat: {0}\n".format(self.repeat)
        s += "foreground_color: {0}\n".format(self.foreground_color)
        s += "background_color: {0}\n".format(self.background_color)
        s += self.text
        return s
