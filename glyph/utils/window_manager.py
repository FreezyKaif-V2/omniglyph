import os


def is_tiling_window_manager() -> bool:
    desktops = (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower().replace(":", ";").split(";")
    )

    tiling_wms = {
        "hyprland",
        "sway",
        "i3",
        "bspwm",
        "awesome",
        "river",
        "niri",
        "dwl",
        "qtile",
    }

    return (
        "HYPRLAND_INSTANCE_SIGNATURE" in os.environ
        or "SWAYSOCK" in os.environ
        or any(desktop in tiling_wms for desktop in desktops)
    )
