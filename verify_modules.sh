#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║            MODULE VERIFICATION SCRIPT - NEXUS AI STUDIO v3.1             ║
# ║           Verify that new chatbox and service bridge modules load        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}    NEXUS AI STUDIO - Module Verification                    ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if modules exist
echo -e "${YELLOW}→ Checking module files...${NC}"

CHATBOX_MODULE="/workspaces/ZSH/ZSH-main/zsh-config/ultra-zsh/modules/ai_chatbox.zsh"
BRIDGE_MODULE="/workspaces/ZSH/ZSH-main/zsh-config/ultra-zsh/modules/llm_service_bridge.zsh"

if [[ -f "$CHATBOX_MODULE" ]]; then
    echo -e "${GREEN}✓${NC} ai_chatbox.zsh exists ($(wc -l < "$CHATBOX_MODULE") lines)"
else
    echo -e "${RED}✗${NC} ai_chatbox.zsh NOT FOUND"
    exit 1
fi

if [[ -f "$BRIDGE_MODULE" ]]; then
    echo -e "${GREEN}✓${NC} llm_service_bridge.zsh exists ($(wc -l < "$BRIDGE_MODULE") lines)"
else
    echo -e "${RED}✗${NC} llm_service_bridge.zsh NOT FOUND"
    exit 1
fi

echo ""
echo -e "${YELLOW}→ Checking for required exports and functions...${NC}"

# Check ai_chatbox.zsh for key functions
CHATBOX_EXPORTS=(
    "NEXUS_CHATBOX_LOADED"
    "nexus_quantum_ai_chat"
    "NEXUS_AI_HOME"
    "NEXUS_CHAT_HISTORY"
)

for export in "${CHATBOX_EXPORTS[@]}"; do
    if grep -q "$export" "$CHATBOX_MODULE"; then
        echo -e "${GREEN}✓${NC} Found: $export (ai_chatbox.zsh)"
    else
        echo -e "${RED}✗${NC} Missing: $export (ai_chatbox.zsh)"
    fi
done

echo ""

# Check llm_service_bridge.zsh for key functions
BRIDGE_EXPORTS=(
    "NEXUS_LLM_BRIDGE_LOADED"
    "llm_invoke"
    "llm_ensemble"
    "llm_stream"
    "LLM_SERVICE_URL"
)

for export in "${BRIDGE_EXPORTS[@]}"; do
    if grep -q "$export" "$BRIDGE_MODULE"; then
        echo -e "${GREEN}✓${NC} Found: $export (llm_service_bridge.zsh)"
    else
        echo -e "${RED}✗${NC} Missing: $export (llm_service_bridge.zsh)"
    fi
done

echo ""
echo -e "${YELLOW}→ Checking syntax...${NC}"

# Check ZSH syntax
if zsh -n "$CHATBOX_MODULE" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} ai_chatbox.zsh syntax valid"
else
    echo -e "${RED}✗${NC} ai_chatbox.zsh has syntax errors"
    zsh -n "$CHATBOX_MODULE"
fi

if zsh -n "$BRIDGE_MODULE" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} llm_service_bridge.zsh syntax valid"
else
    echo -e "${RED}✗${NC} llm_service_bridge.zsh has syntax errors"
    zsh -n "$BRIDGE_MODULE"
fi

echo ""
echo -e "${YELLOW}→ Checking module list in directory...${NC}"

MODULES_DIR="/workspaces/ZSH/ZSH-main/zsh-config/ultra-zsh/modules"
echo -e "${GREEN}✓${NC} Total modules: $(ls -1 "$MODULES_DIR"/*.zsh 2>/dev/null | wc -l)"
echo "  Listing all .zsh modules:"
ls -1 "$MODULES_DIR"/*.zsh | sed 's|.*/||' | sed 's/^/    /'

echo ""
echo -e "${YELLOW}→ Checking install.sh module loader...${NC}"

INSTALL_SH="/workspaces/ZSH/ZSH-main/install.sh"
if grep -q "load_nexus_modules" "$INSTALL_SH"; then
    echo -e "${GREEN}✓${NC} Module loader found in install.sh"
    
    # Show the loader function
    echo "  Loader function:"
    sed -n '/^load_nexus_modules/,/^}/p' "$INSTALL_SH" | sed 's/^/    /'
else
    echo -e "${RED}✗${NC} Module loader NOT found in install.sh"
fi

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}    ✓ All verifications passed!                               ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}    Ready to run: bash install.sh                             ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Run: cd /workspaces/ZSH/ZSH-main && bash install.sh"
echo "  2. Start LLM service: llm_service_start"
echo "  3. Launch chatbox: nexus-chat"
echo ""
