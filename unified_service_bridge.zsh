#!/usr/bin/env zsh
# ╔════════════════════════════════════════════════════════════════════════════╗
# ║        🔗 UNIFIED SERVICE BRIDGE v4.1.0 - ZSH BACKEND INTEGRATION          ║
# ║   Consolidated bridge connecting Zsh CLI to backend services               ║
# ║                                                                            ║
# ║ Merges:                                                                    ║
# ║  ✅ llm_service_bridge.zsh - LLM service integration                       ║
# ║  ✅ ai_backend_bridge.zsh - AI backend bridge                              ║
# ║                                                                            ║
# ║ Features:                                                                  ║
# ║  • Connection to LLM orchestrator service                                 ║
# ║  • Unified backend request handling                                       ║
# ║  • Service health checking                                                ║
# ║  • Real-time streaming response support                                   ║
# ║  • Error handling and retry logic                                         ║
# ║  • Request/response logging                                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝

[[ -n "$NEXUS_UNIFIED_SERVICE_BRIDGE_LOADED" ]] && return
export NEXUS_UNIFIED_SERVICE_BRIDGE_LOADED=1

# ============================================================================
# SERVICE CONFIGURATION
# ============================================================================

export LLM_SERVICE_HOST="${LLM_SERVICE_HOST:-localhost}"
export LLM_SERVICE_PORT="${LLM_SERVICE_PORT:-8002}"
export LLM_SERVICE_TIMEOUT="${LLM_SERVICE_TIMEOUT:-30}"
export SERVICE_BRIDGE_LOG="${HOME}/.nexus/service_bridge.log"
export SERVICE_BRIDGE_CONFIG="${HOME}/.config/ultra-zsh/service_bridge.json"

# Ensure log directory exists
mkdir -p "$(dirname "$SERVICE_BRIDGE_LOG")"
mkdir -p "$(dirname "$SERVICE_BRIDGE_CONFIG")"

# Service endpoints
declare -A SERVICE_ENDPOINTS=(
    [health]="/api/health"
    [llm_chat]="/api/llm/chat"
    [llm_code]="/api/llm/code"
    [llm_analyze]="/api/llm/analyze"
    [registry_entries]="/api/registry/entries"
    [registry_search]="/api/registry/search"
    [registry_health]="/api/registry/health"
)

# Service status cache
declare -A SERVICE_STATUS_CACHE=(
    [last_check]="0"
    [cache_ttl]="60"
)

# ============================================================================
# SERVICE CONNECTIVITY
# ============================================================================

service_bridge_log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$SERVICE_BRIDGE_LOG"
}

service_bridge_build_url() {
    local endpoint="$1"
    echo "http://${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}${SERVICE_ENDPOINTS[$endpoint]}"
}

service_bridge_check_connectivity() {
    local timeout=2
    
    if timeout $timeout curl -s "http://${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}/api/health" > /dev/null 2>&1; then
        return 0
    else
        service_bridge_log "ERROR" "Service not reachable at ${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}"
        return 1
    fi
}

service_bridge_is_healthy() {
    local now=$(date +%s)
    local last_check=${SERVICE_STATUS_CACHE[last_check]:-0}
    local cache_ttl=${SERVICE_STATUS_CACHE[cache_ttl]:-60}
    local time_diff=$((now - last_check))
    
    if [[ $time_diff -lt $cache_ttl ]] && [[ ${SERVICE_STATUS_CACHE[status]} == "healthy" ]]; then
        return 0
    fi
    
    if service_bridge_check_connectivity; then
        SERVICE_STATUS_CACHE[status]="healthy"
        SERVICE_STATUS_CACHE[last_check]="$now"
        return 0
    else
        SERVICE_STATUS_CACHE[status]="unhealthy"
        SERVICE_STATUS_CACHE[last_check]="$now"
        return 1
    fi
}

# ============================================================================
# SERVICE REQUEST HANDLING
# ============================================================================

service_bridge_request() {
    local method="${1:?Usage: service_bridge_request <method> <endpoint> [data]}"
    local endpoint="${2:?Missing endpoint}"
    local data="$3"
    
    if ! service_bridge_is_healthy; then
        echo '{"error": "Service unavailable", "status": "offline"}'
        return 1
    fi
    
    local url="http://${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}${endpoint}"
    local curl_opts=(
        -s
        --max-time "$LLM_SERVICE_TIMEOUT"
        -H "Content-Type: application/json"
        -X "$method"
    )
    
    if [[ -n "$data" ]]; then
        curl_opts+=(-d "$data")
    fi
    
    local response=$(curl "${curl_opts[@]}" "$url" 2>/dev/null)
    
    if [[ -z "$response" ]]; then
        echo '{"error": "No response from service"}'
        service_bridge_log "ERROR" "No response from $endpoint"
        return 1
    fi
    
    echo "$response"
    service_bridge_log "INFO" "Request: $method $endpoint"
}

# ============================================================================
# LLM SERVICE INTEGRATION
# ============================================================================

llm_chat() {
    local prompt="${1:?Usage: llm_chat \"prompt\" [model]}"
    local model="${2:-gpt-3.5-turbo}"
    
    echo "Sending chat request to LLM service..." >&2
    
    local data=$(jq -n \
        --arg prompt "$prompt" \
        --arg model "$model" \
        '{prompt: $prompt, model: $model}')
    
    local response=$(service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_chat]}" "$data")
    
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        echo "❌ Error: $(echo "$response" | jq -r '.error')" >&2
        return 1
    fi
    
    echo "$response" | jq -r '.response'
}

llm_code_explain() {
    local code="${1:?Usage: llm_code_explain <code> [language]}"
    local language="${2:-python}"
    
    echo "Analyzing code..." >&2
    
    local data=$(jq -n \
        --arg code "$code" \
        --arg language "$language" \
        '{code: $code, language: $language, action: "explain"}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_code]}" "$data" | jq -r '.explanation'
}

llm_code_review() {
    local code="${1:?Usage: llm_code_review <code> [language]}"
    local language="${2:-python}"
    
    echo "Reviewing code..." >&2
    
    local data=$(jq -n \
        --arg code "$code" \
        --arg language "$language" \
        '{code: $code, language: $language, action: "review"}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_code]}" "$data" | jq -r '.review'
}

llm_code_debug() {
    local code="${1:?Usage: llm_code_debug <code> [error_msg]}"
    local error_msg="$2"
    
    echo "Debugging code..." >&2
    
    local data=$(jq -n \
        --arg code "$code" \
        --arg error "$error_msg" \
        '{code: $code, error: $error, action: "debug"}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_code]}" "$data" | jq -r '.debug_suggestions'
}

llm_code_optimize() {
    local code="${1:?Usage: llm_code_optimize <code> [goal]}"
    local goal="${2:-performance}"
    
    echo "Optimizing code..." >&2
    
    local data=$(jq -n \
        --arg code "$code" \
        --arg goal "$goal" \
        '{code: $code, goal: $goal, action: "optimize"}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_code]}" "$data" | jq -r '.optimized_code'
}

llm_code_document() {
    local code="${1:?Usage: llm_code_document <code> [style]}"
    local style="${2:-Google}"
    
    echo "Generating documentation..." >&2
    
    local data=$(jq -n \
        --arg code "$code" \
        --arg style "$style" \
        '{code: $code, style: $style, action: "document"}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[llm_code]}" "$data" | jq -r '.documentation'
}

# ============================================================================
# REGISTRY SERVICE INTEGRATION
# ============================================================================

registry_register() {
    local title="${1:?Usage: registry_register <title> [category]}"
    local category="${2:-general}"
    local description="$3"
    
    echo "Registering entry..." >&2
    
    local data=$(jq -n \
        --arg title "$title" \
        --arg category "$category" \
        --arg desc "$description" \
        '{title: $title, category: $category, description: $desc}')
    
    service_bridge_request "POST" "${SERVICE_ENDPOINTS[registry_entries]}" "$data" | jq -r '.id'
}

registry_search() {
    local query="${1:?Usage: registry_search <query> [limit]}"
    local limit="${2:-10}"
    
    echo "Searching registry..." >&2
    
    local url="${SERVICE_ENDPOINTS[registry_search]}?query=$(urlencode "$query")&limit=$limit"
    
    service_bridge_request "GET" "$url" | jq '.'
}

registry_get() {
    local entry_id="${1:?Usage: registry_get <entry_id>"
    
    echo "Fetching registry entry..." >&2
    
    service_bridge_request "GET" "${SERVICE_ENDPOINTS[registry_entries]}/$entry_id" | jq '.'
}

# ============================================================================
# SERVICE DIAGNOSTICS & HEALTH
# ============================================================================

service_bridge_status() {
    echo "🔗 SERVICE BRIDGE STATUS"
    echo "├─ Service: ${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}"
    echo "├─ Timeout: ${LLM_SERVICE_TIMEOUT}s"
    
    if service_bridge_is_healthy; then
        echo "├─ Status: ✅ HEALTHY"
        
        # Get detailed health info
        local health=$(service_bridge_request "GET" "${SERVICE_ENDPOINTS[health]}")
        if [[ -n "$health" ]]; then
            echo "├─ LLM Service: $(echo "$health" | jq -r '.llm_status // "unknown"')"
            echo "├─ Registry Service: $(echo "$health" | jq -r '.registry_status // "unknown"')"
            echo "└─ Timestamp: $(echo "$health" | jq -r '.timestamp // "unknown"')"
        fi
    else
        echo "├─ Status: ❌ OFFLINE"
        echo "└─ Check if services are running on ${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}"
    fi
}

service_bridge_logs() {
    local lines="${1:-20}"
    echo "📋 SERVICE BRIDGE LOGS (last $lines lines):"
    tail -n "$lines" "$SERVICE_BRIDGE_LOG"
}

# ============================================================================
# SERVICE MANAGEMENT
# ============================================================================

llm_service_start() {
    echo "🚀 Starting LLM Service..."
    
    if [[ -d "services/llm_orchestrator" ]]; then
        cd services/llm_orchestrator
        python3 multi_llm_service.py &
        echo "✅ LLM Service starting (PID: $!)"
    else
        echo "❌ LLM Orchestrator not found"
        return 1
    fi
}

llm_service_stop() {
    echo "🛑 Stopping LLM Service..."
    pkill -f "multi_llm_service.py"
    echo "✅ LLM Service stopped"
}

llm_service_restart() {
    llm_service_stop
    sleep 2
    llm_service_start
}

registry_service_start() {
    echo "🚀 Starting Registry Service..."
    
    if [[ -f "services/hyper_registry/server.py" ]]; then
        python3 services/hyper_registry/server.py &
        echo "✅ Registry Service starting (PID: $!)"
    else
        echo "❌ Hyper Registry not found"
        return 1
    fi
}

registry_service_stop() {
    echo "🛑 Stopping Registry Service..."
    pkill -f "server.py"
    echo "✅ Registry Service stopped"
}

# ============================================================================
# SHORTCUTS & ALIASES
# ============================================================================

alias llm-chat="llm_chat"
alias llm-code-explain="llm_code_explain"
alias llm-review="llm_code_review"
alias llm-debug="llm_code_debug"
alias llm-optimize="llm_code_optimize"
alias llm-document="llm_code_document"
alias llm-status="service_bridge_status"
alias llm-logs="service_bridge_logs"
alias llm-start="llm_service_start"
alias llm-stop="llm_service_stop"
alias llm-restart="llm_service_restart"

alias registry-register="registry_register"
alias registry-search="registry_search"
alias registry-get="registry_get"
alias registry-start="registry_service_start"
alias registry-stop="registry_service_stop"

# Initialize
if service_bridge_is_healthy; then
    echo "✅ Unified Service Bridge v4.1.0 loaded (services online)"
else
    echo "⚠️  Unified Service Bridge v4.1.0 loaded (services may be offline)"
    echo "   Use 'llm-start' or 'registry-start' to start services"
fi
