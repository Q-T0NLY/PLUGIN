#!/bin/bash

################################################################################
#                                                                              #
#          🚀 NEXUS UNIFIED PLATFORM - FULL STACK SETUP & CONFIGURATION 🚀  #
#                                                                              #
#    Interactive Installation Wizard with Auto-Detection & Configuration     #
#              Supports Linux, macOS, and Container Environments              #
#                                                                              #
################################################################################

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION & COLORS
# ═══════════════════════════════════════════════════════════════════════════════

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SETUP_VERSION="4.1.0"
readonly PROJECT_NAME="NEXUS Unified Platform"

# Color Palette
readonly C_RED='\033[0;31m'
readonly C_GREEN='\033[0;32m'
readonly C_YELLOW='\033[1;33m'
readonly C_BLUE='\033[0;34m'
readonly C_MAGENTA='\033[0;35m'
readonly C_CYAN='\033[0;36m'
readonly C_WHITE='\033[1;37m'
readonly C_GRAY='\033[0;37m'
readonly C_BOLD='\033[1m'
readonly C_RESET='\033[0m'

# Log & Config
readonly LOG_DIR="${SCRIPT_DIR}/.setup_logs"
readonly LOG_FILE="${LOG_DIR}/setup_$(date +%s).log"
readonly CONFIG_DIR="${HOME}/.config/nexus"
readonly SETUP_STATE="${CONFIG_DIR}/.setup_state"
readonly DEPS_JSON="${CONFIG_DIR}/dependencies.json"

# Create necessary directories
mkdir -p "${LOG_DIR}" "${CONFIG_DIR}"

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING & OUTPUT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${LOG_FILE}"
}

print_banner() {
    clear
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║             🚀 NEXUS UNIFIED PLATFORM - FULL STACK SETUP 🚀                  ║
║                                                                                ║
║              Interactive Installation & Configuration Wizard                  ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

EOF
}

print_section() {
    echo ""
    echo -e "${C_CYAN}┌─────────────────────────────────────────────────────────────────┐${C_RESET}"
    echo -e "${C_CYAN}│${C_RESET} ${C_BOLD}$1${C_RESET}"
    echo -e "${C_CYAN}└─────────────────────────────────────────────────────────────────┘${C_RESET}"
    echo ""
}

print_step() {
    echo -e "${C_BLUE}▶${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_success() {
    echo -e "${C_GREEN}✓${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_warning() {
    echo -e "${C_YELLOW}⚠${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_error() {
    echo -e "${C_RED}✗${C_RESET} ${C_BOLD}$1${C_RESET}"
}

print_info() {
    echo -e "${C_CYAN}ℹ${C_RESET} $1"
}

print_progress() {
    echo -ne "${C_MAGENTA}⟳${C_RESET} $1\r"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ -f /.dockerenv ]]; then
        echo "docker"
    else
        echo "unknown"
    fi
}

detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        echo "${ID}"
    else
        echo "unknown"
    fi
}

detect_arch() {
    uname -m
}

get_system_info() {
    local os=$(detect_os)
    local arch=$(detect_arch)
    local distro=""
    
    [[ "$os" == "linux" ]] && distro=$(detect_distro)
    
    cat > "${SETUP_STATE}" << EOF
{
    "os": "$os",
    "arch": "$arch",
    "distro": "$distro",
    "detected_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    
    log "System detected: OS=$os, ARCH=$arch, DISTRO=$distro"
}

# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

check_command() {
    if command -v "$1" &> /dev/null; then
        echo "installed"
    else
        echo "missing"
    fi
}

get_command_version() {
    local cmd="$1"
    if command -v "$cmd" &> /dev/null; then
        $cmd --version 2>/dev/null | head -1 || echo "unknown"
    else
        echo "not_installed"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# DEPENDENCY SCANNING
# ═══════════════════════════════════════════════════════════════════════════════

declare -A REQUIRED_DEPS=(
    [bash]="3.0"
    [curl]="7.0"
    [git]="2.0"
    [python3]="3.8"
    [pip3]="20.0"
)

declare -A OPTIONAL_DEPS=(
    [docker]="19.0"
    [kubectl]="1.15"
    [postgres]="11.0"
    [redis]="5.0"
    [nodejs]="12.0"
    [npm]="6.0"
    [zsh]="5.0"
)

declare -A PYTHON_PACKAGES=(
    [pip]="latest"
    [setuptools]="latest"
    [wheel]="latest"
    [virtualenv]="latest"
    [pytest]="latest"
    [pylint]="latest"
)

scan_dependencies() {
    print_section "🔍 SCANNING SYSTEM DEPENDENCIES"
    
    local deps_data='{"required": {}, "optional": {}, "python_packages": {}}'
    
    # Scan required dependencies
    print_step "Checking required dependencies..."
    for dep in "${!REQUIRED_DEPS[@]}"; do
        local status=$(check_command "$dep")
        local version=$(get_command_version "$dep")
        
        echo "  $dep: $status ($version)"
        log "Dependency scan: $dep = $status ($version)"
        
        if [[ "$status" == "installed" ]]; then
            print_success "$dep is installed ($version)"
        else
            print_warning "$dep is NOT installed"
        fi
    done
    
    echo ""
    print_step "Checking optional dependencies..."
    for dep in "${!OPTIONAL_DEPS[@]}"; do
        local status=$(check_command "$dep")
        local version=$(get_command_version "$dep")
        
        echo "  $dep: $status ($version)"
        
        if [[ "$status" == "installed" ]]; then
            print_success "$dep is installed ($version)"
        else
            print_info "$dep not found (optional)"
        fi
    done
}

# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MENU SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

show_menu() {
    local title="$1"
    local -a options=("${@:2}")
    
    echo ""
    print_section "$title"
    
    for i in "${!options[@]}"; do
        echo "  ${C_CYAN}$(($i + 1))${C_RESET} ${options[$i]}"
    done
    
    echo ""
    read -p "Select option (1-${#options[@]}): " choice
    
    if [[ $choice =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#options[@]} )); then
        return $((choice - 1))
    else
        print_error "Invalid selection"
        return -1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALLATION HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

install_with_apt() {
    local packages="$*"
    print_step "Installing via apt: $packages"
    
    if sudo -n true 2>/dev/null; then
        sudo apt update -qq
        sudo apt install -y $packages
    else
        print_error "sudo access required but not available"
        read -p "Enter sudo password: " -s passwd
        echo "$passwd" | sudo -S apt update -qq
        echo "$passwd" | sudo -S apt install -y $packages
    fi
}

install_with_brew() {
    local packages="$*"
    print_step "Installing via brew: $packages"
    brew install $packages
}

install_with_pip() {
    local packages="$*"
    print_step "Installing Python packages: $packages"
    pip3 install --upgrade $packages
}

install_docker() {
    print_section "🐳 INSTALLING DOCKER"
    
    if [[ "$(detect_os)" == "linux" ]]; then
        install_with_apt docker.io
        sudo usermod -aG docker $USER
        print_success "Docker installed and user added to docker group"
    elif [[ "$(detect_os)" == "macos" ]]; then
        print_info "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
        read -p "Press Enter once Docker is installed..."
    fi
    
    log "Docker installation completed"
}

install_kubernetes() {
    print_section "☸️  INSTALLING KUBERNETES (kubectl)"
    
    if [[ "$(detect_os)" == "linux" ]]; then
        print_step "Installing kubectl via curl..."
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    elif [[ "$(detect_os)" == "macos" ]]; then
        install_with_brew kubectl
    fi
    
    print_success "kubectl installed"
    log "Kubernetes installation completed"
}

install_database() {
    local db_type="$1"
    print_section "🗄️  INSTALLING DATABASE: $db_type"
    
    case "$db_type" in
        postgresql)
            if [[ "$(detect_os)" == "linux" ]]; then
                install_with_apt postgresql postgresql-contrib
            elif [[ "$(detect_os)" == "macos" ]]; then
                install_with_brew postgresql
            fi
            print_success "PostgreSQL installed"
            ;;
        redis)
            if [[ "$(detect_os)" == "linux" ]]; then
                install_with_apt redis-server
            elif [[ "$(detect_os)" == "macos" ]]; then
                install_with_brew redis
            fi
            print_success "Redis installed"
            ;;
        mongodb)
            if [[ "$(detect_os)" == "linux" ]]; then
                install_with_apt mongodb
            elif [[ "$(detect_os)" == "macos" ]]; then
                install_with_brew mongodb-community
            fi
            print_success "MongoDB installed"
            ;;
    esac
    
    log "Database installation completed: $db_type"
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION WIZARDS
# ═══════════════════════════════════════════════════════════════════════════════

configure_database() {
    local db_type="$1"
    print_section "⚙️  CONFIGURING $db_type"
    
    case "$db_type" in
        postgresql)
            print_step "PostgreSQL Configuration"
            read -p "Database name [nexus_db]: " db_name
            db_name="${db_name:-nexus_db}"
            read -p "Database user [nexus_user]: " db_user
            db_user="${db_user:-nexus_user}"
            read -sp "Database password: " db_pass
            echo ""
            
            print_info "Creating PostgreSQL database..."
            sudo -u postgres createdb "$db_name" 2>/dev/null || true
            sudo -u postgres createuser "$db_user" 2>/dev/null || true
            
            cat > "${CONFIG_DIR}/postgresql.env" << EOF
DB_NAME=$db_name
DB_USER=$db_user
DB_PASSWORD=$db_pass
DB_HOST=localhost
DB_PORT=5432
EOF
            
            print_success "PostgreSQL configured"
            ;;
            
        redis)
            print_step "Redis Configuration"
            read -p "Redis port [6379]: " redis_port
            redis_port="${redis_port:-6379}"
            read -p "Redis password (optional): " redis_pass
            
            cat > "${CONFIG_DIR}/redis.env" << EOF
REDIS_HOST=localhost
REDIS_PORT=$redis_port
REDIS_PASSWORD=$redis_pass
EOF
            
            print_success "Redis configured"
            ;;
    esac
    
    log "Database configuration completed: $db_type"
}

configure_python_env() {
    print_section "🐍 PYTHON ENVIRONMENT CONFIGURATION"
    
    print_step "Creating Python virtual environment..."
    python3 -m venv "${SCRIPT_DIR}/.venv"
    source "${SCRIPT_DIR}/.venv/bin/activate"
    
    print_step "Upgrading pip and installing tools..."
    pip install --upgrade pip setuptools wheel
    
    print_step "Installing Python dependencies..."
    if [[ -f "${SCRIPT_DIR}/cli/requirements.txt" ]]; then
        pip install -r "${SCRIPT_DIR}/cli/requirements.txt"
    fi
    
    if [[ -f "${SCRIPT_DIR}/services/api_gateway/requirements.txt" ]]; then
        pip install -r "${SCRIPT_DIR}/services/api_gateway/requirements.txt"
    fi
    
    print_success "Python environment configured"
    log "Python environment setup completed"
}

configure_git_repo() {
    print_section "🔧 GIT REPOSITORY CONFIGURATION"
    
    print_step "Configuring git settings..."
    read -p "Git user name: " git_name
    read -p "Git email: " git_email
    
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    
    print_step "Setting up git hooks..."
    mkdir -p "${SCRIPT_DIR}/.git/hooks"
    
    print_success "Git configured"
    log "Git configuration completed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP WIZARDS
# ═══════════════════════════════════════════════════════════════════════════════

backend_setup() {
    print_section "⚙️  BACKEND SETUP WIZARD"
    
    # Python Environment
    if [[ ! -d "${SCRIPT_DIR}/.venv" ]]; then
        read -p "Create Python virtual environment? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            configure_python_env
        fi
    fi
    
    # Database Selection
    print_step "Select database(s) to configure:"
    local dbs=("PostgreSQL" "Redis" "MongoDB" "Skip")
    
    while true; do
        show_menu "Database Selection" "${dbs[@]}"
        local choice=$?
        
        if [[ $choice -eq 3 ]]; then
            break
        elif [[ $choice -ne -1 ]]; then
            case $choice in
                0)
                    if [[ $(check_command postgresql) == "missing" ]]; then
                        read -p "PostgreSQL not found. Install? (y/n): " -n 1 -r
                        echo
                        [[ $REPLY =~ ^[Yy]$ ]] && install_database postgresql
                    fi
                    configure_database postgresql
                    ;;
                1)
                    if [[ $(check_command redis-server) == "missing" ]]; then
                        read -p "Redis not found. Install? (y/n): " -n 1 -r
                        echo
                        [[ $REPLY =~ ^[Yy]$ ]] && install_database redis
                    fi
                    configure_database redis
                    ;;
                2)
                    if [[ $(check_command mongod) == "missing" ]]; then
                        read -p "MongoDB not found. Install? (y/n): " -n 1 -r
                        echo
                        [[ $REPLY =~ ^[Yy]$ ]] && install_database mongodb
                    fi
                    print_info "MongoDB configuration (manual setup recommended)"
                    ;;
            esac
        fi
    done
}

docker_setup() {
    print_section "🐳 DOCKER & CONTAINER SETUP"
    
    if [[ $(check_command docker) == "missing" ]]; then
        read -p "Docker not installed. Install? (y/n): " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && install_docker
    else
        print_success "Docker is installed"
    fi
    
    if [[ $(check_command kubectl) == "missing" ]]; then
        read -p "Kubernetes not installed. Install? (y/n): " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && install_kubernetes
    else
        print_success "Kubernetes is installed"
    fi
    
    print_info "Building Docker images..."
    if [[ -f "${SCRIPT_DIR}/infrastructure/docker-compose.yml" ]]; then
        print_step "Found docker-compose.yml"
        read -p "Build and start containers? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "${SCRIPT_DIR}"
            docker-compose -f infrastructure/docker-compose.yml build
            print_success "Docker images built"
        fi
    fi
    
    log "Docker setup completed"
}

frontend_setup() {
    print_section "🎨 FRONTEND SETUP"
    
    if [[ ! -d "${SCRIPT_DIR}/frontend" ]]; then
        print_info "Frontend directory not found"
        return
    fi
    
    if [[ $(check_command npm) == "missing" ]] && [[ $(check_command node) == "missing" ]]; then
        read -p "Node.js/npm not found. Install? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if [[ "$(detect_os)" == "linux" ]]; then
                install_with_apt nodejs npm
            elif [[ "$(detect_os)" == "macos" ]]; then
                install_with_brew node
            fi
        fi
    fi
    
    if [[ -f "${SCRIPT_DIR}/frontend/package.json" ]]; then
        print_step "Installing frontend dependencies..."
        cd "${SCRIPT_DIR}/frontend"
        npm install
        print_success "Frontend dependencies installed"
    fi
    
    log "Frontend setup completed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SETUP FLOW
# ═══════════════════════════════════════════════════════════════════════════════

main_menu() {
    while true; do
        print_banner
        
        print_section "📋 MAIN SETUP MENU"
        
        local options=(
            "🔍 Scan Dependencies"
            "⚙️  Backend Setup (Python, Databases)"
            "🐳 Docker & Kubernetes Setup"
            "🎨 Frontend Setup (Node.js, npm)"
            "🔧 Git Configuration"
            "🚀 Full Stack Setup (All Options)"
            "📊 View System Information"
            "📋 View Logs"
            "✅ Validate Installation"
            "❌ Exit"
        )
        
        show_menu "What would you like to do?" "${options[@]}"
        local choice=$?
        
        if [[ $choice -eq -1 ]]; then
            continue
        fi
        
        case $choice in
            0) scan_dependencies ;;
            1) backend_setup ;;
            2) docker_setup ;;
            3) frontend_setup ;;
            4) configure_git_repo ;;
            5)
                get_system_info
                scan_dependencies
                backend_setup
                docker_setup
                frontend_setup
                configure_git_repo
                ;;
            6)
                print_section "📊 SYSTEM INFORMATION"
                echo "OS: $(detect_os)"
                echo "Architecture: $(detect_arch)"
                echo "Distro: $(detect_distro)"
                echo "Bash: $(bash --version | head -1)"
                echo "Python: $(python3 --version 2>&1)"
                echo "Git: $(git --version)"
                echo "Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
                echo ""
                read -p "Press Enter to continue..."
                ;;
            7)
                print_section "📋 SETUP LOGS"
                tail -50 "${LOG_FILE}"
                echo ""
                read -p "Press Enter to continue..."
                ;;
            8)
                print_section "✅ VALIDATING INSTALLATION"
                print_step "Running validation checks..."
                
                local checks=0
                local passed=0
                
                for dep in "${!REQUIRED_DEPS[@]}"; do
                    ((checks++))
                    if [[ $(check_command "$dep") == "installed" ]]; then
                        print_success "$dep is installed"
                        ((passed++))
                    else
                        print_error "$dep is NOT installed"
                    fi
                done
                
                echo ""
                print_info "Validation: $passed/$checks checks passed"
                read -p "Press Enter to continue..."
                ;;
            9)
                print_success "Setup wizard completed. Exiting..."
                log "Setup wizard exited by user"
                exit 0
                ;;
        esac
    done
}

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Ensure we're running bash
    if [[ -z "${BASH_VERSION:-}" ]]; then
        echo "This script must be run with bash, not sh"
        exit 1
    fi
    
    log "Setup wizard started by $USER"
    print_banner
    get_system_info
    main_menu
fi
