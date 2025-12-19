#!/bin/bash
################################################################################
#              NEXUSPRO TERMINAL SYSTEM - INTERACTIVE SETUP WIZARD             #
#         User-friendly configuration and customization interface              #
################################################################################
#
# PURPOSE: Interactive setup wizard for NEXUSPRO Terminal System
# USAGE: bash setup-wizard.sh
# STATUS: Production Ready
#
# Features:
# - Feature selection interface
# - Package manager preferences
# - Development tool customization
# - Performance tuning options
# - Theme selection
# - Summary and confirmation
#
################################################################################

set -euo pipefail

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 1. CONFIGURATION                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${HOME}/.nexuspro/config"
CONFIG_FILE="${CONFIG_DIR}/setup.config"
WIZARD_LOG="${CONFIG_DIR}/wizard.log"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration options (to be set by user)
declare -A CONFIG_OPTIONS=(
    [ENABLE_DEVTOOLS]="true"
    [ENABLE_ALIASES]="true"
    [ENABLE_VISUAL]="true"
    [ENABLE_PERFORMANCE]="true"
    [ENABLE_CLEANUP]="true"
    [INSTALL_HOMEBREW]="auto"
    [PERFORMANCE_TARGET]="50"
    [THEME]="dark"
    [ENABLE_DOCKER]="true"
    [ENABLE_KUBERNETES]="true"
    [ENABLE_CLOUD_TOOLS]="true"
)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 2. UTILITY FUNCTIONS                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >> "$WIZARD_LOG" 2>/dev/null || true
}

clear_screen() {
    clear
}

print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                   NEXUSPRO Terminal System Setup Wizard                    ║"
    echo "║              Configure your ultra-modern terminal environment             ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_option() {
    local number="$1"
    local text="$2"
    echo "  $(printf '%2d' "$number"). $text"
}

yes_no_prompt() {
    local prompt="$1"
    local default="${2:-y}"
    
    while true; do
        if [[ "$default" == "y" ]]; then
            read -p "$(echo -e ${BLUE}$prompt${NC}) [Y/n] " -r -n 1
            echo
            [[ -z "$REPLY" || "$REPLY" =~ ^[Yy]$ ]] && return 0 || return 1
        else
            read -p "$(echo -e ${BLUE}$prompt${NC}) [y/N] " -r -n 1
            echo
            [[ "$REPLY" =~ ^[Yy]$ ]] && return 0 || return 1
        fi
    done
}

numbered_menu() {
    local prompt="$1"
    shift
    local options=("$@")
    local choice
    
    while true; do
        echo -e "${BLUE}$prompt${NC}"
        for i in "${!options[@]}"; do
            print_option $((i + 1)) "${options[$i]}"
        done
        echo ""
        read -p "$(echo -e ${CYAN}Enter your choice (1-${#options[@]}): ${NC})" choice
        
        if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#options[@]} )); then
            echo "$((choice - 1))"
            return 0
        else
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            echo ""
        fi
    done
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 3. WELCOME & OVERVIEW                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

show_welcome() {
    clear_screen
    print_header
    
    cat << EOF
Welcome to the NEXUSPRO Terminal System Setup Wizard!

This interactive wizard will help you configure:
  ✓ Development tools integration (Git, Docker, Kubernetes)
  ✓ Package manager setup (Homebrew)
  ✓ Language runtime support (Python, Node, Ruby, Rust, Go)
  ✓ Visual enhancements and terminal appearance
  ✓ Performance optimization settings
  ✓ Advanced system cleanup and conflict detection

Estimated time: 5-10 minutes

EOF
    
    yes_no_prompt "Ready to configure your terminal?" "y" || exit 0
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 4. FEATURE SELECTION                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

configure_features() {
    clear_screen
    print_header
    print_section "Step 1: Feature Selection"
    
    echo "Which features would you like to enable?"
    echo ""
    
    # Development Tools
    if yes_no_prompt "Enable development tools integration (Git, Docker, Kubernetes)?" "y"; then
        CONFIG_OPTIONS[ENABLE_DEVTOOLS]="true"
        print_success "✓ Development tools enabled"
    else
        CONFIG_OPTIONS[ENABLE_DEVTOOLS]="false"
    fi
    
    # Aliases
    if yes_no_prompt "Enable productivity aliases and shortcuts?" "y"; then
        CONFIG_OPTIONS[ENABLE_ALIASES]="true"
        print_success "✓ Aliases enabled"
    else
        CONFIG_OPTIONS[ENABLE_ALIASES]="false"
    fi
    
    # Visual Enhancements
    if yes_no_prompt "Enable visual enhancements (colors, syntax highlighting)?" "y"; then
        CONFIG_OPTIONS[ENABLE_VISUAL]="true"
        print_success "✓ Visual enhancements enabled"
    else
        CONFIG_OPTIONS[ENABLE_VISUAL]="false"
    fi
    
    # Performance
    if yes_no_prompt "Enable performance optimization (lazy loading, caching)?" "y"; then
        CONFIG_OPTIONS[ENABLE_PERFORMANCE]="true"
        print_success "✓ Performance optimization enabled"
    else
        CONFIG_OPTIONS[ENABLE_PERFORMANCE]="false"
    fi
    
    # Cleanup
    if yes_no_prompt "Enable system cleanup and conflict detection?" "y"; then
        CONFIG_OPTIONS[ENABLE_CLEANUP]="true"
        print_success "✓ Cleanup enabled"
    else
        CONFIG_OPTIONS[ENABLE_CLEANUP]="false"
    fi
}

print_success() {
    echo -e "${GREEN}$*${NC}"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 5. PACKAGE MANAGER SETUP                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

configure_package_manager() {
    clear_screen
    print_header
    print_section "Step 2: Package Manager Configuration"
    
    echo "NEXUSPRO uses Homebrew for package management on macOS."
    echo ""
    
    if command -v brew &>/dev/null; then
        echo -e "${GREEN}✓ Homebrew is already installed${NC}"
        echo "  Version: $(brew --version | head -1)"
        CONFIG_OPTIONS[INSTALL_HOMEBREW]="skip"
    else
        echo -e "${YELLOW}⚠ Homebrew is not installed${NC}"
        echo ""
        
        if yes_no_prompt "Install Homebrew?" "y"; then
            CONFIG_OPTIONS[INSTALL_HOMEBREW]="true"
            print_success "✓ Homebrew installation scheduled"
        else
            CONFIG_OPTIONS[INSTALL_HOMEBREW]="false"
            echo -e "${YELLOW}⚠ Package manager features will be limited${NC}"
        fi
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 6. DEVELOPMENT TOOLS SELECTION                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

configure_dev_tools() {
    clear_screen
    print_header
    print_section "Step 3: Development Tools Configuration"
    
    if [[ "${CONFIG_OPTIONS[ENABLE_DEVTOOLS]}" == "false" ]]; then
        echo "Development tools are disabled."
        return 0
    fi
    
    echo "Select which development environments to configure:"
    echo ""
    
    # Docker
    if yes_no_prompt "Configure Docker and Docker Compose?" "y"; then
        CONFIG_OPTIONS[ENABLE_DOCKER]="true"
        print_success "✓ Docker configured"
    else
        CONFIG_OPTIONS[ENABLE_DOCKER]="false"
    fi
    
    # Kubernetes
    if yes_no_prompt "Configure Kubernetes (kubectl, helm)?" "y"; then
        CONFIG_OPTIONS[ENABLE_KUBERNETES]="true"
        print_success "✓ Kubernetes configured"
    else
        CONFIG_OPTIONS[ENABLE_KUBERNETES]="false"
    fi
    
    # Cloud Tools
    if yes_no_prompt "Configure cloud tools (AWS, Google Cloud, Azure)?" "y"; then
        CONFIG_OPTIONS[ENABLE_CLOUD_TOOLS]="true"
        print_success "✓ Cloud tools configured"
    else
        CONFIG_OPTIONS[ENABLE_CLOUD_TOOLS]="false"
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 7. THEME & VISUAL CONFIGURATION                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

configure_theme() {
    clear_screen
    print_header
    print_section "Step 4: Visual Theme Configuration"
    
    if [[ "${CONFIG_OPTIONS[ENABLE_VISUAL]}" == "false" ]]; then
        echo "Visual enhancements are disabled."
        return 0
    fi
    
    echo "Select your preferred terminal theme:"
    echo ""
    
    local theme_idx
    theme_idx=$(numbered_menu "Choose theme:" \
        "Dark Theme (recommended for dark terminal)" \
        "Light Theme (recommended for light terminal)" \
        "Auto (detect based on system preferences)")
    
    case "$theme_idx" in
        0) CONFIG_OPTIONS[THEME]="dark" ;;
        1) CONFIG_OPTIONS[THEME]="light" ;;
        2) CONFIG_OPTIONS[THEME]="auto" ;;
    esac
    
    print_success "✓ Theme set to: ${CONFIG_OPTIONS[THEME]}"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 8. PERFORMANCE TUNING                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

configure_performance() {
    clear_screen
    print_header
    print_section "Step 5: Performance Tuning"
    
    if [[ "${CONFIG_OPTIONS[ENABLE_PERFORMANCE]}" == "false" ]]; then
        echo "Performance optimization is disabled."
        return 0
    fi
    
    echo "NEXUSPRO targets <50ms shell startup time through optimization."
    echo ""
    
    echo "Select performance profile:"
    echo ""
    
    local perf_idx
    perf_idx=$(numbered_menu "Performance Profile:" \
        "Maximum Performance (aggressive optimization)" \
        "Balanced (recommended)" \
        "Maximum Features (all features enabled)")
    
    case "$perf_idx" in
        0)
            CONFIG_OPTIONS[PERFORMANCE_TARGET]="30"
            print_success "✓ Performance target: 30ms (maximum)"
            ;;
        1)
            CONFIG_OPTIONS[PERFORMANCE_TARGET]="50"
            print_success "✓ Performance target: 50ms (balanced)"
            ;;
        2)
            CONFIG_OPTIONS[PERFORMANCE_TARGET]="100"
            print_success "✓ Performance target: 100ms (maximum features)"
            ;;
    esac
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 9. SUMMARY & CONFIRMATION                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

show_summary() {
    clear_screen
    print_header
    print_section "Configuration Summary"
    
    cat << EOF
Features:
  • Development Tools:     ${CONFIG_OPTIONS[ENABLE_DEVTOOLS]}
  • Aliases & Shortcuts:   ${CONFIG_OPTIONS[ENABLE_ALIASES]}
  • Visual Enhancements:   ${CONFIG_OPTIONS[ENABLE_VISUAL]}
  • Performance Optimize:  ${CONFIG_OPTIONS[ENABLE_PERFORMANCE]}
  • System Cleanup:        ${CONFIG_OPTIONS[ENABLE_CLEANUP]}

Package Manager:
  • Install Homebrew:      ${CONFIG_OPTIONS[INSTALL_HOMEBREW]}

Development Tools:
  • Docker & Compose:      ${CONFIG_OPTIONS[ENABLE_DOCKER]}
  • Kubernetes:            ${CONFIG_OPTIONS[ENABLE_KUBERNETES]}
  • Cloud Tools:           ${CONFIG_OPTIONS[ENABLE_CLOUD_TOOLS]}

Customization:
  • Theme:                 ${CONFIG_OPTIONS[THEME]}
  • Performance Target:    ${CONFIG_OPTIONS[PERFORMANCE_TARGET]}ms

EOF
    
    if yes_no_prompt "Apply these settings?" "y"; then
        save_configuration
        print_success "✓ Configuration saved"
        show_completion
    else
        echo -e "${YELLOW}Setup wizard cancelled.${NC}"
        exit 0
    fi
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 10. SAVE CONFIGURATION                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

save_configuration() {
    mkdir -p "$CONFIG_DIR"
    
    {
        echo "# NEXUSPRO Terminal System Configuration"
        echo "# Generated: $(date)"
        echo ""
        for key in "${!CONFIG_OPTIONS[@]}"; do
            echo "export CONFIG_${key}=\"${CONFIG_OPTIONS[$key]}\""
        done
    } > "$CONFIG_FILE"
    
    log "INFO" "Configuration saved to $CONFIG_FILE"
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 11. COMPLETION                                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

show_completion() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Setup Complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    cat << EOF
Your NEXUSPRO Terminal System is configured and ready!

Next steps:
1. Run the installer:
   bash ${SCRIPT_DIR}/install.sh

2. Restart your terminal or reload configuration:
   source ~/.zshrc

3. Explore available commands:
   • system_diagnostics - Show system information and status
   • show_startup_time - Display shell startup performance
   • pkg_list - List installed packages
   • path_show - Display current PATH configuration

For more information:
• Configuration file: $CONFIG_FILE
• Setup log: $WIZARD_LOG

Happy coding! 🚀

EOF
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 12. MAIN FLOW                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

main() {
    mkdir -p "$CONFIG_DIR"
    
    show_welcome
    configure_features
    configure_package_manager
    configure_dev_tools
    configure_theme
    configure_performance
    show_summary
}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║ 13. EXECUTION                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

main

################################################################################
# END OF SETUP-WIZARD.SH
################################################################################
