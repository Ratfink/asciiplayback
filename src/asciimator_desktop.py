#!/usr/bin/env python
import sys
from gi.repository import Gtk, Gio, Gdk, GObject
from asciiplayback import *
from gtkasciiplayer import *
from revealerexpander import *
from frameedit import *

class ASCIImatorDesktop(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ASCIImator Desktop")
        self.set_default_size(640, 400)

        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
            self.asciimation = ASCIImation(filename=self.filename)
            self.player = ASCIIPlayback(self.asciimation, speed=0)
        else:
            self.filename = ""
            self.asciimation = ASCIImation(font_family='monospace', size=[15, 3])
            self.asciimation.frames.append(Frame(text='\nNo file loaded!\n'))
            self.player = ASCIIPlayback(asciimation=self.asciimation, speed=0)

#        print('\n'.join(Gtk.IconTheme().list_icons()))

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

        expander_scroll = Gtk.ScrolledWindow()
        expander_scroll.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        expander_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        expander = RevealerExpander("_View")
        view = Gtk.ListBox()
        view.set_selection_mode(Gtk.SelectionMode.NONE)
        optionsize = Gtk.SizeGroup(Gtk.SizeGroupMode.HORIZONTAL)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add(hbox)
        label = Gtk.Label("Loop", xalign=0)
        switch = Gtk.Switch()
        switch.set_active(True)
        hbox.pack_start(label, True, True, 12)
        hbox.pack_start(switch, False, True, 12)
        Gtk.StyleContext.add_class(row.get_style_context(), "option")

        view.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add(hbox)
        label = Gtk.Label("ms/frame", xalign=0)
        spin = Gtk.SpinButton.new_with_range(0, 1000, 5)
        spin.set_value(100)
        optionsize.add_widget(spin)
        hbox.pack_start(label, True, True, 12)
        hbox.pack_start(spin, False, True, 12)
        Gtk.StyleContext.add_class(row.get_style_context(), "option")

        view.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add(hbox)
        label = Gtk.Label("Font", xalign=0)
        font = Gtk.FontButton.new_with_font("Courier New 12")
        optionsize.add_widget(font)
        hbox.pack_start(label, True, True, 12)
        hbox.pack_start(font, False, False, 12)
        Gtk.StyleContext.add_class(row.get_style_context(), "option")

        view.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add(hbox)
        label = Gtk.Label("Width", xalign=0)
        spin = Gtk.SpinButton.new_with_range(1, 1000, 1)
        spin.set_value(20)
        optionsize.add_widget(spin)
        hbox.pack_start(label, True, True, 12)
        hbox.pack_start(spin, False, True, 12)
        Gtk.StyleContext.add_class(row.get_style_context(), "option")

        view.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.add(hbox)
        label = Gtk.Label("Height", xalign=0)
        spin = Gtk.SpinButton.new_with_range(1, 1000, 1)
        spin.set_value(10)
        optionsize.add_widget(spin)
        hbox.pack_start(label, True, True, 12)
        hbox.pack_start(spin, False, True, 12)
        Gtk.StyleContext.add_class(row.get_style_context(), "option")

        view.add(row)

        expander.add(view)
        expander.set_expanded(True)
        expander_box.add(expander)

        expander = RevealerExpander("_Color")
        expander.add(Gtk.ColorButton())
        expander_box.add(expander)

        expander = RevealerExpander("_Frame")
        expander.add(Gtk.FontButton())
        expander_box.add(expander)

        expander = RevealerExpander("_Layer")
        expander.add(Gtk.FontButton())
        expander_box.add(expander)

        expander = RevealerExpander("_Replace")
        expander.add(Gtk.FontButton())
        expander_box.add(expander)

        expander_scroll.add(expander_box)
        left.pack_start(expander_scroll, True, True, 0)

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
        edit_flow = Gtk.FlowBox()
        edit_flow.set_homogeneous(False)
        edit_flow.set_column_spacing(12)
        edit_flow.set_row_spacing(12)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        frame = FrameEdit()
        edit_flow.add(frame)
        edit_window.add(edit_flow)
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

.option {
    padding-top: 3px;
    background-color: @theme_bg_color;
}
.option:hover {
    background-color: @theme_bg_color;
}
"""

style_provider.load_from_data(css)

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
Gtk.main()
