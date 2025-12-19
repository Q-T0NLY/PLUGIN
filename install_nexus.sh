#!/usr/bin/env bash
set -euo pipefail
echo "Installing Nexus AI minimal demo into ~/.nexus"
DEST="$HOME/.nexus"
mkdir -p "$DEST"
cp nexus_dashboard.py nexus_widgets.py nexus_config.py nexus_api.py "$DEST/" || true
python3 -m venv "$DEST/venv" || true
echo "Created virtualenv at $DEST/venv"
cat > "$DEST/run_nexus.sh" <<'EOF'
#!/usr/bin/env bash
source "$HOME/.nexus/venv/bin/activate"
python "$HOME/.nexus/nexus_dashboard.py" "$@"
EOF
chmod +x "$DEST/run_nexus.sh"
echo "Installation complete. Run: $DEST/run_nexus.sh"
