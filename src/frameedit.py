from gi.repository import Gtk, Pango

class FrameEdit(Gtk.FlowBoxChild):
    def __init__(self):
        Gtk.FlowBoxChild.__init__(self)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.textview = Gtk.TextView()
        self.buffer = self.textview.get_buffer()
        self.buffer.set_text(":v")
        self.buffer.connect("changed", self.changed)
        self.textview.connect("button-press-event", self.focus)
        self.textview.override_font(Pango.FontDescription.from_string("monospace"))
        self.vbox.pack_start(self.textview, True, True, 0)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox.pack_start(Gtk.Label(self.get_index()), False, False, 0)
        self.hbox.pack_end(Gtk.SpinButton(), False, False, 0)
        self.vbox.pack_end(self.hbox, False, False, 0)

        self.add(self.vbox)

    def changed(self, buffer):
        print(buffer.props.text)

    def focus(self, lel, lel2):
        self.get_parent().select_child(self)
