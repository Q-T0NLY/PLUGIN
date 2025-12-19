#!/usr/bin/env zsh
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║         🌉 LLM SERVICE BRIDGE - Terminal ↔ Multi-LLM Orchestrator       ║
# ║     Real-time communication bridge between ZSH and Python services      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

[[ -n "$NEXUS_LLM_BRIDGE_LOADED" ]] && return
export NEXUS_LLM_BRIDGE_LOADED=1

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

export LLM_SERVICE_HOST="${LLM_SERVICE_HOST:-localhost}"
export LLM_SERVICE_PORT="${LLM_SERVICE_PORT:-8000}"
export LLM_SERVICE_URL="http://${LLM_SERVICE_HOST}:${LLM_SERVICE_PORT}"
export LLM_TIMEOUT=30

# Color codes
export C_RESET='\033[0m'
export C_BOLD='\033[1m'
export C_DIM='\033[2m'
export C_GREEN='\033[38;2;48;209;88m'
export C_YELLOW='\033[38;2;255;214;10m'
export C_CYAN='\033[38;2;100;210;255m'
export C_RED='\033[38;2;255;59;48m'

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE HEALTH CHECK
# ─────────────────────────────────────────────────────────────────────────────

llm_service_health() {
    local response=$(curl -s -m 3 -w "\n%{http_code}" "${LLM_SERVICE_URL}/health" 2>/dev/null)
    local http_code=$(echo "$response" | tail -1)
    
    if [[ "$http_code" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

llm_service_check() {
    if llm_service_health; then
        echo -e "${C_GREEN}✓ LLM Service: ONLINE${C_RESET}"
        return 0
    else
        echo -e "${C_RED}✗ LLM Service: OFFLINE${C_RESET}"
        echo -e "${C_DIM}  Hint: Start service with: python3 services/llm_orchestrator/multi_llm_service.py${C_RESET}"
        return 1
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# SINGLE PROVIDER INFERENCE
# ─────────────────────────────────────────────────────────────────────────────

llm_invoke() {
    local prompt="$1"
    local provider="${2:-openai}"
    local model="${3:-gpt-4}"
    local temperature="${4:-0.7}"
    local max_tokens="${5:-2000}"
    
    # Build request
    local request_json=$(cat <<EOF
{
  "prompt": "$prompt",
  "providers": [
    {
      "name": "$provider",
      "params": {
        "model": "$model",
        "temperature": $temperature,
        "max_tokens": $max_tokens
      }
    }
  ],
  "temperature": $temperature,
  "max_tokens": $max_tokens
}
EOF
)
    
    # Make request
    local response=$(curl -s -m "$LLM_TIMEOUT" \
        -X POST "${LLM_SERVICE_URL}/multi-llm/invoke" \
        -H "Content-Type: application/json" \
        -d "$request_json" 2>/dev/null)
    
    # Check response
    if [[ -z "$response" ]]; then
        echo -e "${C_RED}✗ Service error or timeout${C_RESET}"
        return 1
    fi
    
    # Extract response text
    echo "$response" | jq -r '.responses[0].text // .error // "Error processing request"' 2>/dev/null
}

# ─────────────────────────────────────────────────────────────────────────────
# MULTI-PROVIDER ENSEMBLE INFERENCE
# ─────────────────────────────────────────────────────────────────────────────

llm_ensemble() {
    local prompt="$1"
    local providers="${2:-openai,claude,ollama}"
    
    # Build providers array
    local providers_json="["
    IFS=',' read -ra PROVIDERS <<< "$providers"
    for i in "${!PROVIDERS[@]}"; do
        local p="${PROVIDERS[$i]}"
        if [[ $i -gt 0 ]]; then providers_json+=","; fi
        providers_json+="{\"name\":\"$p\",\"params\":{}}"
    done
    providers_json+="]"
    
    # Build request
    local request_json="{
      \"prompt\": \"$prompt\",
      \"providers\": $providers_json,
      \"temperature\": 0.7,
      \"max_tokens\": 2000
    }"
    
    # Make request
    curl -s -m "$LLM_TIMEOUT" \
        -X POST "${LLM_SERVICE_URL}/multi-llm/ensemble" \
        -H "Content-Type: application/json" \
        -d "$request_json" 2>/dev/null | jq '.fused.text // .error // "Error"' 2>/dev/null
}

# ─────────────────────────────────────────────────────────────────────────────
# STREAMING INFERENCE
# ─────────────────────────────────────────────────────────────────────────────

llm_stream() {
    local prompt="$1"
    local provider="${2:-openai}"
    
    # Stream response with visual feedback
    echo -ne "${C_CYAN}Assistant: ${C_RESET}"
    
    curl -s -N -m "$LLM_TIMEOUT" \
        -X POST "${LLM_SERVICE_URL}/multi-llm/stream" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\":\"$prompt\",\"providers\":[{\"name\":\"$provider\"}]}" 2>/dev/null | \
        jq -r '.text // .error' 2>/dev/null | \
        while IFS= read -r -n1 char; do
            echo -ne "${C_CYAN}${char}${C_RESET}"
            sleep 0.02
        done
    echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# CODE ANALYSIS & GENERATION
# ─────────────────────────────────────────────────────────────────────────────

llm_code_review() {
    local code="$1"
    local language="${2:-python}"
    
    local prompt="Review this ${language} code and provide constructive feedback:

\`\`\`${language}
${code}
\`\`\`

Focus on:
- Correctness and logic
- Performance optimization
- Code style and best practices
- Security considerations
- Potential bugs or issues"
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.5 2000
}

llm_code_generate() {
    local description="$1"
    local language="${2:-python}"
    
    local prompt="Write production-quality ${language} code to: $description

Requirements:
- Include proper error handling
- Add meaningful comments
- Follow ${language} best practices
- Make it efficient and maintainable
- Include a brief usage example

Provide only the code in a markdown code block."
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.7 2000
}

llm_code_explain() {
    local code="$1"
    local language="${2:-python}"
    
    local prompt="Explain this ${language} code in detail:

\`\`\`${language}
${code}
\`\`\`

Cover:
- What it does
- How it works
- Key concepts
- Potential use cases
- Any gotchas or important notes"
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.3 2000
}

# ─────────────────────────────────────────────────────────────────────────────
# SPECIALIZED TASKS
# ─────────────────────────────────────────────────────────────────────────────

llm_debug() {
    local error="$1"
    local context="${2:-General error}"
    
    local prompt="Help me debug this error in the context of: $context

Error message:
${error}

Please:
1. Explain what the error means
2. List common causes
3. Suggest solutions
4. Provide code examples if applicable"
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.5 2000
}

llm_optimize() {
    local code="$1"
    local goal="${2:-general performance}"
    
    local prompt="Optimize this code for ${goal}:

\`\`\`
${code}
\`\`\`

Provide:
- Optimized code
- Explanation of improvements
- Performance impact estimate
- Trade-offs (if any)"
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.3 2000
}

llm_document() {
    local code="$1"
    local style="${2:-Google}"
    
    local prompt="Add comprehensive ${style}-style documentation to this code:

\`\`\`
${code}
\`\`\`

Include:
- Module/file docstring
- Function/method docstrings
- Parameter descriptions
- Return value descriptions
- Usage examples where appropriate"
    
    llm_invoke "$prompt" "openai" "gpt-4" 0.5 2000
}

# ─────────────────────────────────────────────────────────────────────────────
# CLI COMMANDS
# ─────────────────────────────────────────────────────────────────────────────

# Quick alias: llm "your prompt"
llm() {
    if llm_service_health; then
        llm_invoke "$@"
    else
        echo -e "${C_RED}✗ LLM Service unavailable${C_RESET}"
        return 1
    fi
}

# Ensemble: llm-ensemble "your prompt" [provider1,provider2,provider3]
llm-ensemble() {
    if llm_service_health; then
        llm_ensemble "$@"
    else
        echo -e "${C_RED}✗ LLM Service unavailable${C_RESET}"
        return 1
    fi
}

# Stream: llm-stream "your prompt"
llm-stream() {
    if llm_service_health; then
        llm_stream "$@"
    else
        echo -e "${C_RED}✗ LLM Service unavailable${C_RESET}"
        return 1
    fi
}

# Review code: llm-review < file.py
llm-review() {
    local code=$(cat)
    llm_code_review "$code" "${1:-python}"
}

# Generate code: llm-generate "description" [language]
llm-generate() {
    llm_code_generate "$@"
}

# Explain code: llm-explain < file.py
llm-explain() {
    local code=$(cat)
    llm_code_explain "$code" "${1:-python}"
}

# Debug: llm-debug "error message" [context]
llm-debug() {
    llm_debug "$@"
}

# Optimize: llm-optimize < file.py [goal]
llm-optimize() {
    local code=$(cat)
    llm_optimize "$code" "${1:-general performance}"
}

# Document: llm-document < file.py [style]
llm-document() {
    local code=$(cat)
    llm_document "$code" "${1:-Google}"
}

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

llm_service_start() {
    echo -e "${C_YELLOW}Starting LLM Service...${C_RESET}"
    
    if [[ -d "services/llm_orchestrator" ]]; then
        cd services/llm_orchestrator
        pip3 install -r requirements.txt -q
        python3 multi_llm_service.py &
        sleep 2
        llm_service_check
    else
        echo -e "${C_RED}✗ Service directory not found${C_RESET}"
        return 1
    fi
}

llm_service_stop() {
    echo -e "${C_YELLOW}Stopping LLM Service...${C_RESET}"
    pkill -f "multi_llm_service.py" 2>/dev/null
    echo -e "${C_GREEN}✓ Service stopped${C_RESET}"
}

# ─────────────────────────────────────────────────────────────────────────────
# EXPORT FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

export -f llm_service_health
export -f llm_service_check
export -f llm_invoke
export -f llm_ensemble
export -f llm_stream
export -f llm_code_review
export -f llm_code_generate
export -f llm_code_explain
export -f llm_debug
export -f llm_optimize
export -f llm_document
export -f llm
export -f llm-ensemble
export -f llm-stream
export -f llm_service_start
export -f llm_service_stop
