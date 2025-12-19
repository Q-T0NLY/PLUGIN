#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/universal-registry"
mkdir -p "$ROOT"
cp -r . "$ROOT"
chmod +x "$ROOT/universal-registry/cli/registry_cli.sh"

echo "Databases will be created under: $ROOT"
cd "$ROOT/universal-registry"
./cli/registry_cli.sh init

echo "To run as systemd service (Linux):"
echo "  sudo cp deploy/registry.service /etc/systemd/system/universal-registry.service"
echo "  sudo sed -i 's|/opt/universal-registry|$ROOT|g' /etc/systemd/system/universal-registry.service"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable --now universal-registry.service"

echo "To run on macOS (Launchd):"
echo "  sudo mkdir -p /opt/universal-registry && sudo cp -r . /opt/universal-registry"
echo "  sudo cp deploy/registry.plist /Library/LaunchDaemons/com.universal.registry.plist"
echo "  sudo launchctl bootstrap system /Library/LaunchDaemons/com.universal.registry.plist"

echo "Install complete."
