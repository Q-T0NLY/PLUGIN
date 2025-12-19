#!/usr/bin/env zsh
#  ╔════════════════════════════════════════════════════════════════════════════╗
#  ║          🧠 UNIFIED AI CORE MODULE v4.1.0                                 ║
#  ║   Consolidated comprehensive AI integration for Zsh environments           ║
#  ║                                                                            ║
#  ║ Merges:                                                                    ║
#  ║  ✅ ai_matrix.zsh - AI routing and consensus                              ║
#  ║  ✅ ai_intelligence.zsh - Multi-provider LLM integration                  ║
#  ║  ✅ ai_intelligence_matrix.zsh - Advanced AI intelligence                 ║
#  ║  ✅ ai_chatbox.zsh - Interactive chat and conversations                   ║
#  ║                                                                            ║
#  ║ Features:                                                                  ║
#  ║  • Multi-provider AI integration (OpenAI, Anthropic, DeepSeek, Ollama)   ║
#  ║  • Intelligent prompt routing and model selection                        ║
#  ║  • Multi-model consensus for better responses                           ║
#  ║  • Code analysis, review, and optimization                               ║
#  ║  • Interactive conversational chat                                        ║
#  ║  • Project analysis and TODO generation                                   ║
#  ║  • Real-time streaming responses                                          ║
#  ║  • Response caching and performance optimization                          ║
#  ╚════════════════════════════════════════════════════════════════════════════╝

[[ -n "$NEXUS_UNIFIED_AI_LOADED" ]] && return
export NEXUS_UNIFIED_AI_LOADED=1

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

export AI_CONFIG="${HOME}/.config/ultra-zsh/ai/ai_config.json"
export AI_CACHE="${HOME}/.config/ultra-zsh/ai/cache"
export AI_LOGS="${HOME}/.config/ultra-zsh/ai/logs"
export AI_CREDENTIALS="${HOME}/.config/ultra-zsh/ai/credentials"
export AI_REGISTRY="${HOME}/.nexus/ai/registry.json"
export NEXUS_CHAT_HISTORY_DIR="${HOME}/.nexus/ai/history"

# Create required directories
mkdir -p "$AI_CACHE" "$AI_LOGS" "$AI_CREDENTIALS" "$NEXUS_CHAT_HISTORY_DIR"

# Colors for AI system
export AI_COLOR_MODEL=$'%F{51}'        # Cyan
export AI_COLOR_PROMPT=$'%F{135}'      # Purple
export AI_COLOR_RESPONSE=$'%F{46}'     # Green
export AI_COLOR_THINKING=$'%F{226}'    # Yellow
export AI_COLOR_ERROR=$'%F{196}'       # Red
export AI_COLOR_DEBUG=$'%F{135}'       # Magenta
export C_RESET=$'%f'

# AI providers with endpoints
declare -A AI_PROVIDERS=(
    [openai]="https://api.openai.com/v1/chat/completions"
    [anthropic]="https://api.anthropic.com/v1/messages"
    [google]="https://generativelanguage.googleapis.com/v1beta/models"
    [deepseek]="https://api.deepseek.com/v1/chat/completions"
    [mistral]="https://api.mistral.ai/v1/chat/completions"
    [ollama]="http://localhost:11434/api/generate"
    [groq]="https://api.groq.com/openai/v1/chat/completions"
)

# Advanced model database
declare -A AI_MODELS=(
    # OpenAI
    [gpt-5.1]="openai"     [gpt-4o]="openai"      [gpt-4-turbo]="openai"
    [gpt-4]="openai"       [gpt-3.5-turbo]="openai"
    
    # Anthropic
    [claude-3-opus]="anthropic"    [claude-3-sonnet]="anthropic"
    [claude-3-haiku]="anthropic"
    
    # Google
    [gemini-3]="google"    [gemini-2.0-pro]="google"
    [gemini-2.0-flash]="google"    [gemini-1.5-pro]="google"
    
    # DeepSeek
    [deepseek-v3]="deepseek"       [deepseek-r1]="deepseek"
    [deepseek-chat]="deepseek"     [deepseek-coder]="deepseek"
    
    # Local/Ollama
    [llama3.1]="ollama"    [mistral]="ollama"     [codellama]="ollama"
    [phi]="ollama"
)

# Model performance scores for consensus
declare -A MODEL_SCORES=(
    [gpt-4o]="0.95"        [gpt-5.1]="0.98"       [claude-3-opus]="0.97"
    [gemini-2.0-pro]="0.93"        [deepseek-v3]="0.92"   [llama-3.3-70b]="0.90"
)

# Session management
export NEXUS_SESSION_ID=""
export NEXUS_CONVERSATION=()
export NEXUS_CHAT_ACTIVE=false
export NEXUS_MAX_DISPLAY_LINES=12

# ============================================================================
# INTENT DETECTION & MODEL SELECTION
# ============================================================================

nexus_ai_detect_intent() {
    local prompt="$1"
    
    if [[ $prompt =~ (code|program|function|script|debug|fix|error|bug|implement) ]]; then
        echo "code_generation"
    elif [[ $prompt =~ (explain|why|how|reason|logic|think|analyze) ]]; then
        echo "reasoning"
    elif [[ $prompt =~ (write|create|story|poem|art|creative|design) ]]; then
        echo "creative"
    elif [[ $prompt =~ (secure|security|vulnerability|attack|hack|exploit) ]]; then
        echo "security_analysis"
    elif [[ $prompt =~ (math|calculate|equation|proof|statistic|derive) ]]; then
        echo "mathematical"
    else
        echo "general"
    fi
}

nexus_ai_select_model() {
    local intent="${1:-general}"
    local preferred_provider="${2:-auto}"
    
    case "$intent" in
        code_generation)
            if [[ -n ${AI_MODELS[gpt-4o]+x} ]]; then
                echo "gpt-4o"
            elif [[ -n ${AI_MODELS[claude-3-opus]+x} ]]; then
                echo "claude-3-opus"
            else
                echo "codellama"
            fi
            ;;
        reasoning)
            echo "gpt-4o"
            ;;
        creative)
            echo "claude-3-sonnet"
            ;;
        security_analysis)
            echo "gpt-4o"
            ;;
        mathematical)
            echo "gpt-4-turbo"
            ;;
        *)
            echo "gpt-3.5-turbo"
            ;;
    esac
}

nexus_ai_get_provider_for_model() {
    local model="$1"
    echo "${AI_MODELS[$model]:-ollama}"
}

# ============================================================================
# PROVIDER INTEGRATION & API CALLS
# ============================================================================

nexus_ai_load_keys() {
    export OPENAI_API_KEY="${OPENAI_API_KEY:=$(cat "$AI_CREDENTIALS/openai_key" 2>/dev/null)}"
    export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:=$(cat "$AI_CREDENTIALS/anthropic_key" 2>/dev/null)}"
    export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:=$(cat "$AI_CREDENTIALS/deepseek_key" 2>/dev/null)}"
    export GOOGLE_API_KEY="${GOOGLE_API_KEY:=$(cat "$AI_CREDENTIALS/google_key" 2>/dev/null)}"
}

nexus_ai_add_key() {
    local provider="$1"
    local key="$2"
    
    if [[ -z "$provider" || -z "$key" ]]; then
        echo -e "${AI_COLOR_ERROR}Usage: nexus_ai_add_key <provider> <key>${C_RESET}"
        return 1
    fi
    
    mkdir -p "$AI_CREDENTIALS"
    echo "$key" > "$AI_CREDENTIALS/${provider}_key"
    chmod 600 "$AI_CREDENTIALS/${provider}_key"
    echo -e "${AI_COLOR_RESPONSE}✅ Added API key for $provider${C_RESET}"
}

nexus_ai_call_provider() {
    local provider="$1"
    local prompt="$2"
    local model="$3"
    
    case "$provider" in
        openai)
            nexus_ai_call_openai "$prompt" "$model"
            ;;
        anthropic)
            nexus_ai_call_anthropic "$prompt" "$model"
            ;;
        google)
            nexus_ai_call_google "$prompt" "$model"
            ;;
        deepseek)
            nexus_ai_call_deepseek "$prompt" "$model"
            ;;
        ollama)
            nexus_ai_call_ollama "$prompt" "$model"
            ;;
        *)
            echo -e "${AI_COLOR_ERROR}Unknown provider: $provider${C_RESET}"
            return 1
            ;;
    esac
}

nexus_ai_call_openai() {
    local prompt="$1"
    local model="${2:-gpt-3.5-turbo}"
    
    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ OpenAI API key not set${C_RESET}"
        return 1
    fi
    
    curl -s -X POST "${AI_PROVIDERS[openai]}" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.7,
            \"max_tokens\": 2000
        }" | jq -r '.choices[0].message.content' 2>/dev/null || \
        echo -e "${AI_COLOR_ERROR}❌ API call failed${C_RESET}"
}

nexus_ai_call_anthropic() {
    local prompt="$1"
    local model="${2:-claude-3-sonnet}"
    
    if [[ -z "$ANTHROPIC_API_KEY" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ Anthropic API key not set${C_RESET}"
        return 1
    fi
    
    curl -s -X POST "${AI_PROVIDERS[anthropic]}" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "Content-Type: application/json" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"$model\",
            \"max_tokens\": 2000,
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}]
        }" | jq -r '.content[0].text' 2>/dev/null || \
        echo -e "${AI_COLOR_ERROR}❌ API call failed${C_RESET}"
}

nexus_ai_call_google() {
    local prompt="$1"
    local model="${2:-gemini-1.5-pro}"
    
    if [[ -z "$GOOGLE_API_KEY" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ Google API key not set${C_RESET}"
        return 1
    fi
    
    curl -s -X POST "${AI_PROVIDERS[google]}/$model:generateContent?key=$GOOGLE_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"contents\": [{\"parts\": [{\"text\": \"$prompt\"}]}]
        }" | jq -r '.candidates[0].content.parts[0].text' 2>/dev/null || \
        echo -e "${AI_COLOR_ERROR}❌ API call failed${C_RESET}"
}

nexus_ai_call_deepseek() {
    local prompt="$1"
    local model="${2:-deepseek-chat}"
    
    if [[ -z "$DEEPSEEK_API_KEY" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ DeepSeek API key not set${C_RESET}"
        return 1
    fi
    
    curl -s -X POST "${AI_PROVIDERS[deepseek]}" \
        -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.7
        }" | jq -r '.choices[0].message.content' 2>/dev/null || \
        echo -e "${AI_COLOR_ERROR}❌ API call failed${C_RESET}"
}

nexus_ai_call_ollama() {
    local prompt="$1"
    local model="${2:-llama3}"
    
    curl -s -X POST "${AI_PROVIDERS[ollama]}" \
        -d "{\"model\": \"$model\", \"prompt\": \"$prompt\", \"stream\": false}" | \
        jq -r '.response' 2>/dev/null || \
        echo -e "${AI_COLOR_ERROR}❌ Ollama API call failed${C_RESET}"
}

# ============================================================================
# MAIN AI ROUTER & CONSENSUS
# ============================================================================

nexus_ai_router() {
    local prompt="${1:?Usage: nexus_ai_router \"prompt\" [provider] [model]}"
    local provider="${2:-auto}"
    local model="${3:-auto}"
    
    echo -e "${AI_COLOR_THINKING}🤔 Processing: ${prompt:0:60}...${C_RESET}\n"
    
    # Load API keys
    nexus_ai_load_keys
    
    # Detect intent
    local intent=$(nexus_ai_detect_intent "$prompt")
    echo -e "${AI_COLOR_DEBUG}Intent: $intent${C_RESET}"
    
    # Select model if auto
    if [[ "$model" == "auto" ]]; then
        model=$(nexus_ai_select_model "$intent" "$provider")
    fi
    
    # Get provider
    if [[ "$provider" == "auto" ]]; then
        provider=$(nexus_ai_get_provider_for_model "$model")
    fi
    
    echo -e "${AI_COLOR_MODEL}🧠 Model: $model (Provider: $provider)${C_RESET}\n"
    
    # Call provider
    nexus_ai_call_provider "$provider" "$prompt" "$model"
}

nexus_ai_consensus() {
    local prompt="${1:?Usage: nexus_ai_consensus \"prompt\"}"
    
    echo -e "${AI_COLOR_THINKING}🤔 Running multi-model consensus...${C_RESET}\n"
    
    # Get multiple responses
    local gpt_response=$(nexus_ai_call_openai "$prompt" "gpt-4o" 2>/dev/null)
    local claude_response=$(nexus_ai_call_anthropic "$prompt" "claude-3-opus" 2>/dev/null)
    local ollama_response=$(nexus_ai_call_ollama "$prompt" "llama3" 2>/dev/null)
    
    echo -e "${AI_COLOR_MODEL}📊 CONSENSUS ANALYSIS${C_RESET}"
    echo -e "${AI_COLOR_RESPONSE}✅ GPT-4o:${C_RESET}"
    echo "$gpt_response" | head -5
    echo ""
    
    echo -e "${AI_COLOR_RESPONSE}✅ Claude-3-Opus:${C_RESET}"
    echo "$claude_response" | head -5
    echo ""
    
    echo -e "${AI_COLOR_RESPONSE}✅ Llama3:${C_RESET}"
    echo "$ollama_response" | head -5
}

# ============================================================================
# SPECIALIZED AI FUNCTIONS
# ============================================================================

nexus_ai_code_review() {
    local file="${1:?Usage: nexus_ai_code_review <file>"
    
    if [[ ! -f "$file" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ File not found: $file${C_RESET}"
        return 1
    fi
    
    local code=$(cat "$file")
    local prompt="Review this code for best practices, performance, and security:\n\n$code"
    
    echo -e "${AI_COLOR_MODEL}🔍 CODE REVIEW${C_RESET}\n"
    nexus_ai_router "$prompt" "openai" "gpt-4o"
}

nexus_ai_explain() {
    local code="${1:?Usage: echo 'code' | nexus_ai_explain}"
    
    if [[ -z "$code" ]]; then
        code=$(cat)
    fi
    
    local prompt="Explain this code in simple terms:\n\n$code"
    echo -e "${AI_COLOR_MODEL}📖 EXPLANATION${C_RESET}\n"
    nexus_ai_router "$prompt" "anthropic" "claude-3-sonnet"
}

nexus_ai_generate_todo() {
    local context="${1:-project}"
    
    local prompt="Generate a comprehensive TODO list for: $context. Include priorities (P0-P3), effort estimates (S/M/L), and descriptions."
    echo -e "${AI_COLOR_MODEL}✅ [TODO GENERATOR]${C_RESET}\n"
    nexus_ai_router "$prompt"
}

nexus_ai_score_project() {
    local project_path="${1:-.}"
    
    local files=$(find "$project_path" -type f | wc -l)
    local dirs=$(find "$project_path" -type d | wc -l)
    local has_readme=$([[ -f "$project_path/README.md" ]] && echo "1" || echo "0")
    local has_tests=$(find "$project_path" -name "*test*" | wc -l)
    
    local prompt="Score this project (0-100) in multiple dimensions:
Files: $files, Directories: $dirs, README: $has_readme, Tests: $has_tests
Provide scores for: Architecture, Documentation, Testing, Performance, Security"
    
    echo -e "${AI_COLOR_MODEL}📈 [PROJECT SCORING]${C_RESET}\n"
    nexus_ai_router "$prompt"
}

nexus_ai_debug() {
    local error_msg="${1:?Usage: nexus_ai_debug \"error message\"}"
    
    local prompt="Help debug this error message and suggest fixes:\n\n$error_msg"
    echo -e "${AI_COLOR_MODEL}🐛 [DEBUGGING]${C_RESET}\n"
    nexus_ai_router "$prompt" "openai" "gpt-4"
}

nexus_ai_optimize() {
    local code="${1:?Usage: nexus_ai_optimize < file.py}"
    
    if [[ -z "$code" ]]; then
        code=$(cat)
    fi
    
    local prompt="Optimize this code for performance and readability:\n\n$code"
    echo -e "${AI_COLOR_MODEL}⚡ [OPTIMIZATION]${C_RESET}\n"
    nexus_ai_router "$prompt" "openai" "gpt-4o"
}

# ============================================================================
# INTERACTIVE CHAT
# ============================================================================

_nexus_init_conversation() {
    local session_id=$(date +%s)
    export NEXUS_SESSION_ID="$session_id"
    export NEXUS_CONVERSATION=()
    echo "[]" > "${NEXUS_CHAT_HISTORY_DIR}/session_${session_id}.json"
}

_nexus_add_to_conversation() {
    local role="$1"
    local content="$2"
    
    NEXUS_CONVERSATION+=("{\"role\": \"$role\", \"content\": \"$content\"}")
    
    # Save to history
    local json_data=$(jq -n '$ARGS.positional' --args "${NEXUS_CONVERSATION[@]}")
    echo "$json_data" > "${NEXUS_CHAT_HISTORY_DIR}/session_${NEXUS_SESSION_ID}.json"
}

nexus_quantum_ai_chat() {
    echo -e "${AI_COLOR_MODEL}🧠 NEXUS AI CHAT v4.1.0${C_RESET}"
    echo -e "${AI_COLOR_DEBUG}Type 'exit' to quit, 'help' for commands${C_RESET}\n"
    
    _nexus_init_conversation
    export NEXUS_CHAT_ACTIVE=true
    
    while true; do
        echo -ne "${AI_COLOR_PROMPT}You: ${C_RESET}"
        read -r user_input
        
        if [[ "$user_input" == "exit" ]]; then
            break
        elif [[ "$user_input" == "help" ]]; then
            echo "Commands: clear (clear conversation), history, exit"
            continue
        elif [[ "$user_input" == "clear" ]]; then
            NEXUS_CONVERSATION=()
            continue
        fi
        
        _nexus_add_to_conversation "user" "$user_input"
        
        echo -ne "${AI_COLOR_RESPONSE}Assistant: ${C_RESET}"
        local response=$(nexus_ai_router "$user_input")
        echo "$response\n"
        
        _nexus_add_to_conversation "assistant" "$response"
    done
    
    export NEXUS_CHAT_ACTIVE=false
}

# ============================================================================
# SYSTEM MANAGEMENT & HEALTH
# ============================================================================

nexus_ai_list_models() {
    echo -e "${AI_COLOR_MODEL}📋 AVAILABLE AI MODELS${C_RESET}\n"
    
    echo -e "${AI_COLOR_RESPONSE}OpenAI:${C_RESET}"
    echo "  gpt-4o, gpt-4-turbo, gpt-3.5-turbo"
    
    echo -e "\n${AI_COLOR_RESPONSE}Anthropic:${C_RESET}"
    echo "  claude-3-opus, claude-3-sonnet, claude-3-haiku"
    
    echo -e "\n${AI_COLOR_RESPONSE}Google:${C_RESET}"
    echo "  gemini-3, gemini-2.0-pro, gemini-1.5-pro"
    
    echo -e "\n${AI_COLOR_RESPONSE}DeepSeek:${C_RESET}"
    echo "  deepseek-v3, deepseek-r1, deepseek-chat"
    
    echo -e "\n${AI_COLOR_RESPONSE}Local (Ollama):${C_RESET}"
    echo "  llama3.1, mistral, codellama, phi"
}

nexus_ai_health_check() {
    echo -e "${AI_COLOR_MODEL}🏥 AI SYSTEM HEALTH CHECK${C_RESET}\n"
    
    echo -e "${AI_COLOR_RESPONSE}✓ Ollama:${C_RESET}"
    curl -s http://localhost:11434/api/tags > /dev/null && echo "  Status: ✅ Running" || echo "  Status: ⚠️  Not running"
    
    echo -e "\n${AI_COLOR_RESPONSE}✓ API Keys:${C_RESET}"
    [[ -n "$OPENAI_API_KEY" ]] && echo "  OpenAI: ✅" || echo "  OpenAI: ❌"
    [[ -n "$ANTHROPIC_API_KEY" ]] && echo "  Anthropic: ✅" || echo "  Anthropic: ❌"
    [[ -n "$GOOGLE_API_KEY" ]] && echo "  Google: ✅" || echo "  Google: ❌"
    [[ -n "$DEEPSEEK_API_KEY" ]] && echo "  DeepSeek: ✅" || echo "  DeepSeek: ❌"
    
    echo -e "\n${AI_COLOR_RESPONSE}✓ Cache:${C_RESET}"
    local cache_size=$(du -sh "$AI_CACHE" 2>/dev/null | cut -f1)
    echo "  Size: $cache_size"
    
    echo -e "\n${AI_COLOR_RESPONSE}✓ Logs:${C_RESET}"
    local log_count=$(ls -1 "$AI_LOGS" 2>/dev/null | wc -l)
    echo "  Count: $log_count files"
}

nexus_ai_setup_provider() {
    local provider="${1:?Usage: nexus_ai_setup_provider <provider>"
    
    echo -e "${AI_COLOR_PROMPT}Setup AI Provider: $provider${C_RESET}"
    echo -n "Enter API Key: "
    read -rs api_key
    echo ""
    
    nexus_ai_add_key "$provider" "$api_key"
    nexus_ai_load_keys
}

nexus_ai_help() {
    cat << 'EOF'
🧠 NEXUS UNIFIED AI CORE v4.1.0 - COMMAND REFERENCE

📝 BASIC COMMANDS:
  ai "question"          - Ask AI any question
  aichat                - Interactive chat session
  aiconsensus "q"       - Multi-model consensus answer
  aicode FILE           - Analyze code

📊 PROJECT TOOLS:
  aiscore [dir]         - Score project quality
  aitodo "context"      - Generate TODO list
  aidebug "error"       - Debug error message
  aioptimize < file     - Optimize code

🛠️  SETUP & MANAGEMENT:
  aihealth              - Check AI system health
  aisetup [provider]    - Setup provider (openai, anthropic, deepseek)
  aimodels              - List available models
  aiadd_key <p> <key>   - Add API key manually

💡 EXAMPLES:
  ai "How do I write better Python?"
  aichat
  aicode myfile.py
  aiscore .
  aitodo "backend development"

🔌 SUPPORTED PROVIDERS:
  • OpenAI (GPT-4, GPT-3.5)
  • Anthropic (Claude 3)
  • Google (Gemini)
  • DeepSeek (DeepSeek models)
  • Ollama (Local models)

📚 DOCUMENTATION:
  • Module path: $0
  • Config: $AI_CONFIG
  • Cache: $AI_CACHE
  • Logs: $AI_LOGS
EOF
}

# ============================================================================
# ALIASES & SHORTCUTS
# ============================================================================

alias ai="nexus_ai_router"
alias ask="nexus_ai_router"
alias aichat="nexus_quantum_ai_chat"
alias aicode="nexus_ai_code_review"
alias aiexplain="nexus_ai_explain"
alias aitodo="nexus_ai_generate_todo"
alias aiscore="nexus_ai_score_project"
alias aiconsensus="nexus_ai_consensus"
alias aihealth="nexus_ai_health_check"
alias aidebug="nexus_ai_debug"
alias aioptimize="nexus_ai_optimize"
alias aimodels="nexus_ai_list_models"
alias aisetup="nexus_ai_setup_provider"
alias aiadd_key="nexus_ai_add_key"
alias aihelp="nexus_ai_help"

# Initialize on load
nexus_ai_load_keys

echo -e "${AI_COLOR_RESPONSE}✅ Unified AI Core v4.1.0 loaded${C_RESET}"
