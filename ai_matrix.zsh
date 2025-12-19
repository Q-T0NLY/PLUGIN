#!/usr/bin/env zsh
# ──────────────────────────────────────────────────────────────────────────────
# 🧠 HYPER-MODEL INTELLIGENCE MATRIX v8.0 - Zsh Integration Module
# Complete AI orchestration engine for Nexus Hyper-Orchestrator
# ──────────────────────────────────────────────────────────────────────────────

# ============================================================================
# 📂 INITIALIZATION & PATHS
# ============================================================================

# AI Registry & Configuration Paths
export AI_REGISTRY="${NEXUS_REGISTRY:-$HOME/.nexus/registries}/ai_models.json"
export AI_CACHE="${NEXUS_CACHE:-$HOME/.nexus/cache}/ai_interactions"
export AI_LOGS="${NEXUS_LOGS:-$HOME/.nexus/logs}/ai_matrix"
export AI_CREDENTIALS="$HOME/.nexus/credentials/ai_keys.enc"
export AI_BRIDGE_PY="/workspaces/zsh/ai_hyper_bridge.py"

# Initialize directories
mkdir -p "$AI_CACHE" "$AI_LOGS" "$HOME/.nexus/credentials"

# Color configuration
export AI_COLOR_MODEL="${C_CYAN:-\033[36m}"
export AI_COLOR_PROMPT="${C_PURP:-\033[35m}"
export AI_COLOR_RESPONSE="${C_GREEN:-\033[32m}"
export AI_COLOR_THINKING="${C_YELLOW:-\033[33m}"
export AI_COLOR_ERROR="${C_RED:-\033[31m}"
export AI_COLOR_DEBUG="${C_PINK:-\033[95m}"
export C_RESET="${C_RESET:-\033[0m}"

# ============================================================================
# 🔌 AI BRIDGE INTEGRATION
# ============================================================================

# Initialize AI Bridge connection
nexus_ai_bridge_init() {
    local bridge_script="$AI_BRIDGE_PY"
    
    if [[ ! -f "$bridge_script" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ AI Bridge not found at: $bridge_script${C_RESET}"
        return 1
    fi
    
    # Check if Python environment exists
    if [[ ! -x "/workspaces/zsh/.venv/bin/python" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ Python environment not configured${C_RESET}"
        return 1
    fi
    
    echo -e "${AI_COLOR_MODEL}🔌 Initializing AI Bridge...${C_RESET}"
    
    # Start bridge service in background
    /workspaces/zsh/.venv/bin/python "$bridge_script" &
    export AI_BRIDGE_PID=$!
    
    # Wait for bridge to initialize
    sleep 2
    
    if kill -0 $AI_BRIDGE_PID 2>/dev/null; then
        echo -e "${AI_COLOR_RESPONSE}✅ AI Bridge initialized (PID: $AI_BRIDGE_PID)${C_RESET}"
        return 0
    else
        echo -e "${AI_COLOR_ERROR}❌ AI Bridge failed to initialize${C_RESET}"
        return 1
    fi
}

# Call Python AI Bridge
nexus_ai_call_bridge() {
    local python_code="$1"
    
    if [[ -z "$python_code" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ No Python code provided${C_RESET}"
        return 1
    fi
    
    /workspaces/zsh/.venv/bin/python3 << PYTHON_EOF 2>/dev/null
import sys
sys.path.insert(0, '/workspaces/zsh')
from ai_hyper_bridge import UnifiedAIServiceBridge, AIRequest, AIProvider
import asyncio
import json

async def run():
    try:
        $python_code
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

asyncio.run(run())
PYTHON_EOF
}

# ============================================================================
# 🤖 AI INTENT DETECTION & ROUTING
# ============================================================================

# Detect user intent from prompt
nexus_ai_detect_intent() {
    local prompt="$*"
    local intent="general"
    
    # Convert to lowercase
    local lower_prompt="${(L)prompt}"
    
    # Intent detection
    case "$lower_prompt" in
        *code*|*program*|*function*|*script*|*debug*|*fix*|*error*|*bug*|*implement*)
            intent="code_generation"
            ;;
        *explain*|*why*|*how*|*reason*|*logic*|*think*|*analyze*)
            intent="reasoning_logic"
            ;;
        *write*|*create*|*story*|*poem*|*art*|*creative*|*design*)
            intent="creative_tasks"
            ;;
        *security*|*vulnerability*|*attack*|*hack*|*secure*|*exploit*)
            intent="security_analysis"
            ;;
        *math*|*calculate*|*equation*|*proof*|*statistic*|*derive*)
            intent="mathematical_proofs"
            ;;
        *image*|*picture*|*photo*|*visual*|*draw*|*diagram*)
            intent="multi_modal"
            ;;
    esac
    
    echo "$intent"
}

# Select optimal model based on intent
nexus_ai_select_model() {
    local intent="${1:-general}"
    
    # Model selection by intent
    case "$intent" in
        "code_generation")
            echo "codellama"
            ;;
        "reasoning_logic")
            echo "llama3"
            ;;
        "creative_tasks")
            echo "neural-chat"
            ;;
        "security_analysis")
            echo "llama3"
            ;;
        "mathematical_proofs")
            echo "llama3"
            ;;
        *)
            echo "llama3"
            ;;
    esac
}

# ============================================================================
# 💬 MAIN AI ROUTER
# ============================================================================

# Main AI router function
nexus_ai_router() {
    local prompt="$*"
    
    if [[ -z "$prompt" ]]; then
        echo -e "${AI_COLOR_ERROR}❌ Please provide a prompt${C_RESET}"
        return 1
    fi
    
    # Detect intent
    local intent=$(nexus_ai_detect_intent "$prompt")
    local model=$(nexus_ai_select_model "$intent")
    
    echo -e "${AI_COLOR_MODEL}🤖 [AI ROUTER]${C_RESET}"
    echo -e "${AI_COLOR_MODEL}Intent: ${AI_COLOR_RESPONSE}$intent${C_RESET} → Model: ${AI_COLOR_THINKING}$model${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    # Check for Ollama
    if ! command -v ollama &>/dev/null; then
        echo -e "${AI_COLOR_ERROR}❌ Ollama not installed. Installing...${C_RESET}"
        curl -fsSL https://ollama.ai/install.sh | sh 2>/dev/null
    fi
    
    # Ensure Ollama is running
    if ! curl -s http://localhost:11434/api/tags &>/dev/null; then
        echo -e "${AI_COLOR_THINKING}🚀 Starting Ollama server...${C_RESET}"
        ollama serve &>/dev/null &
        sleep 3
    fi
    
    # Check if model is available
    if ! ollama list 2>/dev/null | grep -q "^$model"; then
        echo -e "${AI_COLOR_THINKING}📥 Pulling model: $model${C_RESET}"
        ollama pull "$model" 2>/dev/null
    fi
    
    # Run the model
    echo -e "${AI_COLOR_THINKING}⏳ Generating response...${C_RESET}\n"
    
    local response=$(ollama run "$model" "$prompt" 2>/dev/null)
    
    echo -e "\n${AI_COLOR_RESPONSE}$response${C_RESET}"
    
    # Log interaction
    nexus_ai_log_interaction "$prompt" "$model" "$intent"
}

# ============================================================================
# 🔍 ADVANCED AI FEATURES
# ============================================================================

# Interactive chat
nexus_ai_chat() {
    echo -e "${AI_COLOR_MODEL}💬 [INTERACTIVE AI CHAT]${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    local history_file="$AI_CACHE/chat_history_$(date +%Y%m%d).json"
    local model="llama3"
    
    echo -e "${AI_COLOR_THINKING}💡 Type 'exit' to quit, 'model' to change model${C_RESET}\n"
    
    while true; do
        echo -ne "${AI_COLOR_PROMPT}You:${C_RESET} "
        read -r user_input
        
        # Check for commands
        case "$user_input" in
            exit|quit)
                echo -e "${AI_COLOR_RESPONSE}👋 Goodbye!${C_RESET}"
                break
                ;;
            model)
                echo -ne "${AI_COLOR_PROMPT}Enter model name (e.g., llama3, codellama):${C_RESET} "
                read -r model
                continue
                ;;
            clear)
                clear
                continue
                ;;
        esac
        
        # Get AI response
        echo -e "${AI_COLOR_THINKING}🤔 Thinking...${C_RESET}"
        local response=$(ollama run "$model" "$user_input" 2>/dev/null)
        echo -e "${AI_COLOR_RESPONSE}AI:${C_RESET} $response\n"
    done
}

# Multi-model consensus
nexus_ai_consensus() {
    local prompt="$*"
    
    echo -e "${AI_COLOR_MODEL}⚖️  [MULTI-MODEL CONSENSUS]${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    local models=("llama3" "codellama" "mistral")
    local responses=()
    
    # Get responses from all models in parallel
    for model in "${models[@]}"; do
        echo -e "${AI_COLOR_THINKING}🧠 $model processing...${C_RESET}"
        
        (
            local response=$(ollama run "$model" "$prompt" 2>/dev/null)
            echo "$response" > "$AI_CACHE/${model}_response.txt"
        ) &
    done
    
    # Wait for all to complete
    wait
    
    echo -e "\n${AI_COLOR_RESPONSE}✅ All models completed${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}\n"
    
    # Display results
    for model in "${models[@]}"; do
        if [[ -f "$AI_CACHE/${model}_response.txt" ]]; then
            local response=$(cat "$AI_CACHE/${model}_response.txt" | head -5)
            echo -e "${AI_COLOR_MODEL}${model}:${C_RESET}"
            echo -e "${AI_COLOR_RESPONSE}$response...${C_RESET}\n"
        fi
    done
    
    # Cleanup
    rm -f "$AI_CACHE"/*_response.txt
}

# Code analysis
nexus_ai_code_review() {
    local file="${1:-.}"
    
    echo -e "${AI_COLOR_MODEL}📁 [CODE ANALYSIS]${C_RESET}"
    
    if [[ -f "$file" ]]; then
        echo -e "${AI_COLOR_THINKING}Analyzing: $file${C_RESET}"
        
        local content=$(head -50 "$file")
        local prompt="Analyze this code for bugs, security issues, and optimization opportunities:\n\n$content"
        
        nexus_ai_router "$prompt"
    else
        echo -e "${AI_COLOR_ERROR}❌ File not found: $file${C_RESET}"
    fi
}

# Generate TODO from context
nexus_ai_generate_todo() {
    local context="${1:-project}"
    
    echo -e "${AI_COLOR_MODEL}✅ [AI TASK GENERATOR]${C_RESET}"
    
    local prompt="Generate a comprehensive TODO list for: $context. Include priorities (P0-P3), effort estimates (S/M/L), and descriptions."
    
    echo -e "${AI_COLOR_THINKING}Generating TODO list...${C_RESET}\n"
    
    nexus_ai_router "$prompt"
}

# Project analysis with scoring
nexus_ai_score_project() {
    local project_path="${1:-.}"
    
    echo -e "${AI_COLOR_MODEL}📈 [PROJECT SCORING]${C_RESET}"
    
    # Calculate metrics
    local files=$(find "$project_path" -type f | wc -l)
    local dirs=$(find "$project_path" -type d | wc -l)
    local has_readme=$([[ -f "$project_path/README.md" ]] && echo "1" || echo "0")
    local has_tests=$(find "$project_path" -name "*test*" | wc -l)
    
    # Score calculation
    local score=$((50 + (files > 0 ? 10 : 0) + (has_readme ? 20 : 0) + (has_tests > 0 ? 20 : 0)))
    
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    echo -e "${AI_COLOR_RESPONSE}Project Score: ${AI_COLOR_THINKING}$score/100${C_RESET}"
    echo -e "${AI_COLOR_RESPONSE}Files: ${AI_COLOR_THINKING}$files${C_RESET}"
    echo -e "${AI_COLOR_RESPONSE}Directories: ${AI_COLOR_THINKING}$dirs${C_RESET}"
    echo -e "${AI_COLOR_RESPONSE}Tests: ${AI_COLOR_THINKING}$has_tests${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    # Save report
    local report_file="project_score_$(date +%Y%m%d).json"
    cat > "$report_file" << EOF
{
  "project": "$project_path",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "scores": {
    "overall": $score,
    "files": $files,
    "directories": $dirs,
    "has_readme": $has_readme,
    "test_count": $has_tests
  }
}
EOF
    
    echo -e "${AI_COLOR_RESPONSE}💾 Report saved: $report_file${C_RESET}"
}

# ============================================================================
# 🛠️ UTILITY FUNCTIONS
# ============================================================================

# Log interaction
nexus_ai_log_interaction() {
    local prompt="$1"
    local model="$2"
    local intent="$3"
    
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="$timestamp | Model: $model | Intent: $intent | Prompt: ${prompt:0:100}"
    
    echo "$log_entry" >> "$AI_LOGS/interactions_$(date +%Y%m%d).log"
}

# Health check
nexus_ai_health_check() {
    echo -e "${AI_COLOR_MODEL}🤖 [AI HEALTH CHECK]${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    # Check Ollama
    if command -v ollama &>/dev/null; then
        echo -e "${AI_COLOR_RESPONSE}✅ Ollama: Installed${C_RESET}"
        
        if curl -s http://localhost:11434/api/tags &>/dev/null; then
            echo -e "${AI_COLOR_RESPONSE}✅ Ollama Server: Running${C_RESET}"
            local model_count=$(ollama list 2>/dev/null | wc -l)
            echo -e "${AI_COLOR_RESPONSE}✅ Models Available: $((model_count - 1))${C_RESET}"
        else
            echo -e "${AI_COLOR_ERROR}❌ Ollama Server: Not running${C_RESET}"
        fi
    else
        echo -e "${AI_COLOR_ERROR}❌ Ollama: Not installed${C_RESET}"
    fi
    
    # Check Python environment
    if [[ -x "/workspaces/zsh/.venv/bin/python" ]]; then
        echo -e "${AI_COLOR_RESPONSE}✅ Python Environment: Ready${C_RESET}"
    else
        echo -e "${AI_COLOR_ERROR}❌ Python Environment: Not configured${C_RESET}"
    fi
    
    # Check AI Bridge
    if [[ -f "$AI_BRIDGE_PY" ]]; then
        echo -e "${AI_COLOR_RESPONSE}✅ AI Bridge: Available${C_RESET}"
    else
        echo -e "${AI_COLOR_ERROR}❌ AI Bridge: Not found${C_RESET}"
    fi
    
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
}

# Setup AI provider
nexus_ai_setup_provider() {
    local provider="${1:-ollama}"
    
    echo -e "${AI_COLOR_MODEL}⚙️  Setting up: $provider${C_RESET}"
    
    case "$provider" in
        "ollama")
            if ! command -v ollama &>/dev/null; then
                echo -e "${AI_COLOR_THINKING}📥 Installing Ollama...${C_RESET}"
                curl -fsSL https://ollama.ai/install.sh | sh
            fi
            
            echo -e "${AI_COLOR_THINKING}📥 Pulling models...${C_RESET}"
            ollama pull llama3 2>/dev/null &
            ollama pull codellama 2>/dev/null &
            
            echo -e "${AI_COLOR_RESPONSE}✅ Ollama configured${C_RESET}"
            ;;
        "openai")
            echo -ne "${AI_COLOR_PROMPT}Enter OpenAI API Key:${C_RESET} "
            read -s api_key
            if [[ -n "$api_key" ]]; then
                export OPENAI_API_KEY="$api_key"
                echo -e "\n${AI_COLOR_RESPONSE}✅ OpenAI configured${C_RESET}"
            fi
            ;;
        "anthropic")
            echo -ne "${AI_COLOR_PROMPT}Enter Anthropic API Key:${C_RESET} "
            read -s api_key
            if [[ -n "$api_key" ]]; then
                export ANTHROPIC_API_KEY="$api_key"
                echo -e "\n${AI_COLOR_RESPONSE}✅ Anthropic configured${C_RESET}"
            fi
            ;;
        *)
            echo -e "${AI_COLOR_ERROR}Unknown provider: $provider${C_RESET}"
            ;;
    esac
}

# List available models
nexus_ai_list_models() {
    echo -e "${AI_COLOR_MODEL}🤖 [AVAILABLE MODELS]${C_RESET}"
    echo -e "${AI_COLOR_MODEL}════════════════════════════════════════════════════${C_RESET}"
    
    if command -v ollama &>/dev/null; then
        echo -e "${AI_COLOR_RESPONSE}Local Models (Ollama):${C_RESET}"
        ollama list 2>/dev/null | awk 'NR>1 {print "  " $1}'
    fi
    
    echo -e "\n${AI_COLOR_RESPONSE}API Models:${C_RESET}"
    echo -e "  gpt-4, gpt-3.5-turbo (OpenAI)"
    echo -e "  claude-3-opus, claude-3-sonnet (Anthropic)"
    echo -e "  deepseek-coder, deepseek-chat (DeepSeek)"
}

# Help
nexus_ai_help() {
    cat << 'EOF'
🧠 NEXUS AI MATRIX - COMMAND REFERENCE

📝 BASIC COMMANDS:
  ai "question"          - Ask AI any question
  aichat                - Interactive chat
  aiconsensus "q"       - Multi-model consensus
  aicode FILE           - Analyze code

📊 PROJECT TOOLS:
  aiscore [dir]         - Score project quality
  aitodo "context"      - Generate TODO list
  aiproject [dir]       - Analyze project

🛠️  SETUP & MANAGEMENT:
  aihealth              - Check AI health
  aisetup [provider]    - Setup provider (ollama, openai, anthropic)
  aimodels              - List available models

💡 EXAMPLES:
  ai "How do I fix this error?"
  aichat
  aiconsensus "Best practice for error handling?"
  aicode src/main.py
  aitodo "Build a web API"

EOF
}

# ============================================================================
# 🎯 COMMAND ALIASES
# ============================================================================

alias ai="nexus_ai_router"
alias ask="nexus_ai_router"
alias aichat="nexus_ai_chat"
alias aiconsensus="nexus_ai_consensus"
alias aicode="nexus_ai_code_review"
alias aiscore="nexus_ai_score_project"
alias aitodo="nexus_ai_generate_todo"
alias aiproject="nexus_ai_score_project"
alias aihealth="nexus_ai_health_check"
alias aisetup="nexus_ai_setup_provider"
alias aimodels="nexus_ai_list_models"
alias aihelp="nexus_ai_help"

# ============================================================================
# 🏁 INITIALIZATION
# ============================================================================

# Mark module as loaded
export NEXUS_AI_MATRIX_LOADED=true

# Print status on load
if [[ -z "$NEXUS_AI_MATRIX_QUIET" ]]; then
    echo -e "${AI_COLOR_RESPONSE}✅ Nexus AI Matrix v8.0 Loaded${C_RESET}"
    echo -e "${AI_COLOR_THINKING}💡 Type 'aihelp' for commands${C_RESET}"
fi
