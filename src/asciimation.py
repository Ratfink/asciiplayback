class ASCIImation(object):
    def __init__(self, font_family="courier new", font_size=12,
                 font_bold=False, speed=500, looped=True, size=[20, 10]):
        self.font_family = font_family
        self.font_size = font_size
        self.font_bold = font_bold
        self.speed = speed
        self.looped = looped
        self.size = size
        self.frames = []

    def __getitem__(self, key):
        if key < 0 or key > len(self):
            raise IndexError("Index outside length of ASCIImation")
        current_frame = 0
        while key >= self.frames[current_frame].duration:
            key -= self.frames[current_frame].duration
            current_frame += 1
        return self.frames[current_frame]

    def __len__(self):
        length = 0
        for f in self.frames:
            length += f.duration
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
    def __init__(self, text="", duration=1, foreground_color="#000000",
                 background_color="#ffffff"):
        self.text = text
        self.duration = duration
        self.foreground_color = foreground_color
        self.background_color = background_color

    def __str__(self):
        s = "duration: {0}\n".format(self.duration)
        s += "foreground_color: {0}\n".format(self.foreground_color)
        s += "background_color: {0}\n".format(self.background_color)
        s += self.text
        return s
