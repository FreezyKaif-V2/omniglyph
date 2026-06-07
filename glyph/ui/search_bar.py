import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


def create_search_bar(on_change=None):
    search = Gtk.SearchEntry()

    search.set_placeholder_text("Search symbols...")

    def on_search_changed(widget):
        if on_change:
            on_change(widget.get_text())

    search.connect("search-changed", on_search_changed)

    return search
