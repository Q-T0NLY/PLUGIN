#!/usr/bin/env zsh
# ============================================================================
# 🧠 NEXUS AI INTELLIGENCE MATRIX v8.0 - ZSH MODULE
# ============================================================================
# Multi-provider LLM integration with intelligent routing, consensus,
# and advanced AI development tools for production zsh environments.
# ============================================================================

[[ -n "$NEXUS_AI_MATRIX_LOADED" ]] && return
export NEXUS_AI_MATRIX_LOADED=1

# Configuration
export AI_REGISTRY="${HOME}/.nexus/ai/registry.json"
export AI_CACHE="${HOME}/.nexus/ai/cache"
export AI_LOGS="${HOME}/.nexus/ai/logs"
export AI_CREDENTIALS="${HOME}/.nexus/ai/credentials"

# Create directories
mkdir -p {$AI_CACHE,$AI_LOGS,$AI_CREDENTIALS}

# Colors for AI system
export AI_MODEL_COLOR="\033[38;2;100;210;255m"     # Cyan
export AI_PROMPT_COLOR="\033[38;2;123;97;255m"     # Purple
export AI_RESPONSE_COLOR="\033[38;2;48;209;88m"    # Green
export AI_THINKING_COLOR="\033[38;2;255;214;10m"   # Yellow
export AI_ERROR_COLOR="\033[38;2;255;59;48m"       # Red
export AI_DEBUG_COLOR="\033[38;2;191;90;242m"      # Magenta
export RESET="\033[0m"

# ============================================================================
# 📊 INTENT DETECTION ENGINE
# ============================================================================

nexus_ai_detect_intent() {
    local prompt="$1"
    local lower_prompt=$(echo "$prompt" | tr '[:upper:]' '[:lower:]')
    
    local intent="general"
    local confidence=0.5
    
    # Pattern matching for intent detection
    if [[ "$lower_prompt" =~ (code|program|function|script|debug|error|fix|implement|class|method|algorithm) ]]; then
        intent="code_generation"
        confidence=0.85
    elif [[ "$lower_prompt" =~ (explain|why|how|reason|logic|think|analyze|understand) ]]; then
        intent="reasoning_logic"
        confidence=0.80
    elif [[ "$lower_prompt" =~ (write|create|story|poem|art|creative|imagine|design) ]]; then
        intent="creative_tasks"
        confidence=0.75
    elif [[ "$lower_prompt" =~ (security|vulnerability|attack|hack|secure|encrypt|threat|exploit) ]]; then
        intent="security_analysis"
        confidence=0.90
    elif [[ "$lower_prompt" =~ (math|calculate|equation|proof|theorem|statistic|formula) ]]; then
        intent="mathematical_proofs"
        confidence=0.88
    elif [[ "$lower_prompt" =~ (image|picture|photo|visual|draw|diagram|chart|graph|video) ]]; then
        intent="multi_modal"
        confidence=0.80
    fi
    
    echo "${intent}:${confidence}"
}

# ============================================================================
# 🤖 PROVIDER MANAGEMENT
# ============================================================================

nexus_ai_add_key() {
    local provider="$1"
    local key="$2"
    
    if [[ -z "$provider" ]] || [[ -z "$key" ]]; then
        echo "${AI_ERROR_COLOR}❌ Usage: nexus_ai_add_key <provider> <key>${RESET}"
        return 1
    fi
    
    # Store encrypted key
    echo "$key" | openssl enc -aes-256-cbc -salt -out "$AI_CREDENTIALS/${provider}.enc" 2>/dev/null
    
    # Update registry
    case "$provider" in
        openai)
            export OPENAI_API_KEY="$key"
            ;;
        anthropic)
            export ANTHROPIC_API_KEY="$key"
            ;;
        google)
            export GEMINI_API_KEY="$key"
            ;;
        deepseek)
            export DEEPSEEK_API_KEY="$key"
            ;;
        mistral)
            export MISTRAL_API_KEY="$key"
            ;;
    esac
    
    echo "${AI_RESPONSE_COLOR}✅ Key stored for $provider${RESET}"
}

nexus_ai_load_keys() {
    # Load stored credentials
    for key_file in "$AI_CREDENTIALS"/*.enc; do
        if [[ -f "$key_file" ]]; then
            provider=$(basename "$key_file" .enc)
            api_key=$(openssl enc -aes-256-cbc -d -in "$key_file" 2>/dev/null)
            
            case "$provider" in
                openai) export OPENAI_API_KEY="$api_key" ;;
                anthropic) export ANTHROPIC_API_KEY="$api_key" ;;
                google) export GEMINI_API_KEY="$api_key" ;;
                deepseek) export DEEPSEEK_API_KEY="$api_key" ;;
                mistral) export MISTRAL_API_KEY="$api_key" ;;
            esac
        fi
    done
}

# ============================================================================
# 🧠 INTELLIGENT MODEL SELECTION
# ============================================================================

nexus_ai_select_model() {
    local intent="$1"
    local prefer_speed="${2:-false}"
    
    case "$intent" in
        code_generation)
            if [[ "$prefer_speed" == "true" ]]; then
                echo "deepseek-v3"
            else
                echo "gpt-4o"
            fi
            ;;
        reasoning_logic)
            echo "claude-3-7-opus"
            ;;
        creative_tasks)
            echo "gpt-4o"
            ;;
        security_analysis)
            echo "claude-3-7-opus"
            ;;
        mathematical_proofs)
            echo "gpt-4o"
            ;;
        multi_modal)
            echo "gemini-3"
            ;;
        *)
            echo "gpt-4o"
            ;;
    esac
}

nexus_ai_get_provider_for_model() {
    local model="$1"
    
    case "$model" in
        gpt-*|gpt-5.1)
            echo "openai"
            ;;
        claude-*)
            echo "anthropic"
            ;;
        gemini-*)
            echo "google"
            ;;
        deepseek-*)
            echo "deepseek"
            ;;
        mistral-*)
            echo "mistral"
            ;;
        llama*|mistral|codellama|phi)
            echo "ollama"
            ;;
        *)
            echo "openai"
            ;;
    esac
}

# ============================================================================
# 💬 MAIN AI CHAT INTERFACE
# ============================================================================

nexus_ai_router() {
    local prompt="$1"
    
    if [[ -z "$prompt" ]]; then
        echo "${AI_ERROR_COLOR}❌ Usage: ai \"<your question>\"${RESET}"
        return 1
    fi
    
    # Load API keys
    nexus_ai_load_keys
    
    # Detect intent
    local intent_result=$(nexus_ai_detect_intent "$prompt")
    local intent="${intent_result%%:*}"
    local confidence="${intent_result##*:}"
    
    echo -e "${AI_MODEL_COLOR}🤖 [AI ROUTER]${RESET}"
    echo -e "${AI_MODEL_COLOR}Intent: ${AI_THINKING_COLOR}$intent${RESET} | Confidence: ${AI_RESPONSE_COLOR}${confidence}${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    
    # Select model
    local prefer_speed=false
    [[ "$intent" == "code_generation" ]] && prefer_speed=true
    
    local model=$(nexus_ai_select_model "$intent" "$prefer_speed")
    local provider=$(nexus_ai_get_provider_for_model "$model")
    
    echo -e "Model: ${AI_RESPONSE_COLOR}$model${RESET} | Provider: ${AI_RESPONSE_COLOR}$provider${RESET}"
    echo -e "${AI_THINKING_COLOR}⏳ Processing...${RESET}"
    echo ""
    
    # Call provider API
    nexus_ai_call_provider "$provider" "$model" "$prompt"
    
    # Log interaction
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] | Intent: $intent | Provider: $provider | Model: $model | Confidence: $confidence" >> "$AI_LOGS/interactions.log"
}

# ============================================================================
# 🌐 PROVIDER CALL HANDLERS
# ============================================================================

nexus_ai_call_provider() {
    local provider="$1"
    local model="$2"
    local prompt="$3"
    
    case "$provider" in
        openai)
            nexus_ai_call_openai "$model" "$prompt"
            ;;
        anthropic)
            nexus_ai_call_anthropic "$model" "$prompt"
            ;;
        google)
            nexus_ai_call_google "$model" "$prompt"
            ;;
        deepseek)
            nexus_ai_call_deepseek "$model" "$prompt"
            ;;
        mistral)
            nexus_ai_call_mistral "$model" "$prompt"
            ;;
        ollama)
            nexus_ai_call_ollama "$model" "$prompt"
            ;;
        *)
            echo "${AI_ERROR_COLOR}❌ Unknown provider: $provider${RESET}"
            return 1
            ;;
    esac
}

nexus_ai_call_openai() {
    local model="$1"
    local prompt="$2"
    
    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo "${AI_ERROR_COLOR}❌ OpenAI API key not set${RESET}"
        return 1
    fi
    
    curl -s https://api.openai.com/v1/chat/completions \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.7,
            \"max_tokens\": 2048
        }" | jq -r '.choices[0].message.content' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling OpenAI API${RESET}"
}

nexus_ai_call_anthropic() {
    local model="$1"
    local prompt="$2"
    
    if [[ -z "$ANTHROPIC_API_KEY" ]]; then
        echo "${AI_ERROR_COLOR}❌ Anthropic API key not set${RESET}"
        return 1
    fi
    
    curl -s https://api.anthropic.com/v1/messages \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"max_tokens\": 2048,
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}]
        }" | jq -r '.content[0].text' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling Anthropic API${RESET}"
}

nexus_ai_call_google() {
    local model="$1"
    local prompt="$2"
    
    if [[ -z "$GEMINI_API_KEY" ]]; then
        echo "${AI_ERROR_COLOR}❌ Google API key not set${RESET}"
        return 1
    fi
    
    curl -s "https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${GEMINI_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"contents\": [{\"parts\": [{\"text\": \"$prompt\"}]}],
            \"generationConfig\": {\"maxOutputTokens\": 2048}
        }" | jq -r '.candidates[0].content.parts[0].text' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling Google API${RESET}"
}

nexus_ai_call_deepseek() {
    local model="$1"
    local prompt="$2"
    
    if [[ -z "$DEEPSEEK_API_KEY" ]]; then
        echo "${AI_ERROR_COLOR}❌ DeepSeek API key not set${RESET}"
        return 1
    fi
    
    curl -s https://api.deepseek.com/v1/chat/completions \
        -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.7,
            \"max_tokens\": 2048
        }" | jq -r '.choices[0].message.content' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling DeepSeek API${RESET}"
}

nexus_ai_call_mistral() {
    local model="$1"
    local prompt="$2"
    
    if [[ -z "$MISTRAL_API_KEY" ]]; then
        echo "${AI_ERROR_COLOR}❌ Mistral API key not set${RESET}"
        return 1
    fi
    
    curl -s https://api.mistral.ai/v1/chat/completions \
        -H "Authorization: Bearer $MISTRAL_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
            \"temperature\": 0.7,
            \"max_tokens\": 2048
        }" | jq -r '.choices[0].message.content' 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling Mistral API${RESET}"
}

nexus_ai_call_ollama() {
    local model="$1"
    local prompt="$2"
    
    if ! command -v ollama &>/dev/null; then
        echo "${AI_ERROR_COLOR}❌ Ollama not installed${RESET}"
        return 1
    fi
    
    ollama run "$model" "$prompt" 2>/dev/null || \
        echo "${AI_ERROR_COLOR}Error calling Ollama${RESET}"
}

# ============================================================================
# ⚖️ MULTI-MODEL CONSENSUS
# ============================================================================

nexus_ai_consensus() {
    local prompt="$1"
    local models=("${@:2}")
    
    if [[ -z "$prompt" ]]; then
        echo "${AI_ERROR_COLOR}❌ Usage: ai_consensus \"<prompt>\" [model1] [model2] ...${RESET}"
        return 1
    fi
    
    # Default to top models if none specified
    if [[ ${#models[@]} -eq 0 ]]; then
        models=("gpt-4o" "claude-3-7-sonnet" "gemini-3")
    fi
    
    echo -e "${AI_MODEL_COLOR}⚖️  [MULTI-MODEL CONSENSUS]${RESET}"
    echo -e "${AI_MODEL_COLOR}Evaluating with ${#models[@]} models...${RESET}"
    echo ""
    
    # Execute models in parallel
    local -A responses
    local -A pids
    local temp_dir=$(mktemp -d)
    
    for model in "${models[@]}"; do
        nexus_ai_router "$prompt" > "$temp_dir/${model}_output.txt" &
        pids[$model]=$!
    done
    
    # Wait for all to complete
    for model in "${models[@]}"; do
        wait ${pids[$model]} 2>/dev/null
        responses[$model]=$(cat "$temp_dir/${model}_output.txt" 2>/dev/null || echo "Error")
    done
    
    # Display results
    echo -e "${AI_RESPONSE_COLOR}📊 Consensus Results:${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    
    for model in "${models[@]}"; do
        echo -e "${AI_MODEL_COLOR}[$model]:${RESET}"
        echo "${responses[$model]}"
        echo ""
    done
    
    rm -rf "$temp_dir"
}

# ============================================================================
# 🛠️ AI DEVELOPMENT TOOLS
# ============================================================================

nexus_ai_code_review() {
    local file_path="$1"
    
    if [[ ! -f "$file_path" ]]; then
        echo "${AI_ERROR_COLOR}❌ File not found: $file_path${RESET}"
        return 1
    fi
    
    local code_content=$(head -100 "$file_path")
    local prompt="Review this code for bugs, security issues, and improvements:\n\n$code_content"
    
    echo -e "${AI_THINKING_COLOR}🔍 Analyzing code...${RESET}"
    nexus_ai_router "$prompt"
}

nexus_ai_explain() {
    local topic="$1"
    
    if [[ -z "$topic" ]]; then
        echo "${AI_ERROR_COLOR}❌ Usage: ai_explain \"<topic>\"${RESET}"
        return 1
    fi
    
    local prompt="Explain this topic step-by-step with examples: $topic"
    
    echo -e "${AI_THINKING_COLOR}🤔 Explaining...${RESET}"
    nexus_ai_router "$prompt"
}

nexus_ai_generate_todo() {
    local context="$1"
    
    if [[ -z "$context" ]]; then
        context="Generate a TODO list for a typical software project"
    fi
    
    local prompt="Generate a detailed, actionable TODO list with priorities (P0-P3) and estimated effort (S/M/L/XL). Context: $context"
    
    echo -e "${AI_THINKING_COLOR}✅ Generating TODO list...${RESET}"
    nexus_ai_router "$prompt"
}

nexus_ai_score_project() {
    local project_path="${1:-.}"
    
    local prompt="Score this project (0-100) across: structure (20%), documentation (15%), testing (30%), security (20%), performance (15%). Provide recommendations. Path: $project_path"
    
    echo -e "${AI_THINKING_COLOR}📈 Scoring project...${RESET}"
    nexus_ai_router "$prompt"
}

# ============================================================================
# 📋 UTILITY FUNCTIONS
# ============================================================================

nexus_ai_list_models() {
    echo -e "${AI_MODEL_COLOR}🤖 [AVAILABLE AI MODELS]${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}OpenAI:${RESET}"
    echo "  • gpt-5.1, gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}Anthropic:${RESET}"
    echo "  • claude-3-7-opus, claude-3-7-sonnet, claude-3-7-haiku"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}Google:${RESET}"
    echo "  • gemini-3, gemini-2.0-pro, gemini-2.0-flash"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}DeepSeek:${RESET}"
    echo "  • deepseek-v3, deepseek-r1, deepseek-chat"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}Mistral:${RESET}"
    echo "  • mistral-large, mistral-medium"
    echo ""
    
    echo -e "${AI_RESPONSE_COLOR}Local (Ollama):${RESET}"
    echo "  • llama3.1, mistral, codellama, phi"
}

nexus_ai_health_check() {
    echo -e "${AI_MODEL_COLOR}🏥 [AI SYSTEM HEALTH CHECK]${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    
    # Check providers
    echo -e "${AI_RESPONSE_COLOR}Provider Status:${RESET}"
    
    [[ -n "$OPENAI_API_KEY" ]] && echo -e "  ✓ ${AI_RESPONSE_COLOR}OpenAI${RESET}: Configured" || echo -e "  ✗ ${AI_ERROR_COLOR}OpenAI${RESET}: Not configured"
    [[ -n "$ANTHROPIC_API_KEY" ]] && echo -e "  ✓ ${AI_RESPONSE_COLOR}Anthropic${RESET}: Configured" || echo -e "  ✗ ${AI_ERROR_COLOR}Anthropic${RESET}: Not configured"
    [[ -n "$GEMINI_API_KEY" ]] && echo -e "  ✓ ${AI_RESPONSE_COLOR}Google${RESET}: Configured" || echo -e "  ✗ ${AI_ERROR_COLOR}Google${RESET}: Not configured"
    [[ -n "$DEEPSEEK_API_KEY" ]] && echo -e "  ✓ ${AI_RESPONSE_COLOR}DeepSeek${RESET}: Configured" || echo -e "  ✗ ${AI_ERROR_COLOR}DeepSeek${RESET}: Not configured"
    [[ -n "$MISTRAL_API_KEY" ]] && echo -e "  ✓ ${AI_RESPONSE_COLOR}Mistral${RESET}: Configured" || echo -e "  ✗ ${AI_ERROR_COLOR}Mistral${RESET}: Not configured"
    command -v ollama &>/dev/null && echo -e "  ✓ ${AI_RESPONSE_COLOR}Ollama${RESET}: Installed" || echo -e "  ✗ ${AI_ERROR_COLOR}Ollama${RESET}: Not installed"
    
    echo ""
    echo -e "${AI_RESPONSE_COLOR}Directories:${RESET}"
    echo -e "  Cache: $AI_CACHE ($(du -sh "$AI_CACHE" 2>/dev/null | cut -f1 || echo '0B'))"
    echo -e "  Logs: $AI_LOGS"
    echo -e "  Interactions: $(wc -l < "$AI_LOGS/interactions.log" 2>/dev/null || echo '0')"
}

nexus_ai_help() {
    echo -e "${AI_MODEL_COLOR}🧠 [NEXUS AI MATRIX HELP]${RESET}"
    echo -e "${AI_MODEL_COLOR}════════════════════════════════════════════════════${RESET}"
    echo ""
    echo -e "${AI_RESPONSE_COLOR}Commands:${RESET}"
    echo "  ai \"<prompt>\"              - Ask AI any question"
    echo "  ai_consensus \"<prompt>\"    - Multi-model consensus"
    echo "  ai_code_review <file>       - Review code quality"
    echo "  ai_explain \"<topic>\"       - Step-by-step explanation"
    echo "  ai_generate_todo \"<ctx>\"   - Generate TODO list"
    echo "  ai_score_project [path]     - Score project quality"
    echo "  ai_health_check              - Check AI system health"
    echo "  ai_list_models              - Show available models"
    echo ""
    echo -e "${AI_RESPONSE_COLOR}Setup:${RESET}"
    echo "  ai_add_key <provider> <key> - Add API key for provider"
    echo ""
    echo -e "${AI_RESPONSE_COLOR}Supported Providers:${RESET}"
    echo "  • openai (GPT-4, GPT-3.5)"
    echo "  • anthropic (Claude 3)"
    echo "  • google (Gemini)"
    echo "  • deepseek (DeepSeek)"
    echo "  • mistral (Mistral)"
    echo "  • ollama (Local models)"
}

# ============================================================================
# ALIASES
# ============================================================================

alias ai="nexus_ai_router"
alias ask="nexus_ai_router"
alias ai_chat="nexus_ai_router"
alias ai_code="nexus_ai_code_review"
alias ai_explain="nexus_ai_explain"
alias ai_todo="nexus_ai_generate_todo"
alias ai_score="nexus_ai_score_project"
alias ai_consensus="nexus_ai_consensus"
alias ai_health="nexus_ai_health_check"
alias ai_models="nexus_ai_list_models"
alias ai_help="nexus_ai_help"

# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize on load
nexus_ai_load_keys

echo -e "${AI_RESPONSE_COLOR}✅ AI Intelligence Matrix v8.0 loaded${RESET}"
echo -e "${AI_THINKING_COLOR}💡 Type 'ai_help' for command help${RESET}"
