#!/bin/zsh
# Install Hyper Registry CLI into Zsh configuration

set -e

SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
ZSH_CONFIG_DIR="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
REGISTRY_CLI_FILE="$SCRIPT_DIR/registry_cli.zsh"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     🚀 Installing Hyper Registry CLI into Zsh                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if registry_cli.zsh exists
if [ ! -f "$REGISTRY_CLI_FILE" ]; then
    echo "❌ registry_cli.zsh not found at $REGISTRY_CLI_FILE"
    exit 1
fi

# Create oh-my-zsh plugins directory if needed
mkdir -p "$ZSH_CONFIG_DIR/plugins/registry"

# Copy CLI script
echo "📋 Installing CLI script..."
cp "$REGISTRY_CLI_FILE" "$ZSH_CONFIG_DIR/plugins/registry/registry_cli.zsh"
chmod +x "$ZSH_CONFIG_DIR/plugins/registry/registry_cli.zsh"
echo "✓ CLI script installed"

# Create plugin loader
echo "📦 Creating plugin loader..."
cat > "$ZSH_CONFIG_DIR/plugins/registry/registry.plugin.zsh" << 'EOF'
# Hyper Registry Plugin for Oh-My-Zsh
# Provides CLI commands for interacting with Hyper Registry backend

REGISTRY_PLUGIN_DIR="${0:a:h}"
source "$REGISTRY_PLUGIN_DIR/registry_cli.zsh"

# Completion function
_registry_completions() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local commands="health status stats metrics help register get delete search link relationships"
    COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
}

alias reg='registry_register'
alias regs='registry_search'
alias reglink='registry_link'
alias regstats='registry_stats'
EOF
echo "✓ Plugin loader created"

# Update .zshrc
echo "⚙️  Updating .zshrc..."

ZSHRC="$HOME/.zshrc"

# Check if registry plugin is already in .zshrc
if grep -q "registry" "$ZSHRC"; then
    echo "ℹ️  Registry plugin already in .zshrc"
else
    # Add to plugins line if it exists
    if grep -q "^plugins=" "$ZSHRC"; then
        sed -i'' -e 's/plugins=(/plugins=(registry /' "$ZSHRC" || \
        sed -i'' "s/plugins=(/plugins=(registry /" "$ZSHRC" || true
        echo "✓ Added registry to plugins"
    else
        # Add plugins line
        echo "plugins=(registry)" >> "$ZSHRC"
        echo "✓ Created plugins line"
    fi
fi

# Add environment variable if needed
if ! grep -q "REGISTRY_API" "$ZSHRC"; then
    echo "" >> "$ZSHRC"
    echo "# Hyper Registry Configuration" >> "$ZSHRC"
    echo "export REGISTRY_API=http://localhost:8000" >> "$ZSHRC"
    echo "✓ Added REGISTRY_API environment variable"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Installation Complete!                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Next Steps:"
echo "  1. Reload your shell: source ~/.zshrc"
echo "  2. Verify installation: registry_help"
echo "  3. Check API connection: registry_health"
echo ""
echo "🎯 Quick Commands:"
echo "  registry_help           - Show all commands"
echo "  registry_health         - Check API status"
echo "  registry_agent ...      - Register agent"
echo "  registry_service ...    - Register service"
echo "  registry_search ...     - Search entries"
echo ""
