#!/bin/bash
# ============================================================================
# 🍎 Enhanced macOS Version Spoofer - Bash Implementation
# Advanced system compatibility layer with multi-strategy spoofing
# ============================================================================

set -euo pipefail

# Color palette for output
readonly C_CYAN='\033[38;2;0;212;255m'
readonly C_PURP='\033[38;2;123;97;255m'
readonly C_GREEN='\033[38;2;0;245;160m'
readonly C_YELLOW='\033[38;2;255;215;0m'
readonly C_RED='\033[38;2;255;59;48m'
readonly C_BLUE='\033[38;2;10;132;255m'
readonly C_BOLD='\033[1m'
readonly C_RESET='\033[0m'

# Spoof configuration directory
SPOOF_DIR="${HOME}/.nexus/spoof"
SPOOF_CONFIG="${SPOOF_DIR}/spoof_config.json"
SPOOF_HISTORY="${SPOOF_DIR}/spoof_history.log"
BACKUP_DIR="${SPOOF_DIR}/backups"

# ============================================================================
# INITIALIZATION
# ============================================================================
initialize_spoof_environment() {
    echo -e "${C_CYAN}${C_BOLD}🍎 Initializing macOS Version Spoofer${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}"
    
    mkdir -p "${SPOOF_DIR}" "${BACKUP_DIR}"
    
    # Create version profiles database
    create_version_profiles_db
    
    echo -e "${C_GREEN}✅ Spoof environment initialized at ${SPOOF_DIR}${C_RESET}\n"
}

# ============================================================================
# VERSION PROFILES DATABASE
# ============================================================================
create_version_profiles_db() {
    cat > "${SPOOF_CONFIG}" << 'EOF'
{
  "versions": {
    "11.7.10": {
      "name": "macOS Big Sur",
      "build": "20G1120",
      "kernel": "20.6.0",
      "webkit": "611.1.1",
      "release_date": "2020-11-12",
      "eol_date": "2023-09-12",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.216 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_10) AppleWebKit/611.1.1 (KHTML, like Gecko) Version/14.1.1 Safari/611.1.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.7.10) Gecko/20100101 Firefox/123.0"
      }
    },
    "12.7.1": {
      "name": "macOS Monterey",
      "build": "21G920",
      "kernel": "21.6.0",
      "webkit": "612.1.1",
      "release_date": "2021-10-25",
      "eol_date": "2024-09-16",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.184 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) AppleWebKit/612.1.1 (KHTML, like Gecko) Version/15.1.1 Safari/612.1.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.7.1) Gecko/20100101 Firefox/123.0"
      }
    },
    "13.6.1": {
      "name": "macOS Ventura",
      "build": "22G313",
      "kernel": "22.6.0",
      "webkit": "613.1.1",
      "release_date": "2022-10-24",
      "eol_date": "2025-09-30",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1) AppleWebKit/613.1.1 (KHTML, like Gecko) Version/16.1.1 Safari/613.1.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.6.1) Gecko/20100101 Firefox/123.0"
      }
    },
    "14.6.1": {
      "name": "macOS Sonoma",
      "build": "23G80",
      "kernel": "23.6.0",
      "webkit": "614.1.1",
      "release_date": "2023-09-26",
      "eol_date": "2026-09-30",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/614.1.1 (KHTML, like Gecko) Version/17.6.1 Safari/614.1.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6.1) Gecko/20100101 Firefox/123.0"
      }
    },
    "15.1": {
      "name": "macOS Sequoia",
      "build": "24B83",
      "kernel": "24.1.0",
      "webkit": "615.1.1",
      "release_date": "2024-09-16",
      "eol_date": "2027-09-30",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_1) AppleWebKit/615.1.1 (KHTML, like Gecko) Version/18.1 Safari/615.1.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15.1) Gecko/20100101 Firefox/124.0"
      }
    },
    "15.2.1": {
      "name": "macOS Sequoia Latest",
      "build": "24C101",
      "kernel": "24.2.0",
      "webkit": "615.2.1",
      "release_date": "2024-12-09",
      "eol_date": "2027-09-30",
      "browsers": {
        "chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36",
        "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_2_1) AppleWebKit/615.2.1 (KHTML, like Gecko) Version/18.2 Safari/615.2.1",
        "firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15.2.1) Gecko/20100101 Firefox/124.0"
      }
    }
  },
  "compatibility_mode": "adaptive",
  "auto_detection": true,
  "persistence_level": "multi_layer"
}
EOF
}

# ============================================================================
# ENVIRONMENT VARIABLE SPOOFING
# ============================================================================
spoof_via_environment() {
    local target_version="$1"
    
    echo -e "${C_BLUE}[1/4] Applying Environment Variable Spoof${C_RESET}"
    
    # Extract version data from config
    local version_data=$(jq ".versions.\"${target_version}\"" "${SPOOF_CONFIG}")
    local name=$(echo "$version_data" | jq -r '.name')
    local build=$(echo "$version_data" | jq -r '.build')
    local kernel=$(echo "$version_data" | jq -r '.kernel')
    
    # Set environment variables
    export SYSTEM_VERSION_COMPAT=1
    export SW_VERS_PRODUCTVERSION="${target_version}"
    export SW_VERS_BUILDVERSION="${build}"
    export MACOS_VERSION="${target_version}"
    export MACOS_BUILD="${build}"
    export MACOS_NAME="${name}"
    export MACOS_KERNEL="${kernel}"
    
    # Persist to shell profile
    local profile_file="${HOME}/.zshrc"
    if [[ -f "${profile_file}" ]]; then
        # Remove existing exports
        sed -i.bak '/^export SYSTEM_VERSION_COMPAT/d; /^export SW_VERS/d; /^export MACOS_/d' "${profile_file}"
        
        # Add new exports
        cat >> "${profile_file}" << ENVEOF
# macOS Spoof Environment Variables (Applied: $(date))
export SYSTEM_VERSION_COMPAT=1
export SW_VERS_PRODUCTVERSION="${target_version}"
export SW_VERS_BUILDVERSION="${build}"
export MACOS_VERSION="${target_version}"
export MACOS_BUILD="${build}"
export MACOS_NAME="${name}"
export MACOS_KERNEL="${kernel}"
ENVEOF
    fi
    
    echo -e "${C_GREEN}  ✅ Environment variables set${C_RESET}"
}

# ============================================================================
# USER-AGENT SPOOFING
# ============================================================================
spoof_via_user_agent() {
    local target_version="$1"
    
    echo -e "${C_BLUE}[2/4] Applying User-Agent Spoof${C_RESET}"
    
    local version_data=$(jq ".versions.\"${target_version}\"" "${SPOOF_CONFIG}")
    local chrome_ua=$(echo "$version_data" | jq -r '.browsers.chrome')
    local safari_ua=$(echo "$version_data" | jq -r '.browsers.safari')
    local firefox_ua=$(echo "$version_data" | jq -r '.browsers.firefox')
    
    # Create HTTP headers file
    cat > "${SPOOF_DIR}/http_headers.json" << HEADERSEOF
{
  "user_agent": "${safari_ua}",
  "chrome_user_agent": "${chrome_ua}",
  "safari_user_agent": "${safari_ua}",
  "firefox_user_agent": "${firefox_ua}",
  "accept_language": "en-US,en;q=0.9",
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "accept_encoding": "gzip, deflate, br",
  "dnt": "1",
  "connection": "keep-alive",
  "upgrade_insecure_requests": "1",
  "sec_fetch_dest": "document",
  "sec_fetch_mode": "navigate",
  "sec_fetch_site": "none"
}
HEADERSEOF
    
    echo -e "${C_GREEN}  ✅ User-Agent headers configured${C_RESET}"
}

# ============================================================================
# BROWSER PROFILE SPOOFING
# ============================================================================
spoof_via_browser_profile() {
    local target_version="$1"
    
    echo -e "${C_BLUE}[3/4] Applying Browser Profile Spoof${C_RESET}"
    
    local version_data=$(jq ".versions.\"${target_version}\"" "${SPOOF_CONFIG}")
    
    mkdir -p "${SPOOF_DIR}/browsers"
    
    # Chrome profile
    jq '.browsers' "${SPOOF_CONFIG}" | jq "{
      user_agent: .chrome,
      webkit_version: \"615.1.1\",
      macos_version: \"${target_version}\",
      cpu_type: \"arm64\",
      chip_model: \"Apple Silicon M1\"
    }" > "${SPOOF_DIR}/browsers/chrome_profile.json"
    
    # Firefox profile
    jq '.browsers' "${SPOOF_CONFIG}" | jq "{
      user_agent: .firefox,
      platform: \"MacIntel\",
      os_version: \"${target_version}\",
      build_id: \"${build}\"
    }" > "${SPOOF_DIR}/browsers/firefox_profile.json"
    
    # Safari profile
    jq '.browsers' "${SPOOF_CONFIG}" | jq "{
      user_agent: .safari,
      webkit_version: \"615.1.1\",
      macos_version: \"${target_version}\"
    }" > "${SPOOF_DIR}/browsers/safari_profile.json"
    
    echo -e "${C_GREEN}  ✅ Browser profiles configured${C_RESET}"
}

# ============================================================================
# SYSTEM DEFAULTS SPOOFING
# ============================================================================
spoof_via_defaults() {
    local target_version="$1"
    
    echo -e "${C_BLUE}[4/4] Applying System Defaults Spoof${C_RESET}"
    
    local version_data=$(jq ".versions.\"${target_version}\"" "${SPOOF_CONFIG}")
    local build=$(echo "$version_data" | jq -r '.build')
    
    # Backup current defaults
    defaults read > "${BACKUP_DIR}/macos_defaults_backup_$(date +%s).plist" 2>/dev/null || true
    
    # Apply spoofed defaults
    defaults write NSGlobalDomain MacOSVersionCompat -string "1" 2>/dev/null || true
    defaults write com.apple.systempreferences SystemVersionString -string "${target_version}" 2>/dev/null || true
    
    echo -e "${C_GREEN}  ✅ System defaults configured${C_RESET}"
}

# ============================================================================
# COMPREHENSIVE SPOOF ACTIVATION
# ============================================================================
activate_comprehensive_spoof() {
    local target_version="$1"
    
    if ! jq ".versions.\"${target_version}\"" "${SPOOF_CONFIG}" > /dev/null 2>&1; then
        echo -e "${C_RED}❌ Unknown macOS version: ${target_version}${C_RESET}"
        list_available_versions
        return 1
    fi
    
    local version_name=$(jq -r ".versions.\"${target_version}\".name" "${SPOOF_CONFIG}")
    
    echo -e "\n${C_CYAN}${C_BOLD}🍎 Activating Comprehensive macOS Spoof${C_RESET}"
    echo -e "${C_YELLOW}Target: ${version_name} (${target_version})${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    spoof_via_environment "$target_version"
    spoof_via_user_agent "$target_version"
    spoof_via_browser_profile "$target_version"
    spoof_via_defaults "$target_version"
    
    # Log operation
    log_spoof_operation "ACTIVATE" "$target_version" "$version_name"
    
    echo -e "\n${C_GREEN}${C_BOLD}✅ Comprehensive spoof activated for ${version_name}${C_RESET}"
    echo -e "${C_CYAN}Spoof directory: ${SPOOF_DIR}${C_RESET}\n"
}

# ============================================================================
# ROLLBACK SPOOF
# ============================================================================
rollback_comprehensive_spoof() {
    echo -e "\n${C_CYAN}${C_BOLD}🔄 Rolling Back macOS Spoof${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    # Remove environment variables
    echo -e "${C_BLUE}[1/2] Removing Environment Variables${C_RESET}"
    unset SYSTEM_VERSION_COMPAT SW_VERS_PRODUCTVERSION SW_VERS_BUILDVERSION
    unset MACOS_VERSION MACOS_BUILD MACOS_NAME MACOS_KERNEL
    
    # Clean shell profile
    if [[ -f "${HOME}/.zshrc" ]]; then
        sed -i.bak '/^export SYSTEM_VERSION_COMPAT/d; /^export SW_VERS/d; /^export MACOS_/d' "${HOME}/.zshrc"
        echo -e "${C_GREEN}  ✅ Shell profile cleaned${C_RESET}"
    fi
    
    # Remove spoof files
    echo -e "${C_BLUE}[2/2] Removing Spoof Artifacts${C_RESET}"
    rm -f "${SPOOF_DIR}/http_headers.json"
    rm -rf "${SPOOF_DIR}/browsers"
    echo -e "${C_GREEN}  ✅ Spoof artifacts removed${C_RESET}"
    
    # Log operation
    log_spoof_operation "ROLLBACK" "" "All active spoofs"
    
    echo -e "\n${C_GREEN}${C_BOLD}✅ All spoofing strategies deactivated${C_RESET}\n"
}

# ============================================================================
# VERIFICATION
# ============================================================================
verify_spoof_status() {
    echo -e "\n${C_CYAN}${C_BOLD}🔍 Verifying Spoof Status${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    # Check environment variables
    echo -e "${C_BLUE}Environment Variables:${C_RESET}"
    if [[ -n "${SYSTEM_VERSION_COMPAT:-}" ]]; then
        echo -e "  🟢 SYSTEM_VERSION_COMPAT=${SYSTEM_VERSION_COMPAT}"
    else
        echo -e "  🔴 SYSTEM_VERSION_COMPAT not set"
    fi
    
    if [[ -n "${MACOS_VERSION:-}" ]]; then
        echo -e "  🟢 MACOS_VERSION=${MACOS_VERSION}"
    else
        echo -e "  🔴 MACOS_VERSION not set"
    fi
    
    # Check configuration files
    echo -e "\n${C_BLUE}Configuration Files:${C_RESET}"
    [[ -f "${SPOOF_DIR}/http_headers.json" ]] && echo -e "  🟢 HTTP headers configured" || echo -e "  🔴 HTTP headers not found"
    [[ -d "${SPOOF_DIR}/browsers" ]] && echo -e "  🟢 Browser profiles available" || echo -e "  🔴 Browser profiles not found"
    
    echo ""
}

# ============================================================================
# LISTING & INFORMATION
# ============================================================================
list_available_versions() {
    echo -e "\n${C_CYAN}${C_BOLD}📋 Available macOS Versions${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    jq -r '.versions | to_entries[] | "\(.key) - \(.value.name) (Build: \(.value.build))"' "${SPOOF_CONFIG}" | while read -r line; do
        echo -e "  ${C_GREEN}•${C_RESET} ${line}"
    done
    
    echo ""
}

get_version_details() {
    local version="$1"
    
    if ! jq ".versions.\"${version}\"" "${SPOOF_CONFIG}" > /dev/null 2>&1; then
        echo -e "${C_RED}❌ Version not found: ${version}${C_RESET}"
        return 1
    fi
    
    echo -e "\n${C_CYAN}${C_BOLD}📊 Version Details: ${version}${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    jq ".versions.\"${version}\"" "${SPOOF_CONFIG}" | jq '{
        name,
        build,
        kernel,
        webkit,
        release_date,
        eol_date
    }' | jq -r 'to_entries[] | "  \(.key): \(.value)"'
    
    echo ""
}

# ============================================================================
# HISTORY & LOGGING
# ============================================================================
log_spoof_operation() {
    local operation="$1"
    local version="$2"
    local version_name="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "{\"timestamp\": \"${timestamp}\", \"operation\": \"${operation}\", \"version\": \"${version}\", \"version_name\": \"${version_name}\"}" >> "${SPOOF_HISTORY}"
}

view_spoof_history() {
    echo -e "\n${C_CYAN}${C_BOLD}📜 Spoof Operation History${C_RESET}"
    echo -e "${C_PURP}$(printf '=%.0s' {1..60})${C_RESET}\n"
    
    if [[ -f "${SPOOF_HISTORY}" ]]; then
        jq '.' "${SPOOF_HISTORY}" 2>/dev/null | head -20
    else
        echo -e "${C_YELLOW}No spoof history available${C_RESET}"
    fi
    
    echo ""
}

# ============================================================================
# MAIN CLI
# ============================================================================
show_usage() {
    cat << EOF
${C_CYAN}${C_BOLD}🍎 Enhanced macOS Version Spoofer${C_RESET}

${C_BOLD}Usage:${C_RESET}
  $0 <command> [options]

${C_BOLD}Commands:${C_RESET}
  init                Initialize spoof environment
  list                List available macOS versions
  details <version>   Show version details
  spoof <version>     Activate spoof for target version
  verify              Verify current spoof status
  rollback            Deactivate all active spoofs
  history             View spoof operation history

${C_BOLD}Examples:${C_RESET}
  $0 init
  $0 list
  $0 spoof 14.6.1
  $0 verify
  $0 rollback

${C_BOLD}Available Versions:${C_RESET}
  • 11.7.10  - macOS Big Sur
  • 12.7.1   - macOS Monterey
  • 13.6.1   - macOS Ventura
  • 14.6.1   - macOS Sonoma
  • 15.1     - macOS Sequoia
  • 15.2.1   - macOS Sequoia Latest

EOF
}

main() {
    local command="${1:-help}"
    
    case "$command" in
        init)
            initialize_spoof_environment
            ;;
        list)
            list_available_versions
            ;;
        details)
            if [[ -z "${2:-}" ]]; then
                echo -e "${C_RED}❌ Version required${C_RESET}"
                show_usage
                return 1
            fi
            get_version_details "$2"
            ;;
        spoof)
            if [[ -z "${2:-}" ]]; then
                echo -e "${C_RED}❌ Target version required${C_RESET}"
                show_usage
                return 1
            fi
            activate_comprehensive_spoof "$2"
            ;;
        verify)
            verify_spoof_status
            ;;
        rollback)
            rollback_comprehensive_spoof
            ;;
        history)
            view_spoof_history
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            echo -e "${C_RED}❌ Unknown command: ${command}${C_RESET}"
            show_usage
            return 1
            ;;
    esac
}

# Ensure jq is available
if ! command -v jq &> /dev/null; then
    echo -e "${C_RED}❌ jq is required but not installed${C_RESET}"
    echo -e "${C_YELLOW}Install with: brew install jq${C_RESET}"
    exit 1
fi

# Run main function
main "$@"
