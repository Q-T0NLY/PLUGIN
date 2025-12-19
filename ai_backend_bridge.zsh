#!/usr/bin/env zsh
# ============================================================================
# 🌉 NEXUS AI-BACKEND INTEGRATION BRIDGE
# ============================================================================
# Connects Zsh frontend with Python backend AI services via REST/WebSocket
# ============================================================================

[[ -n "$NEXUS_AI_BRIDGE_LOADED" ]] && return
export NEXUS_AI_BRIDGE_LOADED=1

export NEXUS_API_HOST="${NEXUS_API_HOST:-localhost}"
export NEXUS_API_PORT="${NEXUS_API_PORT:-8000}"
export NEXUS_API_BASE="http://${NEXUS_API_HOST}:${NEXUS_API_PORT}"
export NEXUS_BACKEND_TIMEOUT=30

# ============================================================================
# 🔌 BACKEND COMMUNICATION
# ============================================================================

nexus_backend_call() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local timeout="${4:-$NEXUS_BACKEND_TIMEOUT}"
    
    local url="${NEXUS_API_BASE}${endpoint}"
    
    if [[ "$method" == "GET" ]]; then
        curl -s -X GET "$url" -w "\n%{http_code}" --max-time "$timeout" 2>/dev/null
    elif [[ "$method" == "POST" ]]; then
        curl -s -X POST "$url" \
            -H "Content-Type: application/json" \
            -d "$data" \
            -w "\n%{http_code}" \
            --max-time "$timeout" 2>/dev/null
    fi
}

nexus_backend_health() {
    local response=$(nexus_backend_call "GET" "/health" "" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    
    if [[ "$http_code" == "200" ]]; then
        echo "ok"
        return 0
    else
        echo "down"
        return 1
    fi
}

# ============================================================================
# 🧠 UNIFIED AI ROUTER (ZSH + BACKEND)
# ============================================================================

nexus_ai_smart_router() {
    local prompt="$1"
    local strategy="${2:-auto}"  # auto, consensus, fastest, cost-optimized
    
    if ! nexus_backend_health > /dev/null; then
        echo "${AI_ERROR_COLOR}⚠️  Backend unavailable, using local router${RESET}"
        nexus_ai_router "$prompt"
        return $?
    fi
    
    # Check prompt size - use backend for complex queries
    local prompt_length=${#prompt}
    
    if [[ $prompt_length -gt 200 ]] || [[ "$strategy" != "auto" ]]; then
        nexus_ai_backend_router "$prompt" "$strategy"
    else
        nexus_ai_router "$prompt"
    fi
}

nexus_ai_backend_router() {
    local prompt="$1"
    local strategy="${2:-consensus}"
    
    # Build JSON payload
    local payload=$(cat <<EOF
{
    "prompt": "$prompt",
    "strategy": "$strategy",
    "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
EOF
)
    
    echo -e "${AI_THINKING_COLOR}🔄 Connecting to backend...${RESET}"
    
    local response=$(nexus_backend_call "POST" "/v1/ai/route" "$payload" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        echo "$body" | jq -r '.response' 2>/dev/null || echo "$body"
    else
        echo "${AI_ERROR_COLOR}❌ Backend error (HTTP $http_code)${RESET}"
        nexus_ai_router "$prompt"
    fi
}

# ============================================================================
# ⚖️ MULTI-MODEL CONSENSUS (BACKEND)
# ============================================================================

nexus_ai_backend_consensus() {
    local prompt="$1"
    shift
    local models=("$@")
    
    if [[ ${#models[@]} -eq 0 ]]; then
        models=("gpt-4o" "claude-3-7-sonnet" "gemini-3")
    fi
    
    local models_json=$(printf '%s\n' "${models[@]}" | jq -R . | jq -s .)
    
    local payload=$(cat <<EOF
{
    "prompt": "$prompt",
    "models": $models_json,
    "strategy": "consensus"
}
EOF
)
    
    echo -e "${AI_THINKING_COLOR}⚖️  Running multi-model consensus...${RESET}"
    
    local response=$(nexus_backend_call "POST" "/v1/ai/consensus" "$payload" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        # Fallback to local consensus
        nexus_ai_consensus "$prompt" "${models[@]}"
    fi
}

# ============================================================================
# 📊 PROVIDER REGISTRY SYNC
# ============================================================================

nexus_ai_sync_registry() {
    echo -e "${AI_THINKING_COLOR}📦 Syncing provider registry...${RESET}"
    
    local response=$(nexus_backend_call "GET" "/registries/ai_registry.json" "" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        # Save registry
        mkdir -p "$(dirname "$AI_REGISTRY")"
        echo "$body" | jq '.' > "$AI_REGISTRY"
        echo -e "${AI_RESPONSE_COLOR}✅ Registry synced${RESET}"
    else
        echo -e "${AI_ERROR_COLOR}⚠️  Could not sync registry${RESET}"
    fi
}

nexus_ai_get_provider_health() {
    local provider="$1"
    
    if ! nexus_backend_health > /dev/null; then
        echo "unknown"
        return 1
    fi
    
    local response=$(nexus_backend_call "GET" "/health/adapters" "" 2>/dev/null)
    local body=$(echo "$response" | sed '$d')
    
    echo "$body" | jq -r ".adapters.\"$provider\".status // \"unknown\"" 2>/dev/null || echo "unknown"
}

nexus_ai_list_backend_models() {
    if ! nexus_backend_health > /dev/null; then
        nexus_ai_list_models
        return 1
    fi
    
    echo -e "${AI_MODEL_COLOR}🤖 [BACKEND AI MODELS]${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    
    local response=$(nexus_backend_call "GET" "/v1/ai/models" "" 2>/dev/null)
    local body=$(echo "$response" | sed '$d')
    
    echo "$body" | jq -r '.models[] | "  • \(.name) (\(.provider)) - Cost: \(.cost) | Latency: \(.latency)ms"' 2>/dev/null || \
        nexus_ai_list_models
}

# ============================================================================
# 🔐 CREDENTIAL MANAGEMENT (BACKEND)
# ============================================================================

nexus_ai_backend_add_key() {
    local provider="$1"
    local key="$2"
    
    if [[ -z "$provider" ]] || [[ -z "$key" ]]; then
        echo "${AI_ERROR_COLOR}❌ Usage: nexus_ai_backend_add_key <provider> <key>${RESET}"
        return 1
    fi
    
    local payload=$(cat <<EOF
{
    "provider": "$provider",
    "api_key": "$key"
}
EOF
)
    
    local response=$(nexus_backend_call "POST" "/v1/ai/credentials" "$payload" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    
    if [[ "$http_code" == "201" ]]; then
        # Also store locally
        nexus_ai_add_key "$provider" "$key"
        echo -e "${AI_RESPONSE_COLOR}✅ Key registered with backend${RESET}"
    else
        echo -e "${AI_ERROR_COLOR}❌ Backend registration failed${RESET}"
    fi
}

# ============================================================================
# 🎯 ADVANCED AI TOOLS (BACKEND)
# ============================================================================

nexus_ai_backend_code_analysis() {
    local file_path="$1"
    local analysis_type="${2:-full}"  # full, security, performance, style
    
    if [[ ! -f "$file_path" ]]; then
        echo "${AI_ERROR_COLOR}❌ File not found: $file_path${RESET}"
        return 1
    fi
    
    local code_content=$(head -200 "$file_path" | sed 's/"/\\"/g')
    local file_ext="${file_path##*.}"
    
    local payload=$(cat <<EOF
{
    "file_path": "$file_path",
    "language": "$file_ext",
    "code": "$code_content",
    "analysis_type": "$analysis_type"
}
EOF
)
    
    echo -e "${AI_THINKING_COLOR}🔍 Running backend code analysis...${RESET}"
    
    local response=$(nexus_backend_call "POST" "/v1/ai/analyze-code" "$payload" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        nexus_ai_code_review "$file_path"
    fi
}

nexus_ai_backend_project_analysis() {
    local project_path="${1:-.}"
    
    local payload=$(cat <<EOF
{
    "project_path": "$project_path",
    "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
EOF
)
    
    echo -e "${AI_THINKING_COLOR}📈 Analyzing project...${RESET}"
    
    local response=$(nexus_backend_call "POST" "/v1/ai/analyze-project" "$payload" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d')
    
    if [[ "$http_code" == "200" ]]; then
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        nexus_ai_score_project "$project_path"
    fi
}

nexus_ai_backend_chat_session() {
    local session_id="${1:-$(uuidgen 2>/dev/null || echo "session-$(date +%s)')}"
    
    echo -e "${AI_THINKING_COLOR}💬 Starting chat session: $session_id${RESET}"
    
    while true; do
        read -p "${AI_PROMPT_COLOR}You: ${RESET}" prompt
        
        if [[ "$prompt" == "exit" ]] || [[ "$prompt" == "quit" ]]; then
            echo -e "${AI_RESPONSE_COLOR}👋 Session ended${RESET}"
            break
        fi
        
        local payload=$(cat <<EOF
{
    "session_id": "$session_id",
    "message": "$prompt",
    "timestamp": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
EOF
)
        
        local response=$(nexus_backend_call "POST" "/v1/ai/chat" "$payload" 2>/dev/null)
        local http_code=$(echo "$response" | tail -1)
        local body=$(echo "$response" | sed '$d')
        
        if [[ "$http_code" == "200" ]]; then
            echo -e "${AI_RESPONSE_COLOR}AI: $(echo "$body" | jq -r '.response // .message' 2>/dev/null)${RESET}"
        else
            echo -e "${AI_ERROR_COLOR}Error: $(echo "$body" | jq -r '.error // "Unknown error"' 2>/dev/null)${RESET}"
        fi
        
        echo ""
    done
}

# ============================================================================
# 📊 MONITORING & OBSERVABILITY
# ============================================================================

nexus_ai_backend_metrics() {
    echo -e "${AI_MODEL_COLOR}📊 [AI BACKEND METRICS]${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    
    local response=$(nexus_backend_call "GET" "/metrics/ai" "" 2>/dev/null)
    local body=$(echo "$response" | sed '$d')
    
    if echo "$body" | jq empty 2>/dev/null; then
        echo -e "${AI_RESPONSE_COLOR}Provider Statistics:${RESET}"
        echo "$body" | jq '.providers[] | "  \(.name): \(.calls) calls, \(.avg_latency)ms avg latency"' 2>/dev/null
        
        echo ""
        echo -e "${AI_RESPONSE_COLOR}Model Statistics:${RESET}"
        echo "$body" | jq '.models[] | "  \(.name): \(.uses) uses, \(.avg_cost) avg cost"' 2>/dev/null
    else
        echo "${AI_ERROR_COLOR}❌ Could not fetch metrics${RESET}"
    fi
}

nexus_ai_backend_logs() {
    local limit="${1:-20}"
    
    local response=$(nexus_backend_call "GET" "/logs/ai?limit=$limit" "" 2>/dev/null)
    local body=$(echo "$response" | sed '$d')
    
    echo "$body" | jq '.logs[] | "[\(.timestamp)] \(.level): \(.message)"' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}❌ Could not fetch logs${RESET}"
}

# ============================================================================
# 🔄 BACKEND FALLBACK LOGIC
# ============================================================================

nexus_ai_hybrid_call() {
    local prompt="$1"
    local strategy="${2:-auto}"
    
    # Try backend first
    if nexus_backend_health > /dev/null 2>&1; then
        nexus_ai_backend_router "$prompt" "$strategy"
        return $?
    fi
    
    # Fallback to local if backend is down
    echo -e "${AI_ERROR_COLOR}⚠️  Backend unavailable, using local fallback${RESET}"
    nexus_ai_router "$prompt"
}

# ============================================================================
# INITIALIZATION
# ============================================================================

# Health check on load
if nexus_backend_health > /dev/null 2>&1; then
    echo -e "${AI_RESPONSE_COLOR}✅ AI Backend connected${RESET}"
    nexus_ai_sync_registry
else
    echo -e "${AI_ERROR_COLOR}⚠️  AI Backend unavailable - using local mode${RESET}"
fi

export NEXUS_AI_BRIDGE_LOADED=1
