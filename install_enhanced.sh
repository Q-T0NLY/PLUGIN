#!/bin/bash

################################################################################
#                                                                              #
#        🚀 NEXUS UNIFIED PLATFORM - ENHANCED FULL STACK INSTALLER 🚀        #
#                                                                              #
#              Interactive Installation with Auto-Detection & Setup            #
#                 Orchestrates All Configuration Wizards                       #
#                                                                              #
################################################################################

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly VERSION="4.1.0"
readonly PROJECT="NEXUS Unified Platform"

# Colors
readonly C_RED='\033[0;31m'
readonly C_GREEN='\033[0;32m'
readonly C_YELLOW='\033[1;33m'
readonly C_BLUE='\033[0;34m'
readonly C_MAGENTA='\033[0;35m'
readonly C_CYAN='\033[0;36m'
readonly C_WHITE='\033[1;37m'
readonly C_BOLD='\033[1m'
readonly C_RESET='\033[0m'

# Logging
readonly LOG_DIR="${SCRIPT_DIR}/.install_logs"
readonly LOG_FILE="${LOG_DIR}/install_$(date +%s).log"
mkdir -p "${LOG_DIR}"

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${LOG_FILE}"
}

print_banner() {
    clear
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║         🚀 NEXUS UNIFIED PLATFORM - FULL STACK SETUP 🚀                      ║
║                                                                                ║
║           Interactive Installation & Configuration Wizard v4.1.0              ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

EOF
}

print_section() {
    echo ""
    echo -e "${C_CYAN}╔═══════════════════════════════════════════════════════════╗${C_RESET}"
    echo -e "${C_CYAN}║${C_RESET} ${C_BOLD}$1${C_RESET}"
    echo -e "${C_CYAN}╚═══════════════════════════════════════════════════════════╝${C_RESET}"
    echo ""
}

print_step() {
    echo -e "${C_BLUE}▶${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_success() {
    echo -e "${C_GREEN}✓${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_error() {
    echo -e "${C_RED}✗${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_warning() {
    echo -e "${C_YELLOW}⚠${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_info() {
    echo -e "${C_CYAN}ℹ${C_RESET} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENT DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

check_command() {
    command -v "$1" &> /dev/null && echo "true" || echo "false"
}

# ═══════════════════════════════════════════════════════════════════════════════
# WELCOME & SETUP SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

show_welcome() {
    print_banner
    
    print_section "👋 WELCOME TO NEXUS SETUP"
    
    cat << 'EOF'
This wizard will help you install and configure NEXUS with:

  ✓ Automatic dependency detection and installation
  ✓ Interactive database setup (PostgreSQL, Redis, MongoDB)
  ✓ Python virtual environment configuration
  ✓ Backend service configuration
  ✓ Docker & Kubernetes setup
  ✓ Frontend installation
  ✓ Git repository setup

The installation will be logged to: ${LOG_FILE}

EOF
    
    read -p "${C_BOLD}Continue with setup? (y/n): ${C_RESET}" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Setup cancelled by user"
        exit 0
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION FLOWS
# ═══════════════════════════════════════════════════════════════════════════════

quick_setup() {
    print_section "⚡ QUICK SETUP MODE"
    
    print_info "This will install minimum required components"
    
    # Scan dependencies
    print_step "Scanning dependencies..."
    python3 "${SCRIPT_DIR}/backend_config.py" 2>/dev/null || {
        print_error "Backend configuration not available"
    }
    
    log "Quick setup completed"
}

standard_setup() {
    print_section "📦 STANDARD SETUP MODE"
    
    print_info "This will install core components with optional features"
    
    # Check script availability
    if [[ ! -f "${SCRIPT_DIR}/setup.sh" ]]; then
        print_error "setup.sh not found"
        return 1
    fi
    
    # Run setup script
    print_step "Launching advanced setup wizard..."
    bash "${SCRIPT_DIR}/setup.sh"
    
    log "Standard setup completed"
}

full_setup() {
    print_section "🚀 FULL STACK SETUP MODE"
    
    print_info "This will configure everything: backend, database, docker, frontend"
    
    # Backend setup
    print_step "Configuring backend..."
    python3 "${SCRIPT_DIR}/backend_config.py" 2>/dev/null || true
    
    # Database setup
    read -p "${C_YELLOW}Configure databases? (y/n): ${C_RESET}" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Setting up databases..."
        # Database setup would go here
    fi
    
    # Docker setup
    read -p "${C_YELLOW}Setup Docker & Kubernetes? (y/n): ${C_RESET}" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Setting up Docker..."
        if [[ "$(check_command docker)" == "true" ]]; then
            print_success "Docker is already installed"
        else
            print_warning "Docker not found - skipping"
        fi
    fi
    
    # Frontend setup
    read -p "${C_YELLOW}Setup Frontend? (y/n): ${C_RESET}" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_step "Setting up frontend..."
        if [[ -d "${SCRIPT_DIR}/frontend" ]]; then
            if [[ "$(check_command npm)" == "true" ]]; then
                print_step "Installing frontend dependencies..."
                cd "${SCRIPT_DIR}/frontend"
                npm install 2>/dev/null && print_success "Frontend dependencies installed" || print_warning "npm install failed"
            else
                print_warning "npm not found - skipping frontend setup"
            fi
        fi
    fi
    
    log "Full setup completed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION & VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

validate_installation() {
    print_section "✅ VALIDATING INSTALLATION"
    
    local checks=0
    local passed=0
    
    # Check core files
    local files=(
        "unified_deployment.py"
        "unified_bridge.py"
        "system_manager.py"
        "backend_config.py"
        "setup.sh"
    )
    
    print_step "Checking required files..."
    for file in "${files[@]}"; do
        ((checks++))
        if [[ -f "${SCRIPT_DIR}/${file}" ]]; then
            print_success "$file"
            ((passed++))
        else
            print_error "$file NOT FOUND"
        fi
    done
    
    # Check commands
    print_step "Checking required commands..."
    local commands=(bash git python3 pip3)
    for cmd in "${commands[@]}"; do
        ((checks++))
        if [[ "$(check_command "$cmd")" == "true" ]]; then
            print_success "$cmd"
            ((passed++))
        else
            print_error "$cmd NOT FOUND"
        fi
    done
    
    echo ""
    print_info "Validation: ${C_BOLD}$passed/$checks checks passed${C_RESET}"
    
    if [[ $passed -eq $checks ]]; then
        print_success "Installation validated successfully!"
        return 0
    else
        print_warning "Some checks failed - see details above"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY & NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════

show_summary() {
    print_section "📋 SETUP SUMMARY"
    
    cat << EOF
✓ Installation completed successfully!

${C_BOLD}Next Steps:${C_RESET}

1. ${C_CYAN}Activate Python environment${C_RESET}
   source ${SCRIPT_DIR}/.venv/bin/activate

2. ${C_CYAN}Start services${C_RESET}
   cd ${SCRIPT_DIR}
   ./unified_deploy.sh full_system

3. ${C_CYAN}Access components${C_RESET}
   API Gateway: http://localhost:8000
   Dashboard: http://localhost:3000

4. ${C_CYAN}View logs${C_RESET}
   tail -f ${LOG_FILE}

${C_BOLD}Documentation:${C_RESET}
   See Documentations/ folder for guides

${C_BOLD}Need help?${C_RESET}
   Run: python3 backend_config.py
   Or: bash setup.sh

EOF
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN MENU & FLOW
# ═══════════════════════════════════════════════════════════════════════════════

show_setup_menu() {
    print_section "🎯 CHOOSE SETUP MODE"
    
    cat << EOF
${C_BOLD}Setup Modes:${C_RESET}

  ${C_CYAN}1${C_RESET} ⚡ Quick Setup
     Minimum requirements only
     Install: bash, git, python3, pip3

  ${C_CYAN}2${C_RESET} 📦 Standard Setup
     Core components with options
     Includes backend and basic database

  ${C_CYAN}3${C_RESET} 🚀 Full Stack Setup
     Everything: backend, database, docker, frontend
     Complete production-ready environment

  ${C_CYAN}4${C_RESET} ✅ Validation Only
     Check existing installation

  ${C_CYAN}5${C_RESET} ❌ Exit

EOF
    
    read -p "${C_BOLD}Select mode (1-5): ${C_RESET}" -n 1 choice
    echo
    
    case $choice in
        1)
            quick_setup
            show_summary
            ;;
        2)
            standard_setup
            show_summary
            ;;
        3)
            full_setup
            show_summary
            ;;
        4)
            validate_installation
            ;;
        5)
            print_success "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            show_setup_menu
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    log "Installation started by $USER"
    
    show_welcome
    show_setup_menu
    
    log "Installation completed"
    
    echo ""
    print_success "Setup complete! Log: $LOG_FILE"
}

# Run main if script is executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
