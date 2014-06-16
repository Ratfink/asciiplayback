from gi.repository import Gtk, Gio, Gdk, GObject
from asciiplayback import *
from asciimation import *

class GtkASCIIPlayer(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        labelbox = Gtk.Box()
        label = Gtk.Label()
        label.set_alignment(0, 0)
        label.set_width_chars(self.player.asciimation.size[0])
        label.set_max_width_chars(self.player.asciimation.size[0])
        labelbox.pack_start(label, True, False, 0)
        self.pack_start(labelbox, True, False, 0)
#TODO        self.do_animate(label)

        ab = Gtk.ActionBar()

        ab_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(ab_buttons.get_style_context(), "linked")

        btn_previous = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                  name="media-skip-backward-symbolic"),
                                  Gtk.IconSize.BUTTON))
#TODO        btn_previous.connect("clicked", self.do_previous)
        ab_buttons.add(btn_previous)

        btn_rewind = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                name="media-seek-backward-symbolic"),
                                Gtk.IconSize.BUTTON))
#TODO        btn_rewind.connect("clicked", self.do_rewind)
        ab_buttons.add(btn_rewind)

        btn_play = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                              name="media-playback-pause-symbolic"),
                              Gtk.IconSize.BUTTON))
#TODO        btn_play.connect("clicked", self.do_play)
        ab_buttons.add(btn_play)

        btn_forward = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                 name="media-seek-forward-symbolic"),
                                 Gtk.IconSize.BUTTON))
#TODO        btn_forward.connect("clicked", self.do_forward)
        ab_buttons.add(btn_forward)

        btn_next = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                              name="media-skip-forward-symbolic"),
                              Gtk.IconSize.BUTTON))
#TODO        btn_next.connect("clicked", self.do_next)
        ab_buttons.add(btn_next)

        ab.set_center_widget(ab_buttons)
        self.pack_end(ab, False, False, 0)
