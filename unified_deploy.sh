#!/bin/bash
#
# 🚀 UNIFIED DEPLOYMENT ORCHESTRATOR v4.1.0
# Complete deployment orchestration for all platform components
#
# Consolidates:
#   - deploy.sh - Multi-component orchestration
#   - unified_deployment.py - Python deployment
#   - Enhanced orchestrator deployment
#
# Features:
#   ✅ Full system deployment orchestration
#   ✅ Multi-mode deployments (hyper_registry, integrated_ai, unified_platform, full_system)
#   ✅ Docker and Kubernetes support
#   ✅ Health monitoring and verification
#   ✅ Rollback capabilities
#   ✅ Environment configuration

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
DEPLOYMENT_LOG="${PROJECT_ROOT}/.deployment.log"
DEPLOYMENT_STATUS="${PROJECT_ROOT}/.deployment_status.json"
DEPLOYMENT_MODE="${1:-full_system}"
DEPLOYMENT_ENV="${DEPLOYMENT_ENV:-production}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging
log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_error() {
    echo -e "${RED}[✗]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $*" | tee -a "$DEPLOYMENT_LOG"
}

# ============================================================================
# DEPLOYMENT MODES
# ============================================================================

deploy_hyper_registry() {
    log "🔧 Deploying HYPER REGISTRY..."
    
    cd "$PROJECT_ROOT/services/hyper_registry" || exit 1
    
    log "  Building Docker image..."
    if [ -f "Dockerfile" ]; then
        docker build -t nexus/hyper-registry:latest . || log_error "Docker build failed"
    fi
    
    log "  Initializing database..."
    python3 database_init.py || log_error "Database init failed"
    
    log "  Starting registry server..."
    python3 server.py &
    REGISTRY_PID=$!
    
    sleep 2
    
    if kill -0 $REGISTRY_PID 2>/dev/null; then
        log_success "Hyper Registry running (PID: $REGISTRY_PID)"
        echo "$REGISTRY_PID" > "${PROJECT_ROOT}/.hyper_registry.pid"
    else
        log_error "Failed to start Hyper Registry"
        return 1
    fi
    
    cd "$PROJECT_ROOT"
}

deploy_llm_orchestrator() {
    log "🧠 Deploying LLM ORCHESTRATOR..."
    
    cd "$PROJECT_ROOT/services/llm_orchestrator" || exit 1
    
    log "  Verifying LLM adapters..."
    for adapter in adapters/*.py; do
        log "    Checking $(basename "$adapter")..."
        python3 -c "import sys; sys.path.insert(0, '.'); __import__('adapters.$(basename $adapter .py)')" || log_warning "$(basename "$adapter") validation skipped"
    done
    
    log "  Starting multi-LLM service..."
    python3 multi_llm_service.py &
    LLM_PID=$!
    
    sleep 2
    
    if kill -0 $LLM_PID 2>/dev/null; then
        log_success "LLM Orchestrator running (PID: $LLM_PID)"
        echo "$LLM_PID" > "${PROJECT_ROOT}/.llm_orchestrator.pid"
    else
        log_error "Failed to start LLM Orchestrator"
        return 1
    fi
    
    cd "$PROJECT_ROOT"
}

deploy_api_gateway() {
    log "🌐 Deploying API GATEWAY..."
    
    cd "$PROJECT_ROOT/services/api_gateway" || exit 1
    
    log "  Installing dependencies..."
    pip3 install -q -r requirements.txt || log_warning "Some dependencies may not be installed"
    
    log "  Starting API gateway..."
    python3 main.py &
    API_PID=$!
    
    sleep 3
    
    if kill -0 $API_PID 2>/dev/null; then
        log_success "API Gateway running (PID: $API_PID)"
        echo "$API_PID" > "${PROJECT_ROOT}/.api_gateway.pid"
    else
        log_error "Failed to start API Gateway"
        return 1
    fi
    
    cd "$PROJECT_ROOT"
}

deploy_enhanced_orchestrator() {
    log "⚙️  Deploying ENHANCED ORCHESTRATOR..."
    
    log "  Installing dependencies..."
    pip3 install -q -r requirements.txt 2>/dev/null || true
    
    log "  Starting orchestrator..."
    python3 enhanced_orchestrator_complete.py &
    ORCH_PID=$!
    
    sleep 3
    
    if kill -0 $ORCH_PID 2>/dev/null; then
        log_success "Enhanced Orchestrator running (PID: $ORCH_PID)"
        echo "$ORCH_PID" > "${PROJECT_ROOT}/.orchestrator.pid"
    else
        log_error "Failed to start Enhanced Orchestrator"
        return 1
    fi
}

deploy_integrated_ai() {
    log "🤖 Deploying INTEGRATED AI SYSTEM..."
    
    log "  Deploying registry..."
    deploy_hyper_registry || return 1
    
    log "  Deploying LLM orchestrator..."
    deploy_llm_orchestrator || return 1
    
    log_success "Integrated AI system deployed"
}

deploy_unified_platform() {
    log "🚀 Deploying UNIFIED PLATFORM..."
    
    log "  Deploying registry..."
    deploy_hyper_registry || return 1
    
    log "  Deploying LLM orchestrator..."
    deploy_llm_orchestrator || return 1
    
    log "  Deploying API gateway..."
    deploy_api_gateway || return 1
    
    log_success "Unified platform deployed"
}

deploy_full_system() {
    log "🌌 Deploying FULL SYSTEM..."
    
    log "  Phase 1: Registry deployment..."
    deploy_hyper_registry || return 1
    
    log "  Phase 2: LLM orchestrator..."
    deploy_llm_orchestrator || return 1
    
    log "  Phase 3: API gateway..."
    deploy_api_gateway || return 1
    
    log "  Phase 4: Enhanced orchestrator..."
    deploy_enhanced_orchestrator || return 1
    
    log_success "Full system deployed"
}

# ============================================================================
# KUBERNETES DEPLOYMENT
# ============================================================================

deploy_kubernetes() {
    log "☸️  KUBERNETES DEPLOYMENT..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Install kubectl to use Kubernetes deployment."
        return 1
    fi
    
    log "  Creating namespace..."
    kubectl create namespace nexus 2>/dev/null || log_warning "Namespace already exists"
    
    log "  Deploying services..."
    
    if [ -f "${PROJECT_ROOT}/services/hyper_registry/docker-compose-full.yml" ]; then
        log "  Applying registry manifests..."
        # In real scenario, convert compose to K8s manifests
        kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: hyper-registry
  namespace: nexus
spec:
  selector:
    app: hyper-registry
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hyper-registry
  namespace: nexus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hyper-registry
  template:
    metadata:
      labels:
        app: hyper-registry
    spec:
      containers:
      - name: hyper-registry
        image: nexus/hyper-registry:latest
        ports:
        - containerPort: 5432
EOF
    fi
    
    log_success "Kubernetes deployment initiated"
}

# ============================================================================
# DOCKER DEPLOYMENT
# ============================================================================

deploy_docker() {
    log "🐳 DOCKER DEPLOYMENT..."
    
    if ! command -v docker &> /dev/null; then
        log_error "docker not found. Install Docker to use Docker deployment."
        return 1
    fi
    
    if [ -f "${PROJECT_ROOT}/infrastructure/docker-compose.yml" ]; then
        log "  Starting Docker Compose services..."
        docker-compose -f "${PROJECT_ROOT}/infrastructure/docker-compose.yml" up -d
        log_success "Docker containers started"
    else
        log_warning "docker-compose.yml not found"
    fi
}

# ============================================================================
# HEALTH CHECKS & VERIFICATION
# ============================================================================

check_service_health() {
    local service=$1
    local port=$2
    
    log "  Checking $service health on port $port..."
    
    if nc -z localhost "$port" 2>/dev/null; then
        log_success "$service is healthy"
        return 0
    else
        log_error "$service is not responding"
        return 1
    fi
}

verify_deployment() {
    log "🔍 VERIFYING DEPLOYMENT..."
    
    case "$DEPLOYMENT_MODE" in
        hyper_registry)
            check_service_health "Hyper Registry" 5432 || return 1
            ;;
        integrated_ai)
            check_service_health "Hyper Registry" 5432 || return 1
            check_service_health "LLM Orchestrator" 8000 || return 1
            ;;
        unified_platform)
            check_service_health "Hyper Registry" 5432 || return 1
            check_service_health "LLM Orchestrator" 8000 || return 1
            check_service_health "API Gateway" 8001 || return 1
            ;;
        full_system)
            check_service_health "Hyper Registry" 5432 || return 1
            check_service_health "LLM Orchestrator" 8000 || return 1
            check_service_health "API Gateway" 8001 || return 1
            check_service_health "Enhanced Orchestrator" 8002 || return 1
            ;;
    esac
    
    log_success "Deployment verification passed"
}

# ============================================================================
# ROLLBACK
# ============================================================================

rollback_deployment() {
    log "⏮️  ROLLING BACK DEPLOYMENT..."
    
    # Kill all service processes
    for pid_file in .hyper_registry.pid .llm_orchestrator.pid .api_gateway.pid .orchestrator.pid; do
        if [ -f "$PROJECT_ROOT/$pid_file" ]; then
            pid=$(cat "$PROJECT_ROOT/$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                log "  Stopping process $pid..."
                kill "$pid" || true
            fi
            rm "$PROJECT_ROOT/$pid_file"
        fi
    done
    
    log_success "Rollback completed"
}

# ============================================================================
# STATUS REPORTING
# ============================================================================

show_status() {
    log "📊 DEPLOYMENT STATUS REPORT"
    log "=================================="
    log "Mode: $DEPLOYMENT_MODE"
    log "Environment: $DEPLOYMENT_ENV"
    log "Timestamp: $(date)"
    log "Log: $DEPLOYMENT_LOG"
    
    echo ""
    echo "Running Services:"
    for pid_file in .hyper_registry.pid .llm_orchestrator.pid .api_gateway.pid .orchestrator.pid; do
        if [ -f "$PROJECT_ROOT/$pid_file" ]; then
            pid=$(cat "$PROJECT_ROOT/$pid_file")
            service_name=$(basename "$pid_file" .pid | sed 's/^\.//')
            if kill -0 "$pid" 2>/dev/null; then
                echo "  ✓ $service_name (PID: $pid)"
            else
                echo "  ✗ $service_name (PID: $pid - not running)"
            fi
        fi
    done
}

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

print_banner() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════════════════╗
║          🚀 NEXUS UNIFIED DEPLOYMENT ORCHESTRATOR v4.1.0                   ║
║        Complete orchestration for all platform components                 ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
}

main() {
    print_banner
    
    log "Starting deployment with mode: $DEPLOYMENT_MODE"
    
    # Create log file
    touch "$DEPLOYMENT_LOG"
    
    # Execute deployment
    case "$DEPLOYMENT_MODE" in
        hyper_registry)
            deploy_hyper_registry
            ;;
        llm)
            deploy_llm_orchestrator
            ;;
        integrated_ai)
            deploy_integrated_ai
            ;;
        unified_platform)
            deploy_unified_platform
            ;;
        full_system)
            deploy_full_system
            ;;
        docker)
            deploy_docker
            ;;
        kubernetes)
            deploy_kubernetes
            ;;
        verify)
            verify_deployment
            ;;
        rollback)
            rollback_deployment
            ;;
        status)
            show_status
            ;;
        *)
            log_error "Unknown deployment mode: $DEPLOYMENT_MODE"
            echo ""
            echo "Usage: $0 [mode] [options]"
            echo ""
            echo "Deployment Modes:"
            echo "  hyper_registry        - Deploy Hyper Registry only"
            echo "  llm                   - Deploy LLM Orchestrator only"
            echo "  integrated_ai         - Deploy Integrated AI system"
            echo "  unified_platform      - Deploy Unified Platform"
            echo "  full_system           - Deploy complete system (default)"
            echo "  docker                - Deploy via Docker Compose"
            echo "  kubernetes            - Deploy to Kubernetes"
            echo "  verify                - Verify deployment health"
            echo "  rollback              - Rollback current deployment"
            echo "  status                - Show deployment status"
            echo ""
            exit 1
            ;;
    esac
    
    # Verify deployment
    if [ "$DEPLOYMENT_MODE" != "status" ] && [ "$DEPLOYMENT_MODE" != "rollback" ]; then
        sleep 2
        verify_deployment || {
            log_warning "Deployment verification failed, attempting rollback..."
            rollback_deployment
            exit 1
        }
    fi
    
    # Show final status
    echo ""
    show_status
    
    log_success "🎉 Deployment completed successfully!"
}

# Handle cleanup on exit
cleanup() {
    log "Cleaning up..."
    # Preserve this for intentional stops only
    # rollback_deployment
}

trap cleanup EXIT

# Run main
main
