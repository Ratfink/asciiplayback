#!/usr/bin/env python
import sys
from gi.repository import Gtk, Gio, Gdk, GObject
from asciiplayback import *

class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ASCIIPlayback")
        self.set_default_size(400, 200)

        self.player = ASCIIPlayback(filename=sys.argv[1])

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        labelbox = Gtk.Box()
        label = Gtk.Label()
        label.set_alignment(0, 0)
        label.set_width_chars(self.player.asciimation.size[0])
        labelbox.pack_start(label, True, True, 0)
        box.pack_start(labelbox, True, True, 0)
        self.do_animate(label)

        ab = Gtk.ActionBar()

        ab_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(ab_buttons.get_style_context(), "linked")

        btn_previous = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_MEDIA_PREVIOUS))
        btn_previous.connect("clicked", self.do_previous)
        ab_buttons.add(btn_previous)

        btn_rewind = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_MEDIA_REWIND))
        btn_rewind.connect("clicked", self.do_rewind)
        ab_buttons.add(btn_rewind)

        btn_play = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE))
        btn_play.connect("clicked", self.do_play)
        ab_buttons.add(btn_play)

        btn_forward = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_MEDIA_FORWARD))
        btn_forward.connect("clicked", self.do_forward)
        ab_buttons.add(btn_forward)

        btn_next = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_MEDIA_NEXT))
        btn_next.connect("clicked", self.do_next)
        ab_buttons.add(btn_next)

        ab.set_center_widget(ab_buttons)
        box.pack_end(ab, False, False, 0)

        self.add(box)

    def do_animate(self, widget):
        asciiframe = self.player.next_frame()
        widget.set_markup('<span size="{0}" background="{1}" foreground="{2}"\
 font_family="{3},monospace">{4}</span>'.format(self.player.asciimation.font_size*1024,
                          asciiframe.background_color, asciiframe.foreground_color,
                          self.player.asciimation.font_family, asciiframe.text))
        widget.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse(asciiframe.background_color)[1])

        GObject.timeout_add(self.player.asciimation.speed, self.do_animate, widget)

    def do_previous(self, button):
        self.player.restart()

    def do_rewind(self, button):
        self.player.rewind()

    def do_play(self, button):
        self.player.toggle_playing()
        if self.player.speed == 0:
            button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY))
        else:
            button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE))

    def do_forward(self, button):
        self.player.fast_forward()

    def do_next(self, button):
        pass

win = HeaderBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
