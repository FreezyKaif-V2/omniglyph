import gi
import sys


gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gtk4LayerShell", "1.0")

from gi.repository import Gtk, Adw, Gdk, Gio
from gi.repository import Gtk4LayerShell

from ui import *
from db.loader import CollectionLoader

from utils.window_manager import is_tiling_window_manager
from utils.config import Config

from importlib.resources import files

css_provider = Gtk.CssProvider()
css_data = files("styles").joinpath("style.css").read_bytes()
css_provider.load_from_data(css_data)
Gtk.StyleContext.add_provider_for_display(
    Gdk.Display.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER,
)

COLLECTION_FLAGS = {
    "emoji": "LoadEmojis",
    "emoticons": "LoadEmoticons",
    "arrows": "LoadArrows",
    "math": "LoadMathSymbols",
    "currency": "LoadCurrency",
    "special": "LoadSpecialSymbols",
    "hieroglyphs": "LoadHieroglyphs",
}

DEFAULT_COLLECTION = "LoadEmojis"

config = Config()

_NAMED_KEYS = {
    "slash": Gdk.KEY_slash,
    "escape": Gdk.KEY_Escape,
    "return": Gdk.KEY_Return,
    "enter": Gdk.KEY_Return,
    "right": Gdk.KEY_Right,
    "left": Gdk.KEY_Left,
    "up": Gdk.KEY_Up,
    "down": Gdk.KEY_Down,
    "tab": Gdk.KEY_Tab,
    "space": Gdk.KEY_space,
    "backspace": Gdk.KEY_BackSpace,
    "delete": Gdk.KEY_Delete,
    "home": Gdk.KEY_Home,
    "end": Gdk.KEY_End,
    "pageup": Gdk.KEY_Page_Up,
    "pagedown": Gdk.KEY_Page_Down,
    "f1": Gdk.KEY_F1,
    "f2": Gdk.KEY_F2,
    "f3": Gdk.KEY_F3,
    "f4": Gdk.KEY_F4,
    "f5": Gdk.KEY_F5,
    "f6": Gdk.KEY_F6,
    "f7": Gdk.KEY_F7,
    "f8": Gdk.KEY_F8,
    "f9": Gdk.KEY_F9,
    "f10": Gdk.KEY_F10,
    "f11": Gdk.KEY_F11,
    "f12": Gdk.KEY_F12,
}


def _parse_shortcut(shortcut):
    if not shortcut:
        return None, Gdk.ModifierType(0)

    parts = [p.strip().lower() for p in shortcut.split("+")]

    mods = Gdk.ModifierType(0)
    key_parts = []

    for p in parts:
        if p == "ctrl":
            mods |= Gdk.ModifierType.CONTROL_MASK
        elif p == "shift":
            mods |= Gdk.ModifierType.SHIFT_MASK
        elif p == "alt":
            mods |= Gdk.ModifierType.ALT_MASK
        elif p == "super":
            mods |= Gdk.ModifierType.SUPER_MASK
        else:
            key_parts.append(p)

    key_str = "+".join(key_parts)

    keyval = _NAMED_KEYS.get(key_str)
    if keyval is None and len(key_str) == 1:
        keyval = Gdk.unicode_to_keyval(ord(key_str))

    return keyval, mods


class AppWindow(Adw.ApplicationWindow):
    def __init__(self, app, initial_data, loader_name):
        super().__init__(application=app)

        self.config = config
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        setup_actions(self)

        self._setup_overlay_window()

        self.char_view = CharView(self, initial_data, loader_name)

        self._build_layout()
        self._setup_keyboard_shortcuts()

        self.main_box.append(self.char_view)

        self.connect("close-request", self._on_close_request)

    def _on_close_request(self, *_):
        self.set_visible(False)
        return True

    def _hide_window(self):
        self.set_visible(False)

    def show_and_focus(self, data, loader_name):
        self.search.set_text("")

        if loader_name != self.char_view.active_loader:
            self.char_view._on_collection_changed(data)
            self.char_view.active_loader = loader_name

        self.present()

        self._focus_search()

    def _setup_overlay_window(self):
        if not is_tiling_window_manager():
            return

        self.set_decorated(False)
        self.set_resizable(False)

        Gtk4LayerShell.init_for_window(self)
        Gtk4LayerShell.set_layer(self, Gtk4LayerShell.Layer.OVERLAY)
        Gtk4LayerShell.set_keyboard_mode(self, Gtk4LayerShell.KeyboardMode.EXCLUSIVE)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.TOP, True)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.RIGHT, True)
        Gtk4LayerShell.set_margin(self, Gtk4LayerShell.Edge.TOP, 20)
        Gtk4LayerShell.set_margin(self, Gtk4LayerShell.Edge.RIGHT, 20)

    def _build_layout(self):
        self.set_title("OmniGlyph")

        if not is_tiling_window_manager():
            self.main_box.append(AppHeader())

        w = self.config.get("behavior", "window_width", default=450)
        h = self.config.get("behavior", "window_height", default=500)
        self.set_default_size(w, h)
        self.main_box.set_spacing(0)

        self.root_overlay = Gtk.Overlay()
        self.root_overlay.set_child(self.main_box)
        self.set_content(self.root_overlay)

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.set_margin_top(12)
        search_box.set_margin_bottom(8)
        search_box.set_margin_start(12)
        search_box.set_margin_end(12)

        self.search = create_search_bar(on_change=self.char_view.filter_entries)
        self.search.set_hexpand(True)
        self.search.set_halign(Gtk.Align.FILL)

        sidebar_sc = self.config.shortcut_label("toggle_sidebar")
        side_bar_button = Gtk.Button()
        side_bar_button.set_icon_name("open-menu-symbolic")
        side_bar_button.set_valign(Gtk.Align.START)
        side_bar_button.set_tooltip_text(f"Open sidebar ({sidebar_sc})")
        side_bar_button.set_margin_start(6)
        side_bar_button.connect("clicked", lambda _: self.char_view.toggle_side_bar())

        search_box.append(self.search)
        search_box.append(side_bar_button)

        self.main_box.append(search_box)
        self.root_overlay.add_overlay(self.char_view.side_bar)

    def _setup_keyboard_shortcuts(self):
        controller = Gtk.EventControllerKey()
        controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(controller)

    def _focus_search(self):
        self.search.grab_focus()
        self.search.select_region(0, len(self.search.get_text()))

    def _match(self, keyval, pure_mods, name, default=""):
        k, m = _parse_shortcut(self.config.get("shortcuts", name, default=default))
        return k is not None and keyval == k and pure_mods == m

    def _on_key_pressed(self, controller, keyval, keycode, state):
        pure_mods = state & (
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.SHIFT_MASK
            | Gdk.ModifierType.ALT_MASK
            | Gdk.ModifierType.SUPER_MASK
        )

        focus = self.get_focus()
        search_focused = focus is self.search
        sidebar_open = self.char_view.side_bar.is_open()

        if sidebar_open:
            if self._match(keyval, pure_mods, "toggle_sidebar", "s"):
                self.char_view.toggle_side_bar()
                return True

            return False

        if (
            self._match(keyval, pure_mods, "focus_search", "slash")
            and not search_focused
        ):
            self._focus_search()
            return True

        if self._match(keyval, pure_mods, "toggle_sidebar", "s") and not search_focused:
            self.char_view.toggle_side_bar()
            first_name = COLLECTIONS[0]["name"]
            self.char_view.side_bar._buttons[first_name].grab_focus()
            return True

        if self._match(keyval, pure_mods, "next_category", "]") and not search_focused:
            self.char_view.select_next_category()
            return True

        if self._match(keyval, pure_mods, "prev_category", "[") and not search_focused:
            self.char_view.select_prev_category()
            return True

        if self._match(keyval, pure_mods, "scroll_down", "j") and not search_focused:
            self.char_view.scroll_by(
                self.config.get("behavior", "scroll_step", default=120)
            )
            return True

        if self._match(keyval, pure_mods, "scroll_up", "k") and not search_focused:
            self.char_view.scroll_by(
                -self.config.get("behavior", "scroll_step", default=120)
            )
            return True

        if self._match(keyval, pure_mods, "copy_first", "ctrl+return"):
            self.char_view.copy_first_symbol()
            return True

        if self._match(keyval, pure_mods, "reload_collection", "ctrl+r"):
            self.char_view.reload_current_collection()
            return True

        if keyval == Gdk.KEY_Escape:
            if search_focused:
                self.set_focus(None)
                return True
            esc_action = self.config.get("behavior", "esc_action", default="hide")
            if esc_action == "hide":
                self._hide_window()
            return True

        return False


class MyApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="dev.anishroy.omniglyph",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.window = None

    def _resolve_collection(self, args):
        for arg in args:
            flag = arg.lstrip("-").lower()
            if flag in COLLECTION_FLAGS:
                return COLLECTION_FLAGS[flag]
        return DEFAULT_COLLECTION

    def _load(self, loader_name):
        return getattr(CollectionLoader(), loader_name)()

    def do_activate(self):
        pass

    def do_command_line(self, command_line):
        raw = command_line.get_arguments()[1:]
        args = [a.decode() if isinstance(a, bytes) else a for a in raw]

        for arg in args:
            flag = arg.lstrip("-").lower()
            if flag in ("help", "h"):
                flags = "\n  ".join(f"--{f}" for f in COLLECTION_FLAGS)
                print(
                    f"Usage: omniglyph [OPTION]\n\nCollections:\n  {flags}\n\nDefault: --emoji"
                )
                return 0

        loader_name = self._resolve_collection(args)

        if self.window is None:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)
            data = self._load(loader_name)
            self.window = AppWindow(self, data, loader_name)
            self.hold()
            self.window.show_and_focus(data, loader_name)
        else:
            if loader_name != self.window.char_view.active_loader:
                data = self._load(loader_name)
                self.window.show_and_focus(data, loader_name)
            else:
                self.window.show_and_focus(None, loader_name)

        return 0


app = MyApp()
app.run(sys.argv)
