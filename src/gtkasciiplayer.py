from gi.repository import Gtk, Gio, Gdk, GObject, Pango
from asciiplayback import *
from asciimation import *

class GtkASCIIPlayer(Gtk.Box):
    def __init__(self, player):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.player = player

        labelbox = Gtk.Box()
        label = Gtk.Label()
        label.set_alignment(0, 0)
        label.set_width_chars(self.player.asciimation.size[0])
        label.set_max_width_chars(self.player.asciimation.size[0])
        labelbox.pack_start(label, True, False, 0)
        self.pack_start(labelbox, True, False, 0)
        self.do_animate(label)

    def do_animate(self, widget):
        asciiframe = self.player.next_frame()

        # Process the string to make each line the correct length, and ensure
        # that there is exactly the right number of lines.  Perhaps this
        # should be somewhere in the model code...
        text = []
        for line in asciiframe.text.split('\n'):
            text.append("{{: <{}s}}".format(self.player.asciimation.size[0]).format(line))
            text[-1] = text[-1][:self.player.asciimation.size[0]]
        while len(text) < self.player.asciimation.size[1]:
            text.append(' '*self.player.asciimation.size[0])
        text = '\n'.join(text[:self.player.asciimation.size[1]])

        # Draw the string and background
        widget.set_markup('<span size="{0}" foreground="{1}"\
 font_family="{2},monospace">{3}</span>'.format(self.player.asciimation.font_size*Pango.SCALE,
                          asciiframe.foreground_color,
                          self.player.asciimation.font_family, text))
        widget.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse(asciiframe.background_color)[1])

        GObject.timeout_add(self.player.asciimation.speed, self.do_animate, widget)

class GtkASCIIControls(Gtk.Box):
    def __init__(self, player):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.get_style_context(), "linked")

        self.player = player

        btn_previous = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                  name="media-skip-backward-symbolic"),
                                  Gtk.IconSize.BUTTON))
        btn_previous.connect("clicked", self.do_previous)
        self.add(btn_previous)

        btn_rewind = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                name="media-seek-backward-symbolic"),
                                Gtk.IconSize.BUTTON))
        btn_rewind.connect("clicked", self.do_rewind)
        self.add(btn_rewind)

        self.btn_play = Gtk.Button()
        self.set_play_button_icon()
        self.btn_play.connect("clicked", self.do_play)
        self.add(self.btn_play)

        btn_forward = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                 name="media-seek-forward-symbolic"),
                                 Gtk.IconSize.BUTTON))
        btn_forward.connect("clicked", self.do_forward)
        self.add(btn_forward)

        btn_next = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                              name="media-skip-forward-symbolic"),
                              Gtk.IconSize.BUTTON))
        btn_next.connect("clicked", self.do_next)
        self.add(btn_next)

    def do_previous(self, button):
        self.player.to_start()
        self.set_play_button_icon()

    def do_rewind(self, button):
        self.player.rewind()
        self.set_play_button_icon()

    def do_play(self, button):
        self.player.toggle_playing()
        self.set_play_button_icon()

    def do_forward(self, button):
        self.player.fast_forward()
        self.set_play_button_icon()

    def do_next(self, button):
        self.player.to_end()
        self.set_play_button_icon()

    def set_play_button_icon(self):
        if self.player.speed == 0:
            self.btn_play.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON))
        else:
            self.btn_play.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                name="media-playback-pause-symbolic"), Gtk.IconSize.BUTTON))
