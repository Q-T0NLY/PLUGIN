#!/bin/zsh
# Hyper Registry CLI - Zsh shell integration
# Provides shell commands to interact with Hyper Registry backend

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

REGISTRY_API="${REGISTRY_API:-http://localhost:8000}"
REGISTRY_PYTHON="${REGISTRY_PYTHON:-python}"
SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

registry_log() {
    echo -e "${BLUE}[Registry]${NC} $1"
}

registry_success() {
    echo -e "${GREEN}✓${NC} $1"
}

registry_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

registry_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# ============================================================================
# API FUNCTIONS
# ============================================================================

registry_health() {
    """Check registry API health"""
    registry_log "Checking API health..."
    
    local response=$(curl -s "$REGISTRY_API/health")
    
    if echo "$response" | grep -q "healthy"; then
        registry_success "API is healthy"
        echo "$response" | jq '.'
    else
        registry_error "API health check failed"
        return 1
    fi
}

registry_status() {
    """Get system status"""
    registry_log "Getting system status..."
    
    curl -s "$REGISTRY_API/status" | jq '.'
}

registry_stats() {
    """Get registry statistics"""
    registry_log "Getting registry statistics..."
    
    curl -s "$REGISTRY_API/api/v1/analytics/registry-stats" | jq '.'
}

registry_metrics() {
    """Get system metrics"""
    registry_log "Getting system metrics..."
    
    curl -s "$REGISTRY_API/api/v1/analytics/metrics" | jq '.'
}

# ============================================================================
# REGISTRY CRUD FUNCTIONS
# ============================================================================

registry_register() {
    """Register a new entry
    Usage: registry_register <category> <title> [description] [tags...]
    """
    local category="$1"
    local title="$2"
    local description="${3:-}"
    shift 3
    local tags="$@"

    if [ -z "$category" ] || [ -z "$title" ]; then
        registry_error "Usage: registry_register <category> <title> [description] [tags...]"
        return 1
    fi

    registry_log "Registering entry..."

    local json_data=$(cat <<EOF
{
    "category": "$category",
    "title": "$title",
    "description": "$description",
    "tags": $(echo "$tags" | jq -R 'split(" ")')
}
EOF
)

    curl -s -X POST "$REGISTRY_API/api/v1/registry/entries" \
        -H "Content-Type: application/json" \
        -d "$json_data" | jq '.'
}

registry_get() {
    """Get entry details
    Usage: registry_get <entry_id>
    """
    local entry_id="$1"

    if [ -z "$entry_id" ]; then
        registry_error "Usage: registry_get <entry_id>"
        return 1
    fi

    registry_log "Getting entry: $entry_id"

    curl -s "$REGISTRY_API/api/v1/registry/entries/$entry_id" | jq '.'
}

registry_delete() {
    """Delete an entry
    Usage: registry_delete <entry_id>
    """
    local entry_id="$1"

    if [ -z "$entry_id" ]; then
        registry_error "Usage: registry_delete <entry_id>"
        return 1
    fi

    registry_log "Deleting entry: $entry_id"

    curl -s -X DELETE "$REGISTRY_API/api/v1/registry/entries/$entry_id" | jq '.'
}

# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

registry_search() {
    """Search registry
    Usage: registry_search <query> [limit] [type]
    """
    local query="$1"
    local limit="${2:-10}"
    local type="${3:-hybrid}"

    if [ -z "$query" ]; then
        registry_error "Usage: registry_search <query> [limit] [type]"
        return 1
    fi

    registry_log "Searching for: $query (type: $type, limit: $limit)"

    local json_data=$(cat <<EOF
{
    "query": "$query",
    "search_type": "$type",
    "filters": {},
    "limit": $limit
}
EOF
)

    curl -s -X POST "$REGISTRY_API/api/v1/search" \
        -H "Content-Type: application/json" \
        -d "$json_data" | jq '.'
}

registry_autocomplete() {
    """Get autocomplete suggestions
    Usage: registry_autocomplete <query>
    """
    local query="$1"

    if [ -z "$query" ]; then
        registry_error "Usage: registry_autocomplete <query>"
        return 1
    fi

    registry_log "Getting autocomplete for: $query"

    curl -s "$REGISTRY_API/api/v1/search/autocomplete?q=$query" | jq '.'
}

registry_trending() {
    """Get trending searches"""
    registry_log "Getting trending searches..."

    curl -s "$REGISTRY_API/api/v1/search/trending" | jq '.'
}

# ============================================================================
# RELATIONSHIP FUNCTIONS
# ============================================================================

registry_link() {
    """Create relationship between entries
    Usage: registry_link <source_id> <target_id> <type>
    """
    local source_id="$1"
    local target_id="$2"
    local rel_type="$3"

    if [ -z "$source_id" ] || [ -z "$target_id" ] || [ -z "$rel_type" ]; then
        registry_error "Usage: registry_link <source_id> <target_id> <type>"
        return 1
    fi

    registry_log "Creating relationship: $source_id -> $target_id ($rel_type)"

    local json_data=$(cat <<EOF
{
    "source_id": "$source_id",
    "target_id": "$target_id",
    "relationship_type": "$rel_type",
    "metadata": {}
}
EOF
)

    curl -s -X POST "$REGISTRY_API/api/v1/relationships" \
        -H "Content-Type: application/json" \
        -d "$json_data" | jq '.'
}

registry_relationships() {
    """Get relationships for entry
    Usage: registry_relationships <entry_id> [type]
    """
    local entry_id="$1"
    local rel_type="${2:-}"

    if [ -z "$entry_id" ]; then
        registry_error "Usage: registry_relationships <entry_id> [type]"
        return 1
    fi

    registry_log "Getting relationships for: $entry_id"

    local url="$REGISTRY_API/api/v1/relationships/$entry_id"
    [ -n "$rel_type" ] && url="$url?rel_type=$rel_type"

    curl -s "$url" | jq '.'
}

# ============================================================================
# AGENT CONVENIENCE FUNCTIONS
# ============================================================================

registry_agent() {
    """Register an agent
    Usage: registry_agent <name> <description> [tags...]
    """
    local name="$1"
    local description="$2"
    shift 2
    local tags="$@"

    registry_log "Registering agent: $name"

    registry_register "agent" "$name" "$description" "$tags"
}

registry_service() {
    """Register a service
    Usage: registry_service <name> <description> [tags...]
    """
    local name="$1"
    local description="$2"
    shift 2
    local tags="$@"

    registry_log "Registering service: $name"

    registry_register "service" "$name" "$description" "$tags"
}

registry_workflow() {
    """Register a workflow
    Usage: registry_workflow <name> <description> [tags...]
    """
    local name="$1"
    local description="$2"
    shift 2
    local tags="$@"

    registry_log "Registering workflow: $name"

    registry_register "workflow" "$name" "$description" "$tags"
}

registry_model() {
    """Register a model
    Usage: registry_model <name> <description> [tags...]
    """
    local name="$1"
    local description="$2"
    shift 2
    local tags="$@"

    registry_log "Registering model: $name"

    registry_register "model" "$name" "$description" "$tags"
}

# ============================================================================
# HELP FUNCTION
# ============================================================================

registry_help() {
    """Display help information"""
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════════╗
║         📚 HYPER REGISTRY CLI - Command Reference                 ║
╚════════════════════════════════════════════════════════════════════╝

SYSTEM COMMANDS:
  registry_health              Check API health status
  registry_status              Get system status
  registry_stats               Get registry statistics
  registry_metrics             Get system metrics
  registry_help                Show this help

CRUD OPERATIONS:
  registry_register <cat> <title> [desc] [tags...]
                               Register new entry
  registry_get <entry_id>      Get entry details
  registry_delete <entry_id>   Delete entry

SEARCH & DISCOVERY:
  registry_search <query> [limit] [type]
                               Search entries
  registry_autocomplete <query>
                               Get autocomplete suggestions
  registry_trending            Get trending searches

RELATIONSHIPS:
  registry_link <src> <dst> <type>
                               Create relationship
  registry_relationships <id>  Get entry relationships

CONVENIENCE FUNCTIONS:
  registry_agent <name> <desc> [tags...]
                               Register agent
  registry_service <name> <desc> [tags...]
                               Register service
  registry_workflow <name> <desc> [tags...]
                               Register workflow
  registry_model <name> <desc> [tags...]
                               Register model

EXAMPLES:
  # Check health
  registry_health

  # Register a service
  registry_service "DataProcessor" "Processes and transforms data" production critical

  # Search for services
  registry_search "data" 5 text

  # Create relationship
  registry_link "agent_001" "service_001" "controls"

  # Get relationships
  registry_relationships "agent_001"

EOF
}

# ============================================================================
# INITIALIZATION
# ============================================================================

# Export functions for use in shell
export -f registry_log registry_success registry_error registry_warning
export -f registry_health registry_status registry_stats registry_metrics
export -f registry_register registry_get registry_delete
export -f registry_search registry_autocomplete registry_trending
export -f registry_link registry_relationships
export -f registry_agent registry_service registry_workflow registry_model
export -f registry_help

# Check if API is reachable
if ! curl -s "$REGISTRY_API/health" > /dev/null 2>&1; then
    registry_warning "Registry API not reachable at $REGISTRY_API"
    registry_warning "Some commands may fail. Ensure the API server is running."
fi

# Display welcome message on new shell
if [ -z "$_REGISTRY_CLI_INITIALIZED" ]; then
    echo -e "${CYAN}✓ Hyper Registry CLI loaded${NC}"
    echo -e "  API: ${CYAN}$REGISTRY_API${NC}"
    echo -e "  Type: ${CYAN}registry_help${NC} for command reference"
    export _REGISTRY_CLI_INITIALIZED=1
fi

# If called with arguments, execute the function
if [ $# -gt 0 ]; then
    "$@"
fi
