#!/usr/bin/env bash
# ============================================================================
# 🌌 NEXUS MASTER CLI LAUNCHER v1.0.0
# ============================================================================
# Unified entry point for NEXUS AI Studio with all CLI tools,
# orchestrator, visualization, and chat interfaces.
# ============================================================================

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

NEXUS_HOME="${NEXUS_HOME:-$HOME/.nexus}"
NEXUS_CLI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEXUS_LOGO_COLOR="\033[1;36m"  # Bold cyan
NEXUS_RESET="\033[0m"

# Create directories
mkdir -p "$NEXUS_HOME"/{logs,cache,config}

# ============================================================================
# 🎨 Display Functions
# ============================================================================

print_logo() {
    cat << 'EOF'
    ███╗   ██╗███████╗██╗   ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝██║   ██║██║   ██║██╔════╝
    ██╔██╗ ██║█████╗  ██║   ██║██║   ██║███████╗
    ██║╚██╗██║██╔══╝  ██║   ██║██║   ██║╚════██║
    ██║ ╚████║███████╗╚██████╔╝╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝
EOF
}

print_header() {
    echo -e "${NEXUS_LOGO_COLOR}"
    print_logo
    echo -e "  NEXUS v1.0.0 - Advanced AI Orchestration Platform${NEXUS_RESET}"
    echo ""
}

show_menu() {
    echo "Select a tool:"
    echo ""
    echo "  🤖 INTERACTIVE INTERFACES"
    echo "    1) Interactive CLI        - Create & execute DAG workflows"
    echo "    2) TUI Dashboard          - Real-time workflow monitoring"
    echo "    3) AI Chat (Multi-LLM)    - Interactive chat with 4+ providers"
    echo "    10) AI Model Manager      - Manage models & ensemble configurations"
    echo ""
    echo "  ⚙️  SYSTEM UTILITIES"
    echo "    4) Orchestrator Health    - Check system status"
    echo "    5) List Workflows         - View all created workflows"
    echo "    6) View History           - Show chat/execution history"
    echo ""
    echo "  🔧 ADVANCED OPERATIONS"
    echo "    7) Python Shell           - IPython with orchestrator pre-loaded"
    echo "    8) API Server             - Start FastAPI backend"
    echo "    9) Full Stack Demo        - Run complete system demo"
    echo ""
    echo "  ℹ️  INFORMATION"
    echo "    h) Show Help              - Display full help"
    echo "    v) Show Version           - Display version info"
    echo "    q) Quit                   - Exit NEXUS"
    echo ""
}

show_help() {
    print_header
    echo "NEXUS - Advanced AI & DAG Orchestration Platform"
    echo ""
    echo "DESCRIPTION:"
    echo "  NEXUS is a comprehensive AI orchestration platform featuring:"
    echo "    • Live DAG workflow creation & execution with real-time visualization"
    echo "    • Multi-provider LLM integration (OpenAI, Claude, DeepSeek, Ollama)"
    echo "    • Interactive dashboards with metrics & monitoring"
    echo "    • Advanced CLI with rich terminal UI"
    echo "    • Full REST API with WebSocket streaming"
    echo ""
    echo "QUICK START:"
    echo "  nexus-cli              Launch interactive menu"
    echo "  nexus create           Create new workflow"
    echo "  nexus execute <id>     Execute workflow"
    echo "  nexus chat             Start AI chat interface"
    echo "  nexus dashboard        Launch TUI dashboard"
    echo ""
    echo "ENVIRONMENT VARIABLES:"
    echo "  NEXUS_HOME             Base directory ($NEXUS_HOME)"
    echo "  REDIS_URL              Redis connection (default: redis://localhost:6379)"
    echo "  OPENAI_API_KEY         OpenAI API key for LLM"
    echo ""
    echo "LEARN MORE:"
    echo "  Visit: https://github.com/d0nedeal/nexus"
    echo "  Docs: $NEXUS_HOME/docs"
    echo ""
}

show_version() {
    echo "NEXUS v1.0.0"
    echo "Python CLI Framework: typer + rich"
    echo "Backend: FastAPI + Redis + NetworkX"
    echo "TUI: Textual"
    echo "Built: 2024-12-09"
}

# ============================================================================
# 🚀 Tool Launchers
# ============================================================================

launch_cli() {
    echo "🚀 Launching NEXUS Interactive CLI..."
    python3 "$NEXUS_CLI_DIR/nexus_cli.py"
}

launch_dashboard() {
    echo "📊 Launching NEXUS TUI Dashboard..."
    python3 "$NEXUS_CLI_DIR/nexus_dashboard.py"
}

launch_chat() {
    echo "💬 Launching NEXUS AI Chat Interface..."
    python3 "$NEXUS_CLI_DIR/nexus_ai_chat.py" chat
}

launch_health() {
    echo "🏥 Checking system health..."
    python3 "$NEXUS_CLI_DIR/nexus_cli.py" health
}

launch_list() {
    echo "📋 Listing workflows..."
    python3 "$NEXUS_CLI_DIR/nexus_cli.py" list
}

launch_history() {
    echo "📜 Viewing history..."
    python3 "$NEXUS_CLI_DIR/nexus_ai_chat.py" history
}

launch_ipython() {
    echo "🐍 Starting IPython with NEXUS preloaded..."
    python3 -c "
import sys
sys.path.insert(0, '$(dirname "$NEXUS_CLI_DIR")/services')
from dag_engine.core import LiveDAGOrchestrator, DAGNode, DAGEdge, NodeType
import asyncio

print('NEXUS IPython Environment Loaded')
print('Available: LiveDAGOrchestrator, DAGNode, DAGEdge, NodeType')
print('Async mode enabled')

try:
    import IPython
    IPython.embed()
except ImportError:
    import code
    code.interact(local=locals())
"
}

launch_api() {
    echo "🌐 Starting NEXUS API Server..."
    python3 -m uvicorn services.api_gateway.main:app --host 0.0.0.0 --port 8000 --reload
}

launch_demo() {
    echo "🎬 Running Full Stack Demo..."
    echo ""
    echo "This demo will:"
    echo "  1. Create a sample DAG workflow"
    echo "  2. Execute the workflow with visualization"
    echo "  3. Display real-time metrics"
    echo ""
    
    python3 << 'PYTHON_DEMO'
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'services'))

from dag_engine.core import (
    LiveDAGOrchestrator,
    DAGNode,
    DAGEdge,
    NodeType,
    ExecutionRequest,
)

async def demo():
    print("⏳ Initializing orchestrator...")
    orch = LiveDAGOrchestrator()
    await orch.init()
    
    print("✅ Creating sample workflow...")
    wf = orch.create_workflow("Demo Pipeline")
    
    # Create nodes
    nodes = [
        DAGNode(id="start", type=NodeType.START, name="Start", x=0, y=0, z=0),
        DAGNode(id="process", type=NodeType.MICROSERVICE, name="Process Data", x=2, y=0, z=0),
        DAGNode(id="analyze", type=NodeType.RAG, name="Analyze", x=4, y=0, z=0),
        DAGNode(id="end", type=NodeType.END, name="End", x=6, y=0, z=0),
    ]
    
    for node in nodes:
        wf.add_node(node)
    
    # Create edges
    edges = [
        DAGEdge(source="start", target="process"),
        DAGEdge(source="process", target="analyze"),
        DAGEdge(source="analyze", target="end"),
    ]
    
    for edge in edges:
        wf.add_edge(edge)
    
    print(f"✅ Workflow created: {wf.id}")
    print(f"   Nodes: {len(wf.nodes)}")
    print(f"   Edges: {len(wf.edges)}")
    print("")
    
    print("🚀 Executing workflow...")
    req = ExecutionRequest(workflow_id=wf.id, params={"demo": True})
    exec_obj = await orch.execute_workflow(wf.id, req)
    
    print(f"⏳ Execution ID: {exec_obj.execution_id}")
    
    # Wait for completion
    while exec_obj.status.value == "running":
        exec_obj = await orch.get_execution(exec_obj.execution_id)
        print(f"   Progress: {len(exec_obj.nodes_executed)}/{len(wf.nodes)} nodes")
        await asyncio.sleep(1)
    
    print(f"✅ Execution complete: {exec_obj.status.value}")
    print(f"   Executed: {len(exec_obj.nodes_executed)}")
    print(f"   Failed: {len(exec_obj.nodes_failed)}")
    
    # Show visualization
    print("")
    print("📊 Visualization Data:")
    viz = orch.generate_visualization(wf, exec_obj)
    print(f"   Total Nodes: {viz['stats']['total_nodes']}")
    print(f"   Progress: {viz['stats']['progress']:.1f}%")
    
    await orch.shutdown()
    print("")
    print("✅ Demo complete!")

asyncio.run(demo())
PYTHON_DEMO
}

launch_ai_manager() {
    echo "🧠 Launching AI Model Manager..."
    if [[ -f "$NEXUS_CLI_DIR/ai_model_manager.py" ]]; then
        python3 "$NEXUS_CLI_DIR/ai_model_manager.py"
    else
        echo "AI Model Manager not installed. To add, create $NEXUS_CLI_DIR/ai_model_manager.py"
    fi
}

# ============================================================================
# 🎯 Main Menu Loop
# ============================================================================

main_menu() {
    while true; do
        clear
        print_header
        show_menu
        read -p "Enter choice (1-10, h, v, q): " choice
        
        case "$choice" in
            1) launch_cli ;;
            2) launch_dashboard ;;
            3) launch_chat ;;
            4) launch_health ;;
            5) launch_list ;;
            6) launch_history ;;
            7) launch_ipython ;;
            8) launch_api ;;
            9) launch_demo ;;
            10) launch_ai_manager ;;
            h|H) show_help ;;
            v|V) show_version ;;
            q|Q) echo "Goodbye!"; exit 0 ;;
            *) echo "Invalid choice. Press Enter to continue..." && read ;;
        esac
        
        if [[ "$choice" != "h" && "$choice" != "v" && "$choice" != "H" && "$choice" != "V" ]]; then
            echo ""
            read -p "Press Enter to return to menu..."
        fi
    done
}

# ============================================================================
# 🎪 Entry Point
# ============================================================================

# Check for arguments
if [[ $# -eq 0 ]]; then
    main_menu
else
    case "$1" in
        cli|interactive) launch_cli ;;
        dashboard|tui) launch_dashboard ;;
        chat|ai) launch_chat ;;
        ai-manager|ai_manager|models) launch_ai_manager ;;
        health|status) launch_health ;;
        list|workflows) launch_list ;;
        history) launch_history ;;
        python|ipython|shell) launch_ipython ;;
        api|server) launch_api ;;
        demo) launch_demo ;;
        help|--help|-h) show_help ;;
        version|--version|-v) show_version ;;
        *)
            echo "Unknown command: $1"
            echo "Use 'nexus help' for usage information"
            exit 1
            ;;
    esac
fi
