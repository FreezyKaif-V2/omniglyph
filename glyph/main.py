import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Adw, Gdk
from gi.repository import Gtk4LayerShell

import os
from ui import *


class AppWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self._setup_overlay_window()

        self.char_view = CharView(self)

        self._build_layout()
        self._setup_keyboard_shortcuts()

        self.main_box.append(self.char_view)

    def _setup_overlay_window(self):
        is_wayland = os.environ.get("XDG_SESSION_TYPE") == "wayland"

        if not is_wayland:
            return

        self.set_decorated(False)
        self.set_resizable(False)

        Gtk4LayerShell.init_for_window(self)

        Gtk4LayerShell.set_layer(
            self,
            Gtk4LayerShell.Layer.OVERLAY,
        )

        Gtk4LayerShell.set_keyboard_mode(
            self,
            Gtk4LayerShell.KeyboardMode.EXCLUSIVE,
        )

        Gtk4LayerShell.set_anchor(
            self,
            Gtk4LayerShell.Edge.TOP,
            True,
        )

        Gtk4LayerShell.set_anchor(
            self,
            Gtk4LayerShell.Edge.RIGHT,
            True,
        )

        Gtk4LayerShell.set_margin(
            self,
            Gtk4LayerShell.Edge.TOP,
            20,
        )

        Gtk4LayerShell.set_margin(
            self,
            Gtk4LayerShell.Edge.RIGHT,
            20,
        )

    def _build_layout(self):
        self.set_title("OmniGlyph")
        self.set_default_size(450, 600)

        self.main_box.set_spacing(10)

        self.set_content(self.main_box)

        header_bar = AppHeader()
        self.main_box.append(header_bar)

        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        search_box.set_margin_top(24)
        search_box.set_margin_bottom(24)
        search_box.set_margin_start(12)
        search_box.set_margin_end(12)

        self.search = create_search_bar(on_change=self.char_view.filter_entries)

        self.search.set_hexpand(True)
        self.search.set_halign(Gtk.Align.FILL)

        search_box.append(self.search)

        self.main_box.append(search_box)

    def _setup_keyboard_shortcuts(self):
        controller = Gtk.EventControllerKey()

        controller.connect(
            "key-pressed",
            self._on_key_pressed,
        )

        self.add_controller(controller)

    def _focus_search(self):
        self.search.grab_focus()

        self.search.select_region(
            0,
            len(self.search.get_text()),
        )

    def _on_key_pressed(
        self,
        controller,
        keyval,
        keycode,
        state,
    ):
        # Focus search on pressing '/'
        if keyval == Gdk.KEY_slash:
            self._focus_search()
            return True

        if keyval != Gdk.KEY_Escape:
            return False

        # If search is focused, unfocus it on ESC
        if self.get_focus() is self.search:
            self.set_focus(None)
            return True

        # Otherwise ESC will close window
        self.close()

        return True


class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="dev.anishroy.glyph")

    def do_activate(self):
        window = AppWindow(self)
        window.present()


app = MyApp()
app.run()
