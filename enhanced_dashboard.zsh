#!/usr/bin/env zsh
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║              ENHANCED NEXUS DASHBOARD v3.1 - BIG SUR INTEL               ║
# ║         Advanced Terminal Dashboard with Real-Time Metrics & AI          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

: "${DASHBOARD_CONFIG:=${NEXUS_HOME}/dashboard/config.json}"
: "${DASHBOARD_CACHE:=${NEXUS_HOME}/dashboard/cache}"
: "${DASHBOARD_STATE:=${NEXUS_HOME}/dashboard/state.json}"

mkdir -p "${NEXUS_HOME}/dashboard" "${DASHBOARD_CACHE}"

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED COLOR PALETTE - TrueColor + 256-Color Support
# ─────────────────────────────────────────────────────────────────────────────

declare -A QUANTUM_COLORS=(
  # Primary gradient (Electric to Deep)
  [cyan]="\033[38;2;0;255;255m"
  [blue]="\033[38;2;0;191;255m"
  [purple]="\033[38;2;138;43;226m"
  [pink]="\033[38;2;255;20;147m"
  [green]="\033[38;2;0;255;127m"
  [gold]="\033[38;2;255;215;0m"
  [magenta]="\033[38;2;255;0;255m"
  [red]="\033[38;2;255;0;0m"
  
  # Status colors
  [success]="\033[38;2;50;205;50m"
  [warning]="\033[38;2;255;165;0m"
  [error]="\033[38;2;220;20;60m"
  [info]="\033[38;2;30;144;255m"
  
  # Neutral
  [white]="\033[38;2;255;255;255m"
  [gray]="\033[38;2;128;128;128m"
  [reset]="\033[0m"
)

declare -A QUANTUM_256=(
  [cyan]=51
  [blue]=39
  [purple]=135
  [pink]=201
  [green]=48
  [gold]=226
  [magenta]=201
  [red]=196
  [success]=34
  [warning]=208
  [error]=160
  [info]=33
  [white]=15
  [gray]=8
  [reset]=0
)

# ─────────────────────────────────────────────────────────────────────────────
# DETECT COLOR CAPABILITY
# ─────────────────────────────────────────────────────────────────────────────

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

get_color() {
  local color_name="$1"
  local fallback="${2:-white}"
  local color_mode=$(detect_color_support)
  
  if [[ "${color_mode}" == "truecolor" ]]; then
    echo -n "${QUANTUM_COLORS[$color_name]}"
  else
    echo -n "\033[38;5;${QUANTUM_256[$color_name]}m"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# REAL-TIME SYSTEM TELEMETRY (Optimized for Big Sur Intel)
# ─────────────────────────────────────────────────────────────────────────────

get_system_metrics() {
  local start_time=$(date +%s%N)
  
  # CPU Usage (more efficient method for Intel Macs)
  local cpu_usage=$(top -l 1 2>/dev/null | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "0.0")
  
  # Memory Usage
  local mem_total=$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.1f", $1/1024/1024/1024}' || echo "0")
  local mem_stats=$(vm_stat 2>/dev/null | head -10)
  local mem_free_pages=$(echo "${mem_stats}" | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
  local mem_page_size=$(echo "${mem_stats}" | head -1 | awk '{print $8}')
  local mem_free_gb=$(awk "BEGIN {printf \"%.1f\", (${mem_free_pages} * ${mem_page_size}) / 1024 / 1024 / 1024}" 2>/dev/null || echo "0")
  local mem_used_gb=$(awk "BEGIN {printf \"%.1f\", ${mem_total} - ${mem_free_gb}}" 2>/dev/null || echo "0")
  local mem_percent=$(awk "BEGIN {printf \"%.0f\", (${mem_used_gb} / ${mem_total}) * 100}" 2>/dev/null || echo "0")
  
  # Disk Usage
  local disk_usage=$(df -h / 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//' || echo "0")
  
  # Process Count
  local proc_count=$(ps aux | wc -l)
  
  # Network (active connections)
  local net_connections=$(netstat -an 2>/dev/null | grep ESTABLISHED | wc -l)
  
  # Battery
  local battery=$(pmset -g batt 2>/dev/null | grep -o '[0-9]*%' | head -1 || echo "N/A")
  
  # Uptime
  local uptime_seconds=$(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | sed 's/,//' || echo "0")
  local current_time=$(date +%s)
  local uptime_days=$(awk "BEGIN {printf \"%.1f\", (${current_time} - ${uptime_seconds}) / 86400}" 2>/dev/null || echo "0")
  
  # Advanced Metrics (GEFS - Generic Efficiency Score)
  local gefs=$(awk "BEGIN {printf \"%.2f\", 100 - (${cpu_usage} * 0.35 + ${mem_percent} * 0.35 + ${disk_usage} * 0.3)}" 2>/dev/null || echo "0")
  local risk=$(awk "BEGIN {printf \"%.4f\", (100 - ${gefs}) / 1000}" 2>/dev/null || echo "0.1")
  
  # Performance metric
  local perf_ms=$(awk "BEGIN {printf \"%.2f\", 0.5 + (${cpu_usage} / 200)}" 2>/dev/null || echo "0.5")
  
  # Health score (0-100)
  local health=$(awk "BEGIN {printf \"%.0f\", ${gefs}}" 2>/dev/null || echo "50")
  
  # Calculate metrics latency
  local end_time=$(date +%s%N)
  local latency_ms=$(awk "BEGIN {printf \"%.2f\", (${end_time} - ${start_time}) / 1000000}" 2>/dev/null || echo "0")
  
  # Return pipe-delimited metrics
  echo "${cpu_usage}|${mem_percent}|${mem_used_gb}|${mem_total}|${disk_usage}|${battery}|${uptime_days}|${gefs}|${risk}|${perf_ms}|${health}|${proc_count}|${net_connections}|${latency_ms}"
}

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD RENDERING COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

# Header bar with title and time
render_dashboard_header() {
  local title="$1"
  local width=$(tput cols 2>/dev/null || echo 88)
  local time_str="$(date '+%H:%M:%S')"
  local date_str="$(date '+%a, %b %d')"
  
  # Truncate title if needed
  [[ ${#title} -gt $((width - 20)) ]] && title="${title:0:$((width - 23))}..."
  
  printf "$(get_color cyan)╭$(printf '━%.0s' $(seq 1 $((width - 2))))╮$(get_color reset)\n"
  printf "$(get_color cyan)│$(get_color magenta) %-$((width - 4))s $(get_color cyan)│$(get_color reset)\n" "${title}"
  printf "$(get_color cyan)│$(get_color gold) %s  |  %s %$((width - ${#time_str} - ${#date_str} - 8))s$(get_color cyan)│$(get_color reset)\n" "${date_str}" "${time_str}" ""
}

# Footer bar
render_dashboard_footer() {
  local width=$(tput cols 2>/dev/null || echo 88)
  printf "$(get_color cyan)╰$(printf '━%.0s' $(seq 1 $((width - 2))))╯$(get_color reset)\n"
}

# Metrics panel with visual indicators
render_metrics_panel() {
  local metrics="$1"
  local width=$(tput cols 2>/dev/null || echo 88)
  
  IFS='|' read -r cpu mem_pct mem_used mem_total disk battery uptime gefs risk perf health proc_count net_conn latency <<< "$metrics"
  
  # Health indicator bar
  local health_bar=""
  local health_color=$(get_color success)
  if (( $(awk "BEGIN {print ($health < 70)}") )); then
    health_color=$(get_color warning)
  fi
  if (( $(awk "BEGIN {print ($health < 40)}") )); then
    health_color=$(get_color error)
  fi
  
  # Construct bar (40 chars)
  local filled=$(awk "BEGIN {printf \"%.0f\", $health / 2.5}")
  local empty=$((40 - filled))
  health_bar+="["
  for ((i=0; i<filled; i++)); do health_bar+="█"; done
  for ((i=0; i<empty; i++)); do health_bar+="░"; done
  health_bar+="]"
  
  printf "\n"
  printf "$(get_color cyan)├─ SYSTEM HEALTH ─────────────────────────────────────────────────────────────────────────$(get_color reset)\n"
  printf "$(get_color cyan)│$(get_color reset) Overall Health: ${health_color}${health_bar}$(get_color reset) ${health}%%\n"
  
  printf "$(get_color cyan)├─ RESOURCE USAGE ─────────────────────────────────────────────────────────────────────────$(get_color reset)\n"
  
  # CPU bar
  local cpu_color=$(get_color success)
  (( $(awk "BEGIN {print ($cpu > 70)}") )) && cpu_color=$(get_color warning)
  (( $(awk "BEGIN {print ($cpu > 85)}") )) && cpu_color=$(get_color error)
  printf "$(get_color cyan)│$(get_color reset)  CPU: ${cpu_color}%-6.1f%%$(get_color reset) " "${cpu}"
  
  # Memory bar
  local mem_color=$(get_color success)
  (( $(awk "BEGIN {print ($mem_pct > 70)}") )) && mem_color=$(get_color warning)
  (( $(awk "BEGIN {print ($mem_pct > 85)}") )) && mem_color=$(get_color error)
  printf "Memory: ${mem_color}%-6.1f%%$(get_color reset) " "${mem_pct}"
  
  # Disk bar
  local disk_color=$(get_color success)
  (( $(awk "BEGIN {print ($disk > 80)}") )) && disk_color=$(get_color warning)
  (( $(awk "BEGIN {print ($disk > 90)}") )) && disk_color=$(get_color error)
  printf "Disk: ${disk_color}%-6.1f%%$(get_color reset)\n" "${disk}"
  
  printf "$(get_color cyan)├─ SYSTEM INFO ────────────────────────────────────────────────────────────────────────────$(get_color reset)\n"
  printf "$(get_color cyan)│$(get_color reset)  Memory: $(get_color blue)%.1fGB$(get_color reset) / %.1fGB  |  Battery: $(get_color gold)%s$(get_color reset)  |  Uptime: $(get_color green)%.1f days$(get_color reset)\n" "${mem_used}" "${mem_total}" "${battery}" "${uptime}"
  
  printf "$(get_color cyan)├─ PERFORMANCE ────────────────────────────────────────────────────────────────────────────$(get_color reset)\n"
  printf "$(get_color cyan)│$(get_color reset)  GEFS: $(get_color gold)%.2f%%$(get_color reset)  |  Risk: $(get_color pink)%.4f$(get_color reset)  |  Latency: $(get_color info)%.2fms$(get_color reset)  |  Processes: $(get_color purple)%d$(get_color reset)  |  Connections: $(get_color cyan)%d$(get_color reset)\n" "${gefs}" "${risk}" "${latency}" "${proc_count}" "${net_conn}"
}

# ─────────────────────────────────────────────────────────────────────────────
# MAIN DASHBOARD FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

quantum_dashboard() {
  local refresh_interval="${1:-2}"  # seconds
  local duration="${2:-0}"          # 0 = infinite
  
  clear
  
  local start_time=$(date +%s)
  while true; do
    clear
    
    # Render dashboard
    render_dashboard_header "🚀 NEXUS AI STUDIO MATRIX - BIG SUR INTEL"
    
    local metrics=$(get_system_metrics)
    render_metrics_panel "$metrics"
    
    render_dashboard_footer
    
    # Check duration limit
    if [[ ${duration} -gt 0 ]]; then
      local current_time=$(date +%s)
      local elapsed=$((current_time - start_time))
      if [[ ${elapsed} -ge ${duration} ]]; then
        break
      fi
    fi
    
    # Wait for next refresh (with Ctrl+C handling)
    sleep ${refresh_interval} || break
  done
}

# ─────────────────────────────────────────────────────────────────────────────
# QUICK STATS - Lightweight version for prompt
# ─────────────────────────────────────────────────────────────────────────────

quantum_quick_stats() {
  local metrics=$(get_system_metrics)
  IFS='|' read -r cpu mem_pct mem_used mem_total disk battery uptime gefs risk perf health <<< "$metrics"
  
  printf "$(get_color cyan)[CPU:$(get_color reset) %.1f%% $(get_color cyan)|$(get_color reset) MEM: %.1f%% $(get_color cyan)|$(get_color reset) DISK: %.1f%% $(get_color cyan)|$(get_color reset) HEALTH: %.0f%%$(get_color cyan)]$(get_color reset) " "${cpu}" "${mem_pct}" "${disk}" "${health}"
}

# ─────────────────────────────────────────────────────────────────────────────
# ALIASES & SHORTCUTS
# ─────────────────────────────────────────────────────────────────────────────

alias quantum-dashboard='quantum_dashboard 1'
alias quantum-stats='quantum_quick_stats'
alias quantum-dash-monitor='quantum_dashboard 1 300'  # 5 minute monitor
