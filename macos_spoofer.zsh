#!/usr/bin/env zsh
# Ultra Advanced macOS Version Spoofer (user-level + system-level when SIP allows)

: "${SPOOF_DIR:=${HOME}/.config/ultra-zsh/security/spoof}"
mkdir -p "${SPOOF_DIR}/backups"
mkdir -p "${HOME}/bin"

macos_sip_enabled() {
    csrutil status 2>/dev/null | grep -qi "enabled"
}

macos_sip_instructions() {
    echo "⚠️  System Integrity Protection (SIP) is enabled."
    echo "To apply system-level spoof:"
    echo "  1) Reboot holding Command+R to enter Recovery."
    echo "  2) Open Utilities > Terminal."
    echo "  3) Run: csrutil disable"
    echo "  4) Reboot normally, then rerun:"
    echo "       macos_spoof_version --force-system <version> [build]"
}

# Supported macOS versions
declare -A MACOS_VERSIONS=(
    ["10.15"]="Catalina"
    ["11.0"]="Big Sur"
    ["12.0"]="Monterey"
    ["13.0"]="Ventura"
    ["14.0"]="Sonoma"
    ["15.0"]="Sequoia"
)

macos_spoof_version() {
    local force_system=false
    if [[ "$1" == "--force-system" ]] || [[ "$1" == "-S" ]]; then
        force_system=true
        shift
    fi

    local target_version="$1"
    local target_build="$2"
    local build_default="$(sw_vers -buildVersion 2>/dev/null || echo 22A400)"

    if [[ -z "${target_version}" ]]; then
        echo "Usage: macos_spoof_version [--force-system|-S] <version> [build]"
        echo "Available versions: ${(k)MACOS_VERSIONS[@]}"
        echo "Notes: --force-system requires SIP disabled (Recovery: csrutil disable) and sudo."
        return 1
    fi

    if (( ${#MACOS_VERSIONS[@]} == 0 )); then
        typeset -A MACOS_VERSIONS=(
            ["10.15"]="Catalina"
            ["11.0"]="Big Sur"
            ["12.0"]="Monterey"
            ["13.0"]="Ventura"
            ["14.0"]="Sonoma"
            ["15.0"]="Sequoia"
        )
    fi

    if [[ -z "${MACOS_VERSIONS[$target_version]-}" ]]; then
        echo "Error: Unsupported version ${target_version}"
        echo "Available: ${(k)MACOS_VERSIONS[@]}"
        return 1
    fi

    local backup_file="${SPOOF_DIR}/backups/system_version_$(date +%Y%m%d_%H%M%S).plist"

    # User-level spoof (works without SIP changes)
    export SYSTEM_VERSION_COMPAT="${target_version}"
    export MACOS_VERSION="${target_version}"
    export PRODUCT_VERSION="${target_version}"

    # sw_vers shim for PATH override
    cat > "${HOME}/bin/sw_vers" <<EOF
#!/bin/zsh
echo "ProductName:    macOS"
echo "ProductVersion: ${target_version}"
echo "BuildVersion:   ${target_build:-$build_default}"
EOF
    chmod +x "${HOME}/bin/sw_vers"

    # launchd agent to persist env + PATH prepend
    cat > "${HOME}/Library/LaunchAgents/com.ultrazsh.spoof.plist" <<LAUNCHD_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ultrazsh.spoof</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>-c</string>
        <string>export SYSTEM_VERSION_COMPAT="${target_version}"; export MACOS_VERSION="${target_version}"; export PRODUCT_VERSION="${target_version}"; export PATH="${HOME}/bin:${PATH}"</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
LAUNCHD_EOF

    # System-level plist spoof (only if SIP disabled; may still require sudo password)
    local system_target="/System/Library/CoreServices/SystemVersion.plist"
    local spoof_plist="${SPOOF_DIR}/spoofed_version.plist"

    cat > "${spoof_plist}" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>ProductBuildVersion</key>
    <string>${target_build:-$build_default}</string>
    <key>ProductCopyright</key>
    <string>1983-2024 Apple Inc.</string>
    <key>ProductName</key>
    <string>macOS</string>
    <key>ProductUserVisibleVersion</key>
    <string>${target_version}</string>
    <key>ProductVersion</key>
    <string>${target_version}</string>
    <key>iOSSupportVersion</key>
    <string>17.0</string>
</dict>
</plist>
PLIST_EOF

    if ${force_system}; then
        if macos_sip_enabled; then
            macos_sip_instructions
        else
            if [[ -f "${system_target}" ]]; then
                sudo cp "${system_target}" "${backup_file}" && echo "✓ Backed up ${system_target}"
            fi
            if sudo cp "${spoof_plist}" "${system_target}"; then
                echo "✓ System plist spoof applied to ${target_version}"
            else
                echo "⚠️  Could not write ${system_target}; user-level spoof still active"
            fi
        fi
    else
        echo "ℹ️  User-level spoof active (env + sw_vers shim). To attempt system-level: macos_spoof_version --force-system ${target_version}"
    fi

    echo "✓ macOS version spoofing configured for ${target_version}"
    echo "ℹ️  To restore: macos_restore_version <backup_file> (if system plist was changed)"
}

macos_restore_version() {
    local backup_file="$1"

    # remove user-level shims
    rm -f "${HOME}/bin/sw_vers"
    launchctl unload "${HOME}/Library/LaunchAgents/com.ultrazsh.spoof.plist" 2>/dev/null || true

    if [[ -z "${backup_file}" ]]; then
        echo "Available backups:"
        ls -1 "${SPOOF_DIR}/backups/" 2>/dev/null || echo "No backups found"
        return 0
    fi

    local system_target="/System/Library/CoreServices/SystemVersion.plist"
    if [[ -f "${SPOOF_DIR}/backups/${backup_file}" ]]; then
        if ! macos_sip_enabled; then
            sudo cp "${SPOOF_DIR}/backups/${backup_file}" "${system_target}" && echo "✓ Restored ${system_target} from backup"
        else
            echo "⚠️  SIP enabled; cannot restore system plist. Disable SIP or restore manually."
            return 1
        fi
    else
        echo "Error: Backup file not found"
        return 1
    fi
}

macos_list_versions() {
    echo "Available macOS Versions:"
    for version in "${(k)MACOS_VERSIONS[@]}"; do
        echo "  ${version} - ${MACOS_VERSIONS[$version]}"
    done
}

