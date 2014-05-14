import codecs
from asciimation import *

class ASCIIPlayback(object):
    def __init__(self, filename):
        f = codecs.open(filename, 'rb', 'utf-8')

        self.asciimation = ASCIImation()
        self.current_frame = 0

        # Parse the ASCIImation file.
        # There are different modes for parsing the file:
        #     meta: read variables
        #     content: read frames
        #     cparams: read frame lengths and colors
        # The initial mode is meta, which not only reads information about the
        # animation, but also enters the other modes when appropriate.
        parsemode = 'meta'
        paramcounter = 0
        frinfo = []
        for line in f:
            ls = line.split()
            # Read information about the animation
            if parsemode == 'meta':
                # Font family
                # TODO: Use ffamily instead of always choosing one font.
                if ls[0] == 'FFamily':
                    self.asciimation.font_family = ' '.join(ls[2:])[1:-2]
                # Font size
                elif ls[0] == 'FSize':
                    self.asciimation.font_size = int(ls[2][:-1])
                # Font weight
                elif ls[0] == 'FWeight':
                    if ls[2][1:-2] == 'normal':
                        self.asciimation.font_bold = False
                    else:
                        self.asciimation.font_bold = True
                # Line height
                # TODO: Figure out why it's better to force lheight to 1.
                # elif ls[0] == 'LH':
                #     lheight = 1.
                #     #lheight = int(ls[2][1:-3]) / 100.
                # Milliseconds per frame
                elif ls[0] == 'sp':
                    self.asciimation.speed = int(ls[2][:-1])
                # Should the animation loop ceaselessly?
                elif ls[0] == 'looped':
                    if ls[2][0] == 'f':
                        self.asciimation.looped = False
                    else:
                        self.asciimation.looped = True
                # Width of the animation
                elif ls[0] == 'FrWidth':
                    self.asciimation.size[0] = int(ls[2][:-1])
                # Height of the animation
                elif ls[0] == 'FrHeight':
                    self.asciimation.size[1] = int(ls[2][:-1])
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
                    self.asciimation.frames.append(Frame(text=frame))
                else:
                    # Remove the trailing comma (if any), take off the quotes,
                    # and strip out the escape sequences
                    frame = line.strip(',')[1:-1].encode('utf-8').decode(
                        'string-escape').decode('utf-8')
                    self.asciimation.frames.append(Frame(text=frame))
            elif parsemode == 'cparams':
                line = line.strip()
                if line == '];':
                    parsemode = 'meta'
                    continue
                # If there's no frame on the line, use the frame from last time
                elif line == '[,,],':
                    self.asciimation.frames[paramcounter].duration = frinfo[0]
                    self.asciimation.frames[paramcounter].foreground_color = \
                        frinfo[1]
                    self.asciimation.frames[paramcounter].background_color = \
                        frinfo[2]
                else:
                    friold = frinfo
                    # Strip off the comma and brackets, then split by the
                    # remaining commas and store in a list
                    frinfo = line.strip(',')[1:-1].split(',')
                    for i in range(3):
                        if frinfo[i] == '':
                            frinfo[i] = friold[i]
                        else:
                            frinfo[i] = frinfo[i].strip("'")
                    frinfo[0] = int(frinfo[0])
                    frinfo[1] = str(frinfo[1])
                    frinfo[2] = str(frinfo[2])
                    self.asciimation.frames[paramcounter].duration = frinfo[0]
                    self.asciimation.frames[paramcounter].foreground_color = \
                        frinfo[1]
                    self.asciimation.frames[paramcounter].background_color = \
                        frinfo[2]
                paramcounter += 1
        f.close()

    def next_frame(self):
        if self.current_frame == len(self.asciimation):
            if self.asciimation.looped:
                self.current_frame = 1
            else:
                raise IndexError("End of ASCIImation reached.")
        else:
            self.current_frame += 1
        return self.asciimation[self.current_frame - 1]

    def prev_frame(self):
        if self.current_frame == -1:
            if self.asciimation.looped:
                self.current_frame = len(self.asciimation) - 2
            else:
                raise IndexError("Start of ASCIImation reached.")
        else:
            self.current_frame -= 1
        return self.asciimation[self.current_frame + 1]

    def restart(self):
        self.current_frame = 0
