from gi.repository import Gdk

_NAMED_KEYS = {
    # Navigation
    "up": Gdk.KEY_Up,
    "down": Gdk.KEY_Down,
    "left": Gdk.KEY_Left,
    "right": Gdk.KEY_Right,
    "home": Gdk.KEY_Home,
    "end": Gdk.KEY_End,
    "pageup": Gdk.KEY_Page_Up,
    "pagedown": Gdk.KEY_Page_Down,
    # Editing
    "escape": Gdk.KEY_Escape,
    "return": Gdk.KEY_Return,
    "enter": Gdk.KEY_Return,
    "tab": Gdk.KEY_Tab,
    "space": Gdk.KEY_space,
    "backspace": Gdk.KEY_BackSpace,
    "delete": Gdk.KEY_Delete,
    "insert": Gdk.KEY_Insert,
    # Lock keys
    "capslock": Gdk.KEY_Caps_Lock,
    "numlock": Gdk.KEY_Num_Lock,
    "scrolllock": Gdk.KEY_Scroll_Lock,
    # Misc
    "menu": Gdk.KEY_Menu,
    "printscreen": Gdk.KEY_Print,
    "pause": Gdk.KEY_Pause,
    # Symbols
    "slash": Gdk.KEY_slash,
    "backslash": Gdk.KEY_backslash,
    "comma": Gdk.KEY_comma,
    "period": Gdk.KEY_period,
    "dot": Gdk.KEY_period,
    "semicolon": Gdk.KEY_semicolon,
    "apostrophe": Gdk.KEY_apostrophe,
    "quote": Gdk.KEY_quotedbl,
    "minus": Gdk.KEY_minus,
    "equal": Gdk.KEY_equal,
    "plus": Gdk.KEY_plus,
    "grave": Gdk.KEY_grave,
    "backtick": Gdk.KEY_grave,
    # Brackets
    "leftbracket": Gdk.KEY_bracketleft,
    "rightbracket": Gdk.KEY_bracketright,
    "leftbrace": Gdk.KEY_braceleft,
    "rightbrace": Gdk.KEY_braceright,
    "leftparen": Gdk.KEY_parenleft,
    "rightparen": Gdk.KEY_parenright,
    # Function keys
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
    # Numeric keypad
    "kp_enter": Gdk.KEY_KP_Enter,
    "kp_add": Gdk.KEY_KP_Add,
    "kp_subtract": Gdk.KEY_KP_Subtract,
    "kp_multiply": Gdk.KEY_KP_Multiply,
    "kp_divide": Gdk.KEY_KP_Divide,
    "kp_decimal": Gdk.KEY_KP_Decimal,
    "kp_0": Gdk.KEY_KP_0,
    "kp_1": Gdk.KEY_KP_1,
    "kp_2": Gdk.KEY_KP_2,
    "kp_3": Gdk.KEY_KP_3,
    "kp_4": Gdk.KEY_KP_4,
    "kp_5": Gdk.KEY_KP_5,
    "kp_6": Gdk.KEY_KP_6,
    "kp_7": Gdk.KEY_KP_7,
    "kp_8": Gdk.KEY_KP_8,
    "kp_9": Gdk.KEY_KP_9,
}


def _parse_shortcut(shortcut):
    if not shortcut:
        return None, Gdk.ModifierType(0)

    parts = [p.strip().lower() for p in shortcut.split("+")]

    mods = Gdk.ModifierType(0)
    key_parts = []

    for part in parts:
        if part == "ctrl":
            mods |= Gdk.ModifierType.CONTROL_MASK
        elif part == "shift":
            mods |= Gdk.ModifierType.SHIFT_MASK
        elif part == "alt":
            mods |= Gdk.ModifierType.ALT_MASK
        elif part == "super":
            mods |= Gdk.ModifierType.SUPER_MASK
        else:
            key_parts.append(part)

    key_name = "+".join(key_parts)

    keyval = _NAMED_KEYS.get(key_name)

    if keyval is None and len(key_name) == 1:
        keyval = Gdk.unicode_to_keyval(ord(key_name))

    return keyval, mods
