#!/usr/bin/env zsh
# Universal Palette Manager - 8 Complete Color Themes

: "${PALETTE_CONFIG:=${HOME}/.config/ultra-zsh/palette_config.json}"

# Universal Palette Manager - 8 Complete Color Themes
declare -A PALETTE_QUANTUM_NEURAL=(
    [PRIMARY]="\033[38;2;0;212;255m"
    [SECONDARY]="\033[38;2;123;97;255m"
    [ACCENT]="\033[38;2;0;245;160m"
    [HIGHLIGHT]="\033[38;2;255;107;255m"
    [SUCCESS]="\033[38;2;0;245;160m"
    [WARNING]="\033[38;2;255;209;102m"
    [ERROR]="\033[38;2;255;107;157m"
    [INFO]="\033[38;2;0;212;255m"
)

declare -A PALETTE_CYBER_FUTURE=(
    [PRIMARY]="\033[38;2;0;240;255m"
    [SECONDARY]="\033[38;2;176;38;255m"
    [ACCENT]="\033[38;2;0;255;178m"
    [HIGHLIGHT]="\033[38;2;255;107;0m"
    [SUCCESS]="\033[38;2;0;255;178m"
    [WARNING]="\033[38;2;255;209;102m"
    [ERROR]="\033[38;2;255;107;157m"
    [INFO]="\033[38;2;0;240;255m"
)

declare -A PALETTE_MACOS_SONOMA=(
    [PRIMARY]="\033[38;2;0;122;255m"
    [SECONDARY]="\033[38;2;88;86;214m"
    [ACCENT]="\033[38;2;52;199;89m"
    [HIGHLIGHT]="\033[38;2;255;149;0m"
    [SUCCESS]="\033[38;2;52;199;89m"
    [WARNING]="\033[38;2;255;149;0m"
    [ERROR]="\033[38;2;255;45;85m"
    [INFO]="\033[38;2;0;122;255m"
)

declare -A PALETTE_ENTERPRISE_DEEP_BLUE=(
    [PRIMARY]="\033[38;2;0;102;204m"
    [SECONDARY]="\033[38;2;102;51;204m"
    [ACCENT]="\033[38;2;0;204;136m"
    [HIGHLIGHT]="\033[38;2;255;51;102m"
    [SUCCESS]="\033[38;2;0;204;136m"
    [WARNING]="\033[38;2;255;170;0m"
    [ERROR]="\033[38;2;255;51;102m"
    [INFO]="\033[38;2;0;102;204m"
)

declare -A PALETTE_NEON_CYBERPUNK=(
    [PRIMARY]="\033[38;2;255;0;128m"
    [SECONDARY]="\033[38;2;0;245;255m"
    [ACCENT]="\033[38;2;123;255;0m"
    [HIGHLIGHT]="\033[38;2;255;107;0m"
    [SUCCESS]="\033[38;2;123;255;0m"
    [WARNING]="\033[38;2;255;212;0m"
    [ERROR]="\033[38;2;255;107;157m"
    [INFO]="\033[38;2;0;245;255m"
)

declare -A PALETTE_MATERIAL_DEEP_OCEAN=(
    [PRIMARY]="\033[38;2;187;134;252m"
    [SECONDARY]="\033[38;2;3;218;198m"
    [ACCENT]="\033[38;2;207;102;121m"
    [HIGHLIGHT]="\033[38;2;255;183;77m"
    [SUCCESS]="\033[38;2;76;175;80m"
    [WARNING]="\033[38;2;255;183;77m"
    [ERROR]="\033[38;2;207;102;121m"
    [INFO]="\033[38;2;3;218;198m"
)

declare -A PALETTE_DRACULA_PRO=(
    [PRIMARY]="\033[38;2;189;147;249m"
    [SECONDARY]="\033[38;2;255;121;198m"
    [ACCENT]="\033[38;2;80;250;123m"
    [HIGHLIGHT]="\033[38;2;255;184;108m"
    [SUCCESS]="\033[38;2;80;250;123m"
    [WARNING]="\033[38;2;255;184;108m"
    [ERROR]="\033[38;2;255;85;85m"
    [INFO]="\033[38;2;139;233;253m"
)

declare -A PALETTE_ONE_DARK_PRO=(
    [PRIMARY]="\033[38;2;97;175;239m"
    [SECONDARY]="\033[38;2;198;120;221m"
    [ACCENT]="\033[38;2;152;195;121m"
    [HIGHLIGHT]="\033[38;2;229;192;123m"
    [SUCCESS]="\033[38;2;152;195;121m"
    [WARNING]="\033[38;2;229;192;123m"
    [ERROR]="\033[38;2;224;108;117m"
    [INFO]="\033[38;2;97;175;239m"
)

# Current active palette
export CURRENT_PALETTE="${CURRENT_PALETTE:-QUANTUM_NEURAL}"

# Universal Palette Manager Functions
get_palette_color() {
    local palette_name="${CURRENT_PALETTE}"
    local color_key="$1"
    
    case "${palette_name}" in
        QUANTUM_NEURAL) echo -n "${PALETTE_QUANTUM_NEURAL[$color_key]}" ;;
        CYBER_FUTURE) echo -n "${PALETTE_CYBER_FUTURE[$color_key]}" ;;
        MACOS_SONOMA) echo -n "${PALETTE_MACOS_SONOMA[$color_key]}" ;;
        ENTERPRISE_DEEP_BLUE) echo -n "${PALETTE_ENTERPRISE_DEEP_BLUE[$color_key]}" ;;
        NEON_CYBERPUNK) echo -n "${PALETTE_NEON_CYBERPUNK[$color_key]}" ;;
        MATERIAL_DEEP_OCEAN) echo -n "${PALETTE_MATERIAL_DEEP_OCEAN[$color_key]}" ;;
        DRACULA_PRO) echo -n "${PALETTE_DRACULA_PRO[$color_key]}" ;;
        ONE_DARK_PRO) echo -n "${PALETTE_ONE_DARK_PRO[$color_key]}" ;;
        *) echo -n "${PALETTE_QUANTUM_NEURAL[$color_key]}" ;;
    esac
}

set_palette() {
    local palette_name="$1"
    local valid_palettes=("QUANTUM_NEURAL" "CYBER_FUTURE" "MACOS_SONOMA" "ENTERPRISE_DEEP_BLUE" 
                          "NEON_CYBERPUNK" "MATERIAL_DEEP_OCEAN" "DRACULA_PRO" "ONE_DARK_PRO")
    
    if [[ -z "${palette_name}" ]]; then
        echo "Available palettes:"
        for p in "${valid_palettes[@]}"; do
            echo "  - ${p}"
        done
        return 1
    fi
    
    if (( ${valid_palettes[(Ie)${palette_name}]} )); then
        export CURRENT_PALETTE="${palette_name}"
        echo "✓ Palette set to: ${palette_name}"
        
        # Save to config
        echo "{\"palette\": \"${palette_name}\"}" > "${PALETTE_CONFIG}" 2>/dev/null || true
    else
        echo "Error: Invalid palette '${palette_name}'"
        return 1
    fi
}

# Load saved palette
if [[ -f "${PALETTE_CONFIG}" ]] && command -v jq >/dev/null 2>&1; then
    saved_palette=$(jq -r '.palette' "${PALETTE_CONFIG}" 2>/dev/null)
    [[ -n "${saved_palette}" ]] && export CURRENT_PALETTE="${saved_palette}"
fi

