#!/usr/bin/env bash
set -euo pipefail

echo "Uninstalling OmniGlyph..."

sudo rm -f /usr/local/bin/omniglyph
sudo rm -f /usr/local/share/applications/dev.anishroy.omniglyph.desktop
sudo rm -f /usr/local/share/icons/hicolor/256x256/apps/omniglyph.png

echo "Updating desktop database..."
sudo update-desktop-database \
    /usr/local/share/applications || true

echo "Updating icon cache..."
sudo gtk-update-icon-cache \
    -f /usr/local/share/icons/hicolor || true

echo "OmniGlyph uninstalled successfully."
