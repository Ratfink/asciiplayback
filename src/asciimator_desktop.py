#!/usr/bin/env python
import sys
from gi.repository import Gtk, Gio, Gdk, GObject
from asciiplayback import *

class ASCIImatorDesktop(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ASCIImator Desktop")
        self.set_default_size(400, 200)

        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
            self.player = ASCIIPlayback(filename=self.filename, speed=0)
        else:
            self.filename = ""
            blank_asciimation = ASCIImation(font_family='monospace', size=[15, 3])
            blank_asciimation.frames.append(Frame(text='\nNo file loaded!\n'))
            self.player = ASCIIPlayback(asciimation=blank_asciimation, speed=0)

#        print('\n'.join(Gtk.IconTheme().list_icons()))

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "ASCIImator Desktop"
        self.set_titlebar(hb)

        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="document-save-symbolic"),
                            Gtk.IconSize.BUTTON))
        hb.pack_end(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="document-open-symbolic"),
                            Gtk.IconSize.BUTTON))
        button.connect("clicked", self.do_open)
        hb.pack_end(button)
        

        stack = Gtk.Stack()
#        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
#        stack.set_transition_duration(250)
        
        edit = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        stack.add_titled(edit, "edit", "Edit")

        label = Gtk.Label()
        label.set_markup("<big>Edit coming soon...</big>")
        edit.pack_start(label, True, True, 0)

        ab = Gtk.ActionBar()
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        ab.pack_start(stack_switcher)
        edit.pack_end(ab, False, False, 0)

        preview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        labelbox = Gtk.Box()
        label = Gtk.Label()
        label.set_alignment(0, 0)
        label.set_width_chars(self.player.asciimation.size[0])
        label.set_max_width_chars(self.player.asciimation.size[0])
        labelbox.pack_start(label, True, False, 0)
        preview.pack_start(labelbox, True, False, 0)
        self.do_animate(label)

        ab = Gtk.ActionBar()

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        ab.pack_start(stack_switcher)

        ab_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(ab_buttons.get_style_context(), "linked")

        btn_previous = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                  name="media-skip-backward-symbolic"),
                                  Gtk.IconSize.BUTTON))
        btn_previous.connect("clicked", self.do_previous)
        ab_buttons.add(btn_previous)

        btn_rewind = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                name="media-seek-backward-symbolic"),
                                Gtk.IconSize.BUTTON))
        btn_rewind.connect("clicked", self.do_rewind)
        ab_buttons.add(btn_rewind)

        btn_play = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                              name="media-playback-start-symbolic"),
                              Gtk.IconSize.BUTTON))
        btn_play.connect("clicked", self.do_play)
        ab_buttons.add(btn_play)

        btn_forward = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                                 name="media-seek-forward-symbolic"),
                                 Gtk.IconSize.BUTTON))
        btn_forward.connect("clicked", self.do_forward)
        ab_buttons.add(btn_forward)

        btn_next = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                              name="media-skip-forward-symbolic"),
                              Gtk.IconSize.BUTTON))
        btn_next.connect("clicked", self.do_next)
        ab_buttons.add(btn_next)

        ab.set_center_widget(ab_buttons)
        preview.pack_end(ab, False, False, 0)

        stack.add_titled(preview, "preview", "Preview")
        
        self.add(stack)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hb.pack_start(stack_switcher)

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
 font_family="{2},monospace">{3}</span>'.format(self.player.asciimation.font_size*1024,
                          asciiframe.foreground_color,
                          self.player.asciimation.font_family, text))
        widget.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse(asciiframe.background_color)[1])

        GObject.timeout_add(self.player.asciimation.speed, self.do_animate, widget)

    def do_previous(self, button):
        self.player.to_start()

    def do_rewind(self, button):
        self.player.rewind()

    def do_play(self, button):
        self.player.toggle_playing()
        if self.player.speed == 0:
            button.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-start-symbolic"), Gtk.IconSize.BUTTON))
        else:
            button.set_image(Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="media-playback-pause-symbolic"), Gtk.IconSize.BUTTON))

    def do_forward(self, button):
        self.player.fast_forward()

    def do_next(self, button):
        self.player.to_end()

    def do_open(self, button):
        dialog = Gtk.FileChooserDialog("Open", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.asciimation = ASCIImation(filename=self.filename)
            self.player = ASCIIPlayback(asciimation=self.asciimation, speed=0)
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

win = ASCIImatorDesktop()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
