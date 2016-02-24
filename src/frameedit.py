from gi.repository import Gtk, Pango

class FrameEdit(Gtk.FlowBoxChild):
    def __init__(self):
        Gtk.FlowBoxChild.__init__(self)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.textview = Gtk.TextView()
        self.buffer = self.textview.get_buffer()
        self.buffer.set_text(":v")
        self.buffer.connect("changed", self.changed)
        self.textview.connect("button-press-event", self.focus)
        self.font = Pango.FontDescription.from_string("dejavu sans mono 12")
        self.textview.override_font(self.font)
        self.scrolledwindow.add(self.textview)

        # Set the ScrolledWindow large enough to show the whole frame
        context = self.textview.get_pango_context()
        metrics = context.get_metrics(self.font)
        width = 20 * metrics.get_approximate_digit_width() / Pango.SCALE + 1
        height = 10 * (metrics.get_ascent() + metrics.get_descent()) / Pango.SCALE
        self.scrolledwindow.set_size_request(width, height)

        # Add the ScrolledWindow
        self.hbox.pack_start(self.scrolledwindow, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.pack_start(Gtk.Label(self.get_index()), False, False, 0)
        self.hbox.pack_end(Gtk.SpinButton(), False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

        self.add(self.vbox)

    def changed(self, buffer):
        print(buffer.props.text)

    def focus(self, lel, lel2):
        self.get_parent().select_child(self)
