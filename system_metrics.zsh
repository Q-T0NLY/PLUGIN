#!/usr/bin/env zsh
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║              ENHANCED SYSTEM METRICS v3.1 - BIG SUR INTEL                ║
# ║           Real-time Performance Monitoring for macOS Big Sur             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM METRICS COLLECTION (Optimized for Big Sur Intel)
# ─────────────────────────────────────────────────────────────────────────────

quantum_metrics() {
    # CPU Usage (Intel optimization)
    local cpu_usage=$(top -l 1 2>/dev/null | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "0.0")
    
    # Memory Usage (optimized for Big Sur)
    local mem_total=$(sysctl -n hw.memsize 2>/dev/null | awk '{printf "%.2f", $1/1024/1024/1024}' || echo "16.00")
    local mem_stats=$(vm_stat 2>/dev/null | head -10)
    local mem_free_pages=$(echo "${mem_stats}" | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local mem_page_size=$(echo "${mem_stats}" | head -1 | awk '{print $8}')
    local mem_free_gb=$(awk "BEGIN {printf \"%.2f\", (${mem_free_pages} * ${mem_page_size}) / 1024 / 1024 / 1024}" 2>/dev/null || echo "0")
    local mem_used_gb=$(awk "BEGIN {printf \"%.2f\", ${mem_total} - ${mem_free_gb}}" 2>/dev/null || echo "0")
    local mem_percent=$(awk "BEGIN {printf \"%.1f\", (${mem_used_gb} / ${mem_total}) * 100}" 2>/dev/null || echo "50")
    
    # Disk Usage
    local disk_usage=$(df -h / 2>/dev/null | awk 'NR==2 {print $5}' | sed 's/%//' || echo "0")
    local disk_total=$(df -h / 2>/dev/null | awk 'NR==2 {print $2}' || echo "0")
    local disk_used=$(df -h / 2>/dev/null | awk 'NR==2 {print $3}' || echo "0")
    
    # Process Count
    local proc_count=$(ps aux 2>/dev/null | wc -l || echo "0")
    
    # Network Stats (Big Sur compatible)
    local net_in=$(netstat -ib 2>/dev/null | awk '/en0/ {print $7; exit}' || echo "0")
    local net_out=$(netstat -ib 2>/dev/null | awk '/en0/ {print $10; exit}' || echo "0")
    
    # Thermal info (if available)
    local temp=$(sysctl -a 2>/dev/null | grep -i temp | head -1 | awk '{print $NF}' || echo "N/A")
    
    # Battery (if available)
    local battery=$(pmset -g batt 2>/dev/null | grep -o '[0-9]*%' | head -1 || echo "N/A")
    local battery_status=$(pmset -g batt 2>/dev/null | grep "Battery" | awk '{for(i=1;i<=NF;i++) if ($i ~ /charging|discharging|AC/) print $(i+1) " " $(i+2)}' || echo "Unknown")
    
    # Uptime
    local uptime_seconds=$(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | sed 's/,//' || echo "0")
    local current_time=$(date +%s)
    local uptime_days=$(awk "BEGIN {printf \"%.1f\", (${current_time} - ${uptime_seconds}) / 86400}" 2>/dev/null || echo "0")
    
    # System info
    local kernel=$(uname -r 2>/dev/null || echo "Unknown")
    local hostname=$(hostname 2>/dev/null || echo "macOS")
    
    # Display metrics with enhanced formatting
    print -P "%F{226}╔══════════════════════════════════════════════════════════════════════════════╗%f"
    print -P "%F{226}║%f                    🖥️  NEXUS SYSTEM METRICS - BIG SUR INTEL               %F{226}║%f"
    print -P "%F{226}╠══════════════════════════════════════════════════════════════════════════════╣%f"
    
    # System Info
    print -P "%F{226}║%f  📊 System: %F{51}${hostname}%f | Kernel: %F{51}${kernel}%f | Battery: %F{226}${battery}%f %F{208}${battery_status}%f"
    
    # CPU & Process
    print -P "%F{226}║%f  ⚡ CPU Usage: %F{196}${cpu_usage}%%%f | Processes: %F{208}${proc_count}%f"
    
    # Memory
    print -P "%F{226}║%f  🧠 Memory: %F{202}${mem_percent}%%%f (${mem_used_gb}GB / ${mem_total}GB) | Free: %F{34}${mem_free_gb}GB%f"
    
    # Disk
    print -P "%F{226}║%f  💾 Disk: %F{208}${disk_usage}%%%f (${disk_used} / ${disk_total})"
    
    # Network
    print -P "%F{226}║%f  🌐 Network: IN %F{51}${net_in}%f | OUT %F{51}${net_out}%f"
    
    # Temperature & Uptime
    print -P "%F{226}║%f  🌡️  Temp: %F{208}${temp}%f | ⏱️  Uptime: %F{34}${uptime_days} days%f"
    
    print -P "%F{226}╚══════════════════════════════════════════════════════════════════════════════╝%f"
}

# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED PROGRESS BAR WITH COLOR GRADIENTS
# ─────────────────────────────────────────────────────────────────────────────

quantum_progress_bar() {
    local current=$1
    local total=$2
    local label="${3:-Progress}"
    local width=50
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    local empty=$((width - filled))
    
    # Dynamic color based on percentage
    local color="%F{34}"  # Green (0-33%)
    if (( percent > 33 && percent < 66 )); then
        color="%F{226}"    # Yellow (33-66%)
    elif (( percent >= 66 )); then
        color="%F{196}"    # Red (66-100%)
    fi
    
    printf "\r%F{226}[%f"
    printf "${color}%${filled}s%f" | tr ' ' '█'
    printf "%F{240}%${empty}s%f" | tr ' ' '░'
    printf "%F{226}]%f ${color}${percent}%%%f - ${label}"
}

# ─────────────────────────────────────────────────────────────────────────────
# LIVE METRICS MONITOR (Continuous display)
# ─────────────────────────────────────────────────────────────────────────────

quantum_metrics_monitor() {
    local interval="${1:-2}"  # Update interval in seconds
    
    while true; do
        clear
        quantum_metrics
        
        # Check for keyboard interrupt
        if ! sleep "${interval}" 2>/dev/null; then
            break
        fi
    done
}

# ─────────────────────────────────────────────────────────────────────────────
# ALIASES
# ─────────────────────────────────────────────────────────────────────────────

alias quantum-metrics='quantum_metrics'
alias quantum-monitor='quantum_metrics_monitor'

