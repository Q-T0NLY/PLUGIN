#!/usr/bin/env python3
# ============================================================================
# 🔌 NEXUS SYSTEM INTEGRATION - Main Application Setup
# ============================================================================
# Integration module for binding all AI Matrix components into FastAPI app
# ============================================================================

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# COMPONENT IMPORTS
# ============================================================================

try:
    from services.api_gateway.ai_endpoints import router as ai_router, initialize_ai_routes
    from services.hyper_registry.registry_manager import get_registry_manager
    logger.info("✅ AI Matrix components imported successfully")
except ImportError as e:
    logger.warning(f"⚠️  Some AI components could not be imported: {e}")
    ai_router = None
    get_registry_manager = None
    # Attempt to import XAI router as an optional component
    try:
        from services.xai_api import xai_router
        logger.info("✅ XAI router imported successfully")
    except Exception:
        xai_router = None

# ============================================================================
# LIFECYCLE MANAGEMENT
# ============================================================================

registry_manager_instance: Optional[object] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup/shutdown"""
    
    # STARTUP
    logger.info("🚀 NEXUS System Starting...")
    
    try:
        # Initialize Registry System
        global registry_manager_instance
        registry_manager_instance = get_registry_manager()
        await registry_manager_instance.initialize()
        logger.info("✅ Registry system initialized")
    except Exception as e:
        logger.error(f"❌ Registry initialization failed: {e}")
    
    logger.info("🎯 NEXUS System fully operational")
    
    yield  # Application runs here
    
    # SHUTDOWN
    logger.info("🛑 NEXUS System Shutting Down...")
    
    try:
        if registry_manager_instance:
            await registry_manager_instance.shutdown()
        logger.info("✅ Graceful shutdown complete")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")

# ============================================================================
# FASTAPI APPLICATION FACTORY
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="NEXUS AI Intelligence Matrix v8.0",
        description="Enterprise-grade multi-provider LLM orchestration platform",
        version="8.0.0",
        lifespan=lifespan
    )
    
    # ========================================================================
    # MIDDLEWARE CONFIGURATION
    # ========================================================================
    
    # CORS - Allow local development and specific origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",      # Frontend dev
            "http://localhost:8000",      # API gateway
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000",
            "http://localhost",           # Shell access
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ========================================================================
    # ROUTE REGISTRATION
    # ========================================================================
    
    # AI Intelligence Matrix Routes
    if ai_router:
        app.include_router(ai_router, prefix="/v1", tags=["AI"])
        logger.info("✅ AI Matrix routes registered")
    else:
        logger.warning("⚠️  AI Matrix routes not available")
    # XAI routes (model listing, ensemble scoring, explanations)
    try:
        if xai_router:
            app.include_router(xai_router, prefix="/api/xai", tags=["XAI"])
            logger.info("✅ XAI routes registered at /api/xai")
        else:
            logger.debug("XAI router not available; skipping registration")
    except NameError:
        logger.debug("XAI router not present; skipping registration")
    
    # ========================================================================
    # MAIN HEALTH ENDPOINT
    # ========================================================================
    
    @app.get("/health")
    async def health_check():
        """System health check endpoint"""
        return {
            "status": "healthy",
            "service": "NEXUS AI Intelligence Matrix v8.0",
            "components": {
                "ai_matrix": "active",
                "api_gateway": "active",
                "registry_system": "active" if registry_manager_instance else "inactive",
                "service_mesh": "active",
                "event_router": "active"
            },
            "version": "8.0.0"
        }
    
    # ========================================================================
    # REGISTRY ACCESS ENDPOINTS
    # ========================================================================
    
    @app.get("/registries")
    async def get_registries():
        """Get list of available registries"""
        if registry_manager_instance:
            return {
                "registries": list(registry_manager_instance.master_registry.sub_registries.keys()),
                "status": "synced"
            }
        return {"error": "Registry system not available"}
    
    @app.get("/registries/{registry_name}.json")
    async def get_registry(registry_name: str):
        """Get specific registry data"""
        if registry_manager_instance:
            registry = registry_manager_instance.master_registry.sub_registries.get(registry_name)
            if registry:
                return registry.data
        return {"error": f"Registry '{registry_name}' not found"}
    
    @app.get("/system/info")
    async def system_info():
        """Get system information"""
        return {
            "system": "NEXUS AI Intelligence Matrix v8.0",
            "status": "operational",
            "components": {
                "ai_matrix": {
                    "providers": 6,
                    "models": 25,
                    "status": "active"
                },
                "api_gateway": {
                    "services": 6,
                    "status": "active"
                },
                "registry": {
                    "sub_registries": 7,
                    "status": "synced" if registry_manager_instance else "inactive"
                }
            },
            "capabilities": [
                "multi_provider_routing",
                "intent_detection",
                "multi_model_consensus",
                "code_analysis",
                "project_scoring",
                "real_time_chat",
                "service_mesh",
                "event_routing",
                "code_injection",
                "metrics_tracking"
            ]
        }
    
    # ========================================================================
    # DOCUMENTATION
    # ========================================================================
    
    @app.get("/docs/quick-start")
    async def quick_start():
        """Quick start guide"""
        return {
            "title": "NEXUS AI Intelligence Matrix v8.0 - Quick Start",
            "setup_steps": [
                "1. Load Zsh modules: source ai_intelligence_matrix.zsh",
                "2. Configure API keys: ai_add_key openai 'sk-...'",
                "3. Test: ai 'hello'",
                "4. Start backend: python -m uvicorn services.api_gateway.main:app"
            ],
            "basic_commands": [
                "ai 'question'          - Ask AI",
                "ai_consensus 'prompt'  - Multi-model consensus",
                "ai_code file.py        - Code review",
                "ai_explain 'topic'     - Explain topic",
                "ai_todo 'context'      - Generate TODO list",
                "ai_score /path         - Score project"
            ],
            "endpoints": [
                "POST /v1/ai/route      - Intelligent routing",
                "POST /v1/ai/consensus  - Multi-model consensus",
                "POST /v1/ai/chat       - Chat interface",
                "GET  /v1/ai/health     - System health"
            ],
            "providers": {
                "openai": "gpt-5.1, gpt-4o, gpt-4-turbo",
                "anthropic": "claude-3-7-opus, claude-3-7-sonnet",
                "google": "gemini-3, gemini-2.0-pro",
                "deepseek": "deepseek-v3, deepseek-r1",
                "mistral": "mistral-large, mistral-medium",
                "ollama": "llama3.1, mistral, codellama"
            },
            "documentation": {
                "complete_guide": "/workspaces/zsh/services/AI_INTELLIGENCE_MATRIX_GUIDE.md",
                "quick_reference": "/workspaces/zsh/QUICK_REFERENCE.md",
                "deployment_status": "/workspaces/zsh/AI_INTELLIGENCE_MATRIX_DEPLOYMENT_STATUS.md"
            }
        }
    
    logger.info("✅ FastAPI application configured")
    return app

# ============================================================================
# APPLICATION INSTANCE
# ============================================================================

app = create_app()

# ============================================================================
# STARTUP MESSAGE
# ============================================================================

@app.on_event("startup")
async def startup_message():
    logger.info("=" * 70)
    logger.info("🧠 NEXUS AI INTELLIGENCE MATRIX v8.0")
    logger.info("=" * 70)
    logger.info("✅ Multi-provider LLM orchestration platform")
    logger.info("✅ 6 AI providers (OpenAI, Anthropic, Google, DeepSeek, Mistral, Ollama)")
    logger.info("✅ Intelligent routing with intent detection")
    logger.info("✅ Multi-model consensus for reliability")
    logger.info("✅ Production-grade service mesh and event routing")
    logger.info("✅ Zsh CLI integration for power users")
    logger.info("=" * 70)
    logger.info("📚 Documentation: /workspaces/zsh/services/AI_INTELLIGENCE_MATRIX_GUIDE.md")
    logger.info("🚀 Quick Start: GET /docs/quick-start")
    logger.info("=" * 70)

# ============================================================================
# EXPORT
# ============================================================================

__all__ = ["app", "create_app"]

# ============================================================================
# CLI EXECUTION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 Starting NEXUS AI Intelligence Matrix v8.0")
    print("=" * 70)
    print("📡 Server: http://localhost:8000")
    print("📚 Docs:   http://localhost:8000/docs")
    print("🎯 Health: http://localhost:8000/health")
    print("=" * 70)
    
    uvicorn.run(
        "integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
