#!/usr/bin/env zsh
# NEXUS AI STUDIO MATRIX DASHBOARD v2.0
# Quantum Neural Gradient Interactive Terminal Dashboard

: "${DASHBOARD_CONFIG:=${HOME}/.config/ultra-zsh/dashboard/config.json}"
: "${CHAT_HISTORY:=${HOME}/.config/ultra-zsh/dashboard/chat_history.json}"
mkdir -p "${HOME}/.config/ultra-zsh/dashboard"

# Ultra Modern Neon Gradient Palette (TrueColor RGB)
declare -A QUANTUM_GRADIENT=(
    [1]="\033[38;2;0;255;255m"      # Electric Cyan
    [2]="\033[38;2;0;191;255m"      # Bright Blue
    [3]="\033[38;2;138;43;226m"     # Blue Violet
    [4]="\033[38;2;255;20;147m"     # Deep Pink
    [5]="\033[38;2;0;255;127m"      # Spring Green
    [6]="\033[38;2;255;215;0m"      # Gold
    [7]="\033[38;2;255;0;255m"      # Magenta
    [8]="\033[38;2;0;255;255m"      # Aqua
)

# 16-bit fallback colors (ANSI 256-color) - Ultra Modern
declare -A QUANTUM_256=(
    [1]=51   # Bright Cyan
    [2]=39   # Bright Blue
    [3]=135  # Bright Magenta
    [4]=201  # Hot Pink
    [5]=48   # Bright Green
    [6]=226  # Yellow
    [7]=201  # Magenta
    [8]=51   # Cyan
)

# Detect terminal color support
detect_color_support() {
    if [[ "${TERM}" == *"256color"* ]] || [[ -n "${COLORTERM}" ]]; then
        if [[ "${COLORTERM}" == "truecolor" ]] || [[ "${COLORTERM}" == "24bit" ]]; then
            echo "truecolor"
        else
            echo "256color"
        fi
    else
        echo "16color"
    fi
}

# Get color code based on terminal support
get_quantum_color() {
    local index=$1
    local color_support=$(detect_color_support)
    
    if [[ "${color_support}" == "truecolor" ]]; then
        echo -n "${QUANTUM_GRADIENT[$index]}"
    else
        echo -n "\033[38;5;${QUANTUM_256[$index]}m"
    fi
}

# Animated quantum gradient text (startup animation)
animate_quantum_text() {
    local text="$1"
    local iterations="${2:-20}"
    local delay="${3:-0.05}"
    
    for i in $(seq 1 ${iterations}); do
        clear
        local offset=$((i % 5 + 1))
        local next_offset=$(((i + 1) % 5 + 1))
        
        # Create gradient effect
        local gradient_chars=$(echo "${text}" | fold -w1)
        local char_index=0
        
        for char in ${gradient_chars}; do
            local color_idx=$(((char_index + i) % 5 + 1))
            local color=$(get_quantum_color ${color_idx})
            echo -ne "${color}${char}\033[0m"
            ((char_index++))
        done
        echo
        
        sleep ${delay}
    done
}

# Generate static gradient text (stable mode)
render_gradient_text() {
    local text="$1"
    local base_color="${2:-1}"
    
    local chars=$(echo "${text}" | fold -w1)
    local char_index=0
    
    for char in ${chars}; do
        local color_idx=$(((char_index + base_color - 1) % 5 + 1))
        local color=$(get_quantum_color ${color_idx})
        echo -ne "${color}${char}\033[0m"
        ((char_index++))
    done
}

# Get real-time system metrics
get_realtime_telemetry() {
    # CPU Usage
    local cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' 2>/dev/null || echo "0.0")
    
    # Memory Usage
    local mem_total=$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.2f", $1/1024/1024/1024}' || echo "0")
    local mem_stats=$(vm_stat 2>/dev/null | head -5)
    local mem_free_pages=$(echo "${mem_stats}" | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local page_size=$(echo "${mem_stats}" | head -1 | awk '{print $8}')
    local mem_free_gb=$(awk "BEGIN {printf \"%.2f\", (${mem_free_pages} * ${page_size}) / 1024 / 1024 / 1024}")
    local mem_used_gb=$(awk "BEGIN {printf \"%.2f\", ${mem_total} - ${mem_free_gb}}")
    local mem_percent=$(awk "BEGIN {printf \"%.1f\", (${mem_used_gb} / ${mem_total}) * 100}")
    
    # Disk Usage
    local disk_usage=$(df -h / 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//' || echo "0")
    
    # Battery
    local battery=$(pmset -g batt 2>/dev/null | grep -o '[0-9]*%' | head -1 || echo "N/A")
    
    # Uptime
    local uptime_seconds=$(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | sed 's/,//' || echo "0")
    local current_time=$(date +%s)
    local uptime_days=$(awk "BEGIN {printf \"%.1f\", (${current_time} - ${uptime_seconds}) / 86400}")
    
    # Calculate GEFS (Generic Efficiency Score) - simulated advanced metric
    local gefs=$(awk "BEGIN {printf \"%.2f\", 100 - (${cpu_usage} * 0.3 + ${mem_percent} * 0.3 + ${disk_usage} * 0.2)}")
    
    # Performance metric (latency simulation)
    local perf_ms=$(awk "BEGIN {printf \"%.2f\", 0.5 + (${cpu_usage} / 200)}")
    
    # Risk score (inverse of health)
    local risk=$(awk "BEGIN {printf \"%.3f\", (100 - ${gefs}) / 1000}")
    
    echo "${gefs}|${risk}|${perf_ms}|${cpu_usage}|${mem_percent}|${disk_usage}|${battery}|${uptime_days}"
}

# Center text in terminal
center_text() {
    local text="$1"
    local width=$(tput cols 2>/dev/null || echo 80)
    local text_length=${#text}
    local padding=$(( (width - text_length) / 2 ))
    if [[ ${padding} -lt 0 ]]; then padding=0; fi
    printf "%*s%s" ${padding} "" "${text}"
}

# Create centered box with auto-scaling width
create_centered_box() {
    local content_lines=("$@")
    local width=$(tput cols 2>/dev/null || echo 80)
    local border_color="$1"
    local reset="$2"
    shift 2
    content_lines=("$@")
    
    # Calculate box width (80% of terminal width, min 60, max content width + 4)
    local max_content_width=0
    for line in "${content_lines[@]}"; do
        local line_len=${#line}
        [[ ${line_len} -gt ${max_content_width} ]] && max_content_width=${line_len}
    done
    
    local box_width=$((width * 80 / 100))
    [[ ${box_width} -lt 60 ]] && box_width=60
    [[ ${box_width} -gt $((max_content_width + 4)) ]] && box_width=$((max_content_width + 4))
    [[ ${box_width} -gt $((width - 4)) ]] && box_width=$((width - 4))
    
    local padding=$(( (width - box_width) / 2 ))
    [[ ${padding} -lt 0 ]] && padding=0
    
    # Top border
    printf "%*s" ${padding} ""
    echo -ne "${border_color}╔"
    printf "═%.0s" $(seq 1 $((box_width - 2)))
    echo -ne "╗${reset}\n"
    
    # Content lines
    for line in "${content_lines[@]}"; do
        printf "%*s" ${padding} ""
        echo -ne "${border_color}║${reset}"
        local line_len=${#line}
        local line_padding=$(( (box_width - line_len - 2) / 2 ))
        [[ ${line_padding} -lt 0 ]] && line_padding=0
        printf "%*s" ${line_padding} ""
        echo -ne "${line}"
        local remaining=$((box_width - line_len - line_padding - 2))
        [[ ${remaining} -lt 0 ]] && remaining=0
        printf "%*s" ${remaining} ""
        echo -ne "${border_color}║${reset}\n"
    done
    
    # Bottom border
    printf "%*s" ${padding} ""
    echo -ne "${border_color}╚"
    printf "═%.0s" $(seq 1 $((box_width - 2)))
    echo -ne "╝${reset}\n"
}

# Render CONNEXUS ASCII art with auto-scaling and centering - Ultra Modern
render_connexus_art() {
    local mode="${1:-stable}"
    local width=$(tput cols 2>/dev/null || echo 80)
    local border_color=$(get_quantum_color 1)  # Electric Cyan
    local reset="\033[0m"
    
    # Original CONNEXUS art (66 chars wide)
    local original_art=(
        "╭══════════════════════════════════════════════════════════════════════╮"
        "║  ██████╗  ██████╗ ███╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗      ║"
        "║  ██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║      ║"
        "║  ██║  ██║██║   ██║██╔██╗ ██║█████╗  ██║  ██║█████╗  ███████║██║      ║"
        "║  ██║  ██║██║   ██║██║╚██╗██║██╔══╝  ██║  ██║██╔══╝  ██╔══██╗██║      ║"
        "║  ██████╔╝╚██████╔╝██║ ╚████║███████╗██████╔╝███████╗██║  ██║███████╗ ║"
        "║  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ║"
        "╰══════════════════════════════════════════════════════════════════════╯"
    )
    
    # Ultra modern neon color gradient
    local neon_colors=(51 45 39 33 27 21 57 63)  # Cyan to blue to purple gradient
    
    # Fit art inside outer frame (width - 2 for side borders) with minimal padding (1 space each side when possible)
    local art_width=66
    local available=$((width - 2 - art_width))
    local left_padding=0
    local right_padding=0
    if (( available > 0 )); then
        # cap padding to at most 2 spaces total to keep art near the frame
        (( available > 2 )) && available=2
        left_padding=$((available / 2))
        right_padding=$((available - left_padding))
    fi
    
    # Center and render each line with exact symmetry
    local i=1
    while [[ $i -le ${#original_art[@]} ]]; do
        local line="${original_art[$i]}"
        local color_idx=$(( (i - 1) % ${#neon_colors[@]} + 1 ))
        local neon_color="${neon_colors[$color_idx]}"
        
        echo -ne "${border_color}║${reset}"
        printf "%*s" ${left_padding} ""
        print -Pn "%F{${neon_color}}${line}%f"
        printf "%*s" ${right_padding} ""
        echo -ne "${border_color}║${reset}\n"
        ((i++))
    done
}

# Render the full provided CONNEXUS block (title + art + telemetry)
render_connexus_block_full() {
    local cols=$(tput cols 2>/dev/null || echo 80)

    # Live telemetry (reuse dashboard metrics)
    local telemetry=$(get_realtime_telemetry)
    local gefs=$(echo "${telemetry}" | cut -d'|' -f1)
    local risk=$(echo "${telemetry}" | cut -d'|' -f2)
    local perf=$(echo "${telemetry}" | cut -d'|' -f3)
    local uptime=$(echo "${telemetry}" | cut -d'|' -f8)
    local health=$(awk "BEGIN {printf \"%.0f\", ${gefs}}")

    local content_width=69
    local tele_line1=$(printf "%-69.69s" "$(printf "🎯 GEFS: %s%%    ⚡ MODE: HYPER-GENERATIVE    📊 HEALTH: %s%%" "${gefs}" "${health}")")
    local tele_line2=$(printf "%-69.69s" "$(printf "🛡️ RISK: %s     🚀 PERF: <%sms core         🔄 UPTIME: %sd" "${risk}" "${perf}" "${uptime}")")

    local block=(
        "╔══════════════════════════════════════════════════════════════════════════════╗"
        "║                     🚀 NEXUS AI STUDIO MATRIX v2.0 🚀                        ║"
        "╠══════════════════════════════════════════════════════════════════════════════╣"
        "║  ╭══════════════════════════════════════════════════════════════════════╮    ║"
        "║  ║  ██████╗  ██████╗ ███╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗      ║    ║"
        "║  ║  ██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║      ║    ║"
        "║  ║  ██║  ██║██║   ██║██╔██╗ ██║█████╗  ██║  ██║█████╗  ███████║██║      ║    ║"
        "║  ║  ██║  ██║██║   ██║██║╚██╗██║██╔══╝  ██║  ██║██╔══╝  ██╔══██╗██║      ║    ║"
        "║  ║  ██████╔╝╚██████╔╝██║ ╚████║███████╗██████╔╝███████╗██║  ██║███████╗ ║    ║"
        "║  ║    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚════╝ ║    ║"
        "║  ╰══════════════════════════════════════════════════════════════════════╯    ║"
        "╠══════════════════════════════════════════════════════════════════════════════╣"
        "║  ┌─ LIVE TELEMETRY ────────────────────────────────────────────────────────┐ ║"
        "║  │ ${tele_line1} │ ║"
        "║  │ ${tele_line2} │ ║"
        "║  └────────────────────────────────────────────────────────────────────────┘ ║"
        "╚══════════════════════════════════════════════════════════════════════════════╝"
    )

    local block_width=${#block[1]}
    local pad=$(( (cols - block_width) / 2 ))
    [[ ${pad} -lt 0 ]] && pad=0
    local line=""
    for line in "${block[@]}"; do
        printf "%*s%s\n" ${pad} "" "${line}"
    done
}

# Generate dashboard frame with full auto-scaling and centering
render_dashboard() {
    local mode="${1:-stable}"
    local chat_mode="${2:-false}"
    local chat_content="${3:-}"

    clear
    render_connexus_block_full
}

# Startup animation sequence
dashboard_startup() {
    local iterations=15
    local delay=0.08
    
    for i in $(seq 1 ${iterations}); do
        render_dashboard "startup" "false"
        sleep ${delay}
    done
    
    # Transition to stable
    for i in $(seq 1 5); do
        render_dashboard "transition" "false"
        sleep 0.1
    done
}

# Virtual reasoning display (shows AI thinking process)
display_virtual_reasoning() {
    local reasoning_steps=(
        "🔍 Analyzing user intent..."
        "🧠 Processing context vectors..."
        "⚡ Running ensemble fusion algorithm..."
        "🌐 Querying knowledge graph..."
        "🤖 Generating response with consensus..."
        "✨ Refining output quality..."
    )
    
    local step_index=$((RANDOM % ${#reasoning_steps[@]} + 1))
    local color=$(get_quantum_color $((step_index % 5 + 1)))
    local reset="\033[0m"
    
    echo -e "${color}${reasoning_steps[$step_index]}${reset}"
}

# Main dashboard launcher
nexus_dashboard() {
    local mode="${1:-interactive}"
    
    if [[ "${mode}" == "startup" ]]; then
        dashboard_startup
    fi
    
    render_dashboard "stable" "false"
    
    # Interactive menu loop
    while true; do
        read -r "choice?Select option [0-9]: "
        
        case "${choice}" in
            1)
                # AI Chat Interface
                clear
                render_dashboard "stable" "true" ""
                
                local chat_active=true
                local chat_buffer=""
                
                while [[ "${chat_active}" == "true" ]]; do
                    read -r "user_input?You: "
                    
                    if [[ "${user_input}" == "/exit" ]] || [[ "${user_input}" == "/back" ]]; then
                        chat_active=false
                        render_dashboard "stable" "false"
                        break
                    fi
                    
                    # Display virtual reasoning
                    echo ""
                    display_virtual_reasoning
                    sleep 1
                    
                    # Simulate AI response (integrate with actual AI later)
                    local ai_response="🤖 AI: I understand your query: '${user_input}'. Processing with multi-model consensus..."
                    
                    chat_buffer+="You: ${user_input}\n\n${ai_response}\n\n"
                    
                    clear
                    render_dashboard "stable" "true" "${chat_buffer}"
                done
                ;;
            0)
                echo "Exiting dashboard..."
                break
                ;;
            *)
                echo "Invalid option. Please select 0-9."
                sleep 1
                render_dashboard "stable" "false"
                ;;
        esac
    done
}

# Auto-start dashboard on shell load (optional)
if [[ "${AUTO_START_DASHBOARD}" == "true" ]]; then
    nexus_dashboard "startup"
fi

