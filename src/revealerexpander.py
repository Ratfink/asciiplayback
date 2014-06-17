from gi.repository import Gtk

class RevealerExpander(Gtk.Box):
    def __init__(self, mnemonic):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.button = Gtk.ToggleButton.new_with_mnemonic(mnemonic)
        self.button.connect("toggled", self.do_expand)

        self.revealer = Gtk.Revealer()

        self.pack_start(self.button, False, False, 0)
        self.pack_start(self.revealer, True, True, 0)

    def add(self, widget):
        self.revealer.add(widget)

    def do_expand(self, button):
        self.set_expanded(button.get_active())

    def set_expanded(self, expanded):
        self.revealer.set_reveal_child(expanded)
        self.button.set_active(expanded)
