from copy import deepcopy
from pathlib import Path
import tomllib

from gi.repository import GLib

DEFAULT_CONFIG = r"""
# OmniGlyph Configuration
#
# Location:
# ~/.config/omniglyph/config.toml
#
# Restart OmniGlyph after changing this file.
#
# Shortcut Syntax
# ----------------
#
# A shortcut is composed of zero or more modifiers
# followed by a key name:
#
#   ctrl+q
#   ctrl+shift+h
#   alt+s
#   super+space
#   ctrl+alt+delete
#
# Supported Modifiers
# -------------------
#
#   ctrl
#   shift
#   alt
#   super
#
# Supported Named Keys
# --------------------
#
# Navigation
#
#   up
#   down
#   left
#   right
#   home
#   end
#   pageup
#   pagedown
#
# Editing
#
#   return
#   enter
#   escape
#   tab
#   space
#   backspace
#   delete
#   insert
#
# Lock Keys
#
#   capslock
#   numlock
#   scrolllock
#
# Function Keys
#
#   f1 - f12
#
# Miscellaneous
#
#   menu
#   printscreen
#   pause
#
# Symbol Keys
#
#   slash        (/)
#   backslash    (\\)
#   comma        (,)
#   period       (.)
#   dot          (.)
#   semicolon    (;)
#   apostrophe   (')
#   quote        (")
#   minus        (-)
#   equal        (=)
#   plus         (+)
#   grave        (`)
#   backtick     (`)
#
# Bracket Keys
#
#   leftbracket   ([)
#   rightbracket  (])
#   leftbrace     ({)
#   rightbrace    (})
#   leftparen     (()
#   rightparen    ())
#
# Keypad Keys
#
#   kp_enter
#   kp_add
#   kp_subtract
#   kp_multiply
#   kp_divide
#   kp_decimal
#
# Single Character Keys
# ---------------------
#
# Any single printable character can also be used:
#
#   a-z
#   A-Z
#   0-9
#   /
#   \\
#   [
#   ]
#   .
#   ,
#   ;
#   '
#   -
#   =
#
# Missing values automatically fall back
# to OmniGlyph's built-in defaults.

[shortcuts]

# Quit OmniGlyph
quit = "ctrl+q"

# Focus search bar
focus_search = "slash"

# Toggle category bar
toggle_categories = "tab"

# Toggle sidebar
toggle_sidebar = "ctrl+b"

# Open history view
history = "ctrl+h"

# Close sidebar
close_sidebar = "escape"

# Navigate categories
next_category = "pagedown"
prev_category = "pageup"

# Sidebar navigation
sidebar_next = "down"
sidebar_prev = "up"
sidebar_activate = "return"

# Copy first visible symbol
copy_first = "ctrl+return"

# Scroll symbol grid
scroll_down = "down"
scroll_up = "up"

# Reload active collection
reload_collection = "ctrl+r"

[behavior]

# hide | quit
esc_action = "hide"

# system | light | dark
theme = "system"

# Hide window after copying a symbol
close_on_copy = true

# Show notifications
show_notifications = true

# Number of columns in the symbol grid
grid_columns = 13

# Symbols loaded per pagination batch
batch_size = 30

# Initial window size
window_width = 450
window_height = 500

# Sidebar width in pixels
sidebar_width = 180

# Scroll amount used by scroll shortcuts
scroll_step = 120
"""

DEFAULT_DATA = {
    "shortcuts": {
        "quit": "ctrl+q",
        "focus_search": "slash",
        "toggle_categories": "c",
        "toggle_sidebar": "s",
        "history": "ctrl+h",
        "close_sidebar": "escape",
        "next_category": "]",
        "prev_category": "[",
        "sidebar_next": "down",
        "sidebar_prev": "up",
        "sidebar_activate": "return",
        "copy_first": "return",
        "scroll_down": "j",
        "scroll_up": "k",
        "reload_collection": "ctrl+r",
    },
    "behavior": {
        "esc_action": "hide",
        "theme": "system",
        "close_on_copy": True,
        "show_notifications": True,
        "grid_columns": 13,
        "batch_size": 30,
        "window_width": 450,
        "window_height": 500,
        "sidebar_width": 180,
        "scroll_step": 120,
    },
}

KEY_DISPLAY = {
    # Modifiers
    "ctrl": "Ctrl",
    "shift": "Shift",
    "alt": "Alt",
    "super": "Super",
    # Symbols
    "slash": "/",
    "backslash": "\\",
    "comma": ",",
    "period": ".",
    "dot": ".",
    "semicolon": ";",
    "apostrophe": "'",
    "quote": '"',
    "minus": "-",
    "equal": "=",
    "plus": "+",
    "grave": "`",
    "backtick": "`",
    # Brackets
    "leftbracket": "[",
    "rightbracket": "]",
    "leftbrace": "{",
    "rightbrace": "}",
    "leftparen": "(",
    "rightparen": ")",
    # Navigation
    "up": "↑",
    "down": "↓",
    "left": "←",
    "right": "→",
    "home": "Home",
    "end": "End",
    "pageup": "PgUp",
    "pagedown": "PgDn",
    # Editing
    "tab": "Tab",
    "space": "Space",
    "escape": "Esc",
    "return": "Enter",
    "enter": "Enter",
    "backspace": "Backspace",
    "delete": "Del",
    "insert": "Ins",
    # Lock keys
    "capslock": "Caps Lock",
    "numlock": "Num Lock",
    "scrolllock": "Scroll Lock",
    # Misc
    "menu": "Menu",
    "printscreen": "PrtSc",
    "pause": "Pause",
    # Keypad
    "kp_enter": "Num Enter",
    "kp_add": "Num +",
    "kp_subtract": "Num -",
    "kp_multiply": "Num *",
    "kp_divide": "Num /",
    "kp_decimal": "Num .",
}


class Config:
    def __init__(self):
        config_dir = Path(GLib.get_user_config_dir()) / "omniglyph"
        config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = config_dir / "config.toml"

        if not self.config_file.exists():
            self.config_file.write_text(
                DEFAULT_CONFIG,
                encoding="utf-8",
            )

        self.data = self._load_with_defaults()

    def _merge(self, base, override):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge(base[key], value)
            else:
                base[key] = value

        return base

    def _load_with_defaults(self):
        try:
            with self.config_file.open("rb") as f:
                user_data = tomllib.load(f)
        except (FileNotFoundError, tomllib.TOMLDecodeError):
            return deepcopy(DEFAULT_DATA)

        return self._merge(
            deepcopy(DEFAULT_DATA),
            user_data,
        )

    def load(self):
        self.data = self._load_with_defaults()
        return self.data

    def get(self, *keys, default=None):
        value = self.data

        for key in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value

    def shortcut_label(self, name):
        raw = self.get("shortcuts", name, default="")

        if not raw:
            return ""

        parts = []

        for part in raw.split("+"):
            part_lower = part.lower()

            parts.append(
                KEY_DISPLAY.get(
                    part_lower,
                    part.upper() if len(part) == 1 else part.capitalize(),
                )
            )

        return "+".join(parts)
