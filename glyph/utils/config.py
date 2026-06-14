from pathlib import Path
import tomllib

from gi.repository import GLib

DEFAULT_CONFIG = """
# OmniGlyph Configuration
#
# Location:
# ~/.config/omniglyph/config.toml
#
# Restart OmniGlyph after changing this file.
#
# Shortcut format examples:
#   ctrl+q
#   ctrl+shift+h
#   alt+s
#   super+space
#
# Supported modifiers:
#   ctrl, shift, alt, super
#
# Supported named keys:
#   slash, escape, return, tab, space,
#   up, down, left, right,
#   home, end, pageup, pagedown,
#   delete, backspace,
#   f1-f12
#
# Single-character keys:
#   a-z, 0-9, [, ], /, ., ,, ;, etc.
#
# If a setting is missing, OmniGlyph will fall back
# to its built-in default value.

[shortcuts]

# Quit OmniGlyph
quit = "ctrl+q"

# Focus the search bar
focus_search = "slash"

# Toggle category bar
toggle_categories = "c"

# Toggle sidebar
toggle_sidebar = "s"

# Open history view
history = "ctrl+h"

# Close sidebar
close_sidebar = "escape"

# Navigate categories
next_category = "]"
prev_category = "["

# Sidebar navigation
sidebar_next = "down"
sidebar_prev = "up"
sidebar_activate = "return"

# Copy first visible symbol
copy_first = "ctrl+return"

# Vim-style scrolling
scroll_down = "j"
scroll_up = "k"

# Reload active collection
reload_collection = "ctrl+r"

[behavior]

# hide | quit
esc_action = "hide"

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
    "slash": "/",
    "escape": "Esc",
    "return": "Enter",
    "enter": "Enter",
    "right": "→",
    "left": "←",
    "up": "↑",
    "down": "↓",
    "tab": "Tab",
    "space": "Space",
    "backspace": "Backspace",
    "delete": "Del",
    "home": "Home",
    "end": "End",
    "pageup": "PgUp",
    "pagedown": "PgDn",
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

    def _deep_copy(self, data):
        return {
            key: self._deep_copy(value) if isinstance(value, dict) else value
            for key, value in data.items()
        }

    def _merge(self, base, override):
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge(base[key], value)
            else:
                base[key] = value

        return base

    def _load_with_defaults(self):
        try:
            with open(self.config_file, "rb") as f:
                user_data = tomllib.load(f)
        except Exception:
            return self._deep_copy(DEFAULT_DATA)

        return self._merge(
            self._deep_copy(DEFAULT_DATA),
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

        result = []

        for part in raw.split("+"):
            part_lower = part.lower()

            if part_lower in ("ctrl", "shift", "alt", "super"):
                result.append(part_lower.capitalize())
            else:
                result.append(
                    KEY_DISPLAY.get(
                        part_lower,
                        part.upper() if len(part) == 1 else part.capitalize(),
                    )
                )

        return "+".join(result)
