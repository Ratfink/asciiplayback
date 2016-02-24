#!/usr/bin/env python
import os.path
import sys

from gi.repository import Gtk, Gio, Gdk, GObject

from asciiplayback import *
from asciimation import *
from gtkasciiplayer import *

class ASCIIPlaybackGtk(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ASCIIPlayback")
        self.set_default_size(0, 0)

        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
            self.player = ASCIIPlayback(ASCIImation(filename=self.filename))
        else:
            self.filename = ""
            blank_asciimation = ASCIImation(font_family='monospace', size=[19, 3])
            blank_asciimation.frames.append(Frame(text='\n  No file loaded!  \n'))
            self.player = ASCIIPlayback(asciimation=blank_asciimation)

        self.hb = Gtk.HeaderBar()
        self.update_headerbar()

        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="document-open-symbolic"),
                            Gtk.IconSize.BUTTON))
        button.connect("clicked", self.do_open)
        self.hb.pack_start(button)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.video = GtkASCIIPlayer(self.player)
        box.pack_start(self.video, True, True, 0)

        ab = Gtk.ActionBar()

        self.controls = GtkASCIIControls(self.player)
        ab.set_center_widget(self.controls)
        box.pack_end(ab, False, False, 0)

        self.add(box)

    def do_open(self, button):
        dialog = Gtk.FileChooserDialog("Open", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.player = ASCIIPlayback(ASCIImation(filename=self.filename))
            self.video.player = self.player
            self.controls.player = self.player
            self.update_headerbar()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def add_filters(self, dialog):
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("All files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def update_headerbar(self):
        self.hb.props.show_close_button = True
        self.hb.props.title = "ASCIIPlayback"
        self.hb.props.subtitle = os.path.basename(self.filename)
        self.hb.props.has_subtitle = True
        self.set_titlebar(self.hb)

def run():
    win = ASCIIPlaybackGtk()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    run()
