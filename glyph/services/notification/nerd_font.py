import webbrowser

from gi.repository import Gio, PangoCairo
from utils.settings import (
    get_setting,
    set_setting,
)

NERD_FONT_URL = "https://www.nerdfonts.com/"


def has_nerd_font():
    try:
        fontmap = PangoCairo.FontMap.get_default()

        return any(
            "Nerd Font" in family.get_name() for family in fontmap.list_families()
        )

    except Exception:
        return False


def _show_nerd_font_notification(app):
    try:
        notification = Gio.Notification.new("Nerd Font Required")

        notification.set_body(
            "Install a Nerd Font to display icons from the Nerd Fonts collection."
        )

        notification.add_button(
            "Get Nerd Fonts",
            "app.open-nerd-fonts",
        )

        notification.add_button(
            "Don't Show Again",
            "app.dismiss-nerd-font-notification",
        )

        app.send_notification(
            "omniglyph-nerd-font",
            notification,
        )

    except Exception:
        pass

    return False


def setup_nerd_font_actions(app):
    try:
        open_action = Gio.SimpleAction.new(
            "open-nerd-fonts",
            None,
        )

        open_action.connect(
            "activate",
            lambda *_: webbrowser.open(NERD_FONT_URL),
        )

        app.add_action(open_action)

        dismiss_action = Gio.SimpleAction.new(
            "dismiss-nerd-font-notification",
            None,
        )

        dismiss_action.connect(
            "activate",
            lambda *_: set_setting(
                "hide_nerd_font_notification",
                True,
            ),
        )

        app.add_action(dismiss_action)

    except Exception:
        pass


def notify_if_nerd_font_missing(app):
    if has_nerd_font():
        return

    if get_setting("hide_nerd_font_notification"):
        return

    _show_nerd_font_notification(app)
