#!/bin/bash
# Installer to copy the nexus zsh module to user's home and enable it
MODULE_SRC="$(pwd)/zsh-config/ultra-zsh/nexus_hyper_core.zsh"
TARGET="$HOME/.zshrc_custom"

if [[ ! -f "$MODULE_SRC" ]]; then
  echo "❌ Module source not found: $MODULE_SRC"
  exit 1
fi

mkdir -p "$HOME/.nexus"
cp "$MODULE_SRC" "$TARGET"
chmod 700 "$TARGET"

echo "# Sourcing Nexus hyper-core" >> "$HOME/.zshrc"
if ! grep -q "source \"$TARGET\"" "$HOME/.zshrc" 2>/dev/null; then
  echo "source \"$TARGET\"" >> "$HOME/.zshrc"
  echo "✅ Added 'source $TARGET' to ~/.zshrc"
else
  echo "ℹ️  ~/.zshrc already sources $TARGET"
fi

echo "✅ Nexus zsh module installed to: $TARGET"

echo "Run 'source ~/.zshrc' or start a new terminal to activate."