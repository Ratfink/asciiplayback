#!/usr/bin/env python
import sys
from gi.repository import Gtk, Gio, Gdk, GObject
from asciiplayback import *
from gtkasciiplayer import *

class ASCIImatorDesktop(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ASCIImator Desktop")
        self.set_default_size(400, 200)

        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
            self.asciimation = ASCIImation(filename=self.filename)
            self.player = ASCIIPlayback(self.asciimation, speed=0)
        else:
            self.filename = ""
            self.asciimation = ASCIImation(font_family='monospace', size=[15, 3])
            self.asciimation.frames.append(Frame(text='\nNo file loaded!\n'))
            self.player = ASCIIPlayback(asciimation=self.asciimation, speed=0)

        print('\n'.join(Gtk.IconTheme().list_icons()))

        self.hsize_group = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)

        right_box = self.main_content()
        left_box = self.sidebar()
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

        hb = self.headerbar()
        self.set_titlebar(hb)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.pack_start(left_box, False, False, 0)
        box.pack_start(separator, False, False, 0)
        box.pack_start(right_box, True, True, 0)

        self.add(box)

    def headerbar(self):
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        left_header = Gtk.HeaderBar()
        left_header.props.show_close_button = True
        right_header = Gtk.HeaderBar()
        right_header.props.show_close_button = True

        left_header.get_style_context().add_class("titlebar")
        left_header.get_style_context().add_class("titlebar-left")
        right_header.get_style_context().add_class("titlebar")
        right_header.get_style_context().add_class("titlebar-right")

        layout_desc = Gtk.Settings.get_default().props.gtk_decoration_layout
        tokens = layout_desc.split(":", 2)
        if tokens != None:
            right_header.props.decoration_layout = ":" + tokens[1]
            left_header.props.decoration_layout = tokens[0]

        self.title = Gtk.Label(self.filename)
        self.title.get_style_context().add_class("title")
        right_header.set_custom_title(self.title)

        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="document-save-symbolic"),
                            Gtk.IconSize.BUTTON))
        right_header.pack_end(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="document-open-symbolic"),
                            Gtk.IconSize.BUTTON))
        button.connect("clicked", self.do_open)
        right_header.pack_end(button)

        left_header.props.title = "ASCIImator Desktop"
        left_header.props.subtitle = "Offline ASCII Animator"

        header.pack_start(left_header, False, False, 0)
        header.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL),
                          False, False, 0)
        header.pack_start(right_header, True, True, 0)
        
        self.hsize_group.add_widget(left_header)

        return header

    def sidebar(self):
        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        ab = Gtk.ActionBar()
        ab.set_center_widget(self.stack_switcher)
        left.pack_end(ab, False, False, 0)



        self.hsize_group.add_widget(left)

        return left

    def main_content(self):
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(250)

        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(stack)

        #### Edit panel ####
        edit = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        edit_window = Gtk.ScrolledWindow()
        label = Gtk.Label()
        label.set_markup("<big>Edit coming soon...</big>")
        edit_window.add(label)
        edit.pack_start(edit_window, True, True, 0)

        ab = Gtk.ActionBar()
        ab_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(ab_buttons.get_style_context(), "linked")

        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="edit-undo-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="edit-redo-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="list-add-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="list-remove-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="edit-copy-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        button = Gtk.Button(image=Gtk.Image.new_from_gicon(Gio.ThemedIcon(
                            name="edit-paste-symbolic"),
                            Gtk.IconSize.BUTTON))
        ab_buttons.add(button)
        ab.set_center_widget(ab_buttons)

        edit.pack_end(ab, False, False, 0)

        stack.add_titled(edit, "edit", "Edit")

        #### Preview panel ####
        preview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.video = GtkASCIIPlayer(self.player)
        preview.pack_start(self.video, True, False, 0)

        ab = Gtk.ActionBar()

        self.controls = GtkASCIIControls(self.player)
        ab.set_center_widget(self.controls)
        preview.pack_end(ab, False, False, 0)

        stack.add_titled(preview, "preview", "Preview")

        return stack

    def do_open(self, button):
        dialog = Gtk.FileChooserDialog("Open", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.title.set_text(self.filename)
            self.asciimation = ASCIImation(filename=self.filename)
            self.player = ASCIIPlayback(asciimation=self.asciimation, speed=0)
            self.video.player = self.player
            self.controls.player = self.player
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

style_provider = Gtk.CssProvider()

css = b"""
.titlebar-left:dir(ltr),
.titlebar-left:dir(rtl) {
    border-top-right-radius: 0;
}

.titlebar-right:dir(ltr),
.titlebar-right:dir(rtl) {
    border-top-left-radius: 0;
}
"""

style_provider.load_from_data(css)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
Gtk.main()
