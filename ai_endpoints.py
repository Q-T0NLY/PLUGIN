#!/usr/bin/env python3
# ============================================================================
# 🌐 NEXUS AI API ENDPOINTS - FastAPI Integration Layer
# ============================================================================
# Exposes AI Intelligence Matrix, Service Mesh, Event Router, and
# Infrastructure Bridge capabilities via REST API and WebSocket
# ============================================================================

from fastapi import APIRouter, HTTPException, WebSocket, BackgroundTasks, Query
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

# Import backend services
try:
    from services.ai_matrix.core import (
        IntentDetector,
        UniversalAdapter,
        ConsensusEngine,
        AIMetrics,
        Intent,
        ProviderCapability
    )
    from services.api_gateway.api_manager import get_api_manager
    from services.api_gateway.service_mesh import ServiceMesh
    from services.api_gateway.event_router import EventRouter
    from services.llm_orchestrator.llm_service_bridge import LLMServiceBridge
except ImportError as e:
    logging.warning(f"Could not import backend services: {e}")

# ============================================================================
# SETUP
# ============================================================================

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/ai", tags=["AI Intelligence Matrix"])

# Initialize components
intent_detector = IntentDetector()
universal_adapter = UniversalAdapter()
consensus_engine = ConsensusEngine()
ai_metrics = AIMetrics()
llm_bridge = LLMServiceBridge()
api_manager = get_api_manager()

# ============================================================================
# DATA MODELS
# ============================================================================

class AIRouteRequest(BaseModel):
    prompt: str
    strategy: str = "auto"  # auto, consensus, fastest, cost-optimized, best-match
    models: Optional[List[str]] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    timestamp: Optional[str] = None

class AIConsensusRequest(BaseModel):
    prompt: str
    models: List[str] = ["gpt-4o", "claude-3-7-sonnet", "gemini-3"]
    strategy: str = "consensus"
    temperature: float = 0.7

class AICodeAnalysisRequest(BaseModel):
    file_path: str
    language: str
    code: str
    analysis_type: str = "full"  # full, security, performance, style

class AIProjectAnalysisRequest(BaseModel):
    project_path: str
    analysis_depth: str = "standard"  # standard, detailed, comprehensive
    include_metrics: bool = True

class AIChatMessage(BaseModel):
    session_id: str
    message: str
    timestamp: Optional[str] = None
    model: Optional[str] = None

class CredentialRequest(BaseModel):
    provider: str
    api_key: str

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@router.get("/health")
async def ai_health():
    """Check AI system health status"""
    try:
        adapter_health = await universal_adapter.check_health()
        return JSONResponse({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "adapters": adapter_health,
            "metrics": {
                "total_calls": ai_metrics.total_calls,
                "total_tokens": ai_metrics.total_tokens_used,
                "avg_latency": ai_metrics.get_average_latency()
            }
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    """Get list of available models and providers"""
    try:
        models = await universal_adapter.get_available_models()
        return JSONResponse({
            "models": models,
            "providers": list(universal_adapter.providers.keys()),
            "count": len(models),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# INTELLIGENT ROUTING ENDPOINTS
# ============================================================================

@router.post("/route")
async def intelligent_route(request: AIRouteRequest):
    """
    Intelligently route request to best provider/model combination
    
    Strategies:
    - auto: Auto-select based on intent
    - consensus: Multi-model consensus
    - fastest: First-to-respond
    - cost-optimized: Cheapest option
    - best-match: Highest capability score
    """
    try:
        # Detect intent
        intent_analysis = intent_detector.detect_intent(request.prompt)
        
        # Log request
        ai_metrics.log_request(
            provider="intelligent_router",
            model="auto",
            tokens=len(request.prompt.split())
        )
        
        # Route based on strategy
        if request.strategy == "auto":
            response = await llm_bridge.orchestrate_multi_provider_call(
                request.prompt,
                strategy="best_match"
            )
        elif request.strategy == "consensus":
            response = await consensus_engine.evaluate_multi_model(
                request.prompt,
                request.models or ["gpt-4o", "claude-3-7-sonnet", "gemini-3"]
            )
        elif request.strategy == "fastest":
            response = await llm_bridge.orchestrate_multi_provider_call(
                request.prompt,
                strategy="fastest"
            )
        elif request.strategy == "cost-optimized":
            response = await llm_bridge.orchestrate_multi_provider_call(
                request.prompt,
                strategy="cost_optimized"
            )
        else:
            response = await llm_bridge.orchestrate_multi_provider_call(
                request.prompt,
                strategy="best_match"
            )
        
        return JSONResponse({
            "response": response,
            "intent": intent_analysis.intent.value,
            "confidence": intent_analysis.confidence,
            "strategy": request.strategy,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Route failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/consensus")
async def multi_model_consensus(request: AIConsensusRequest):
    """Execute multi-model consensus evaluation"""
    try:
        ai_metrics.log_request(
            provider="consensus",
            model="multi-model",
            tokens=len(request.prompt.split())
        )
        
        consensus_result = await consensus_engine.evaluate_multi_model(
            request.prompt,
            request.models
        )
        
        return JSONResponse({
            "consensus_result": consensus_result,
            "models": request.models,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Consensus failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CODE ANALYSIS ENDPOINTS
# ============================================================================

@router.post("/analyze-code")
async def analyze_code(request: AICodeAnalysisRequest):
    """Analyze code for bugs, security, performance"""
    try:
        analysis_prompt = f"""Analyze this {request.language} code for:
        - Bugs and errors
        - Security vulnerabilities
        - Performance issues
        - Code style and best practices
        
        Code:
        ```{request.language}
        {request.code}
        ```
        
        Provide detailed analysis with severity levels."""
        
        response = await llm_bridge.orchestrate_multi_provider_call(
            analysis_prompt,
            strategy="best_match"
        )
        
        ai_metrics.log_analysis("code", request.language)
        
        return JSONResponse({
            "file": request.file_path,
            "language": request.language,
            "analysis_type": request.analysis_type,
            "analysis": response,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-project")
async def analyze_project(request: AIProjectAnalysisRequest):
    """Analyze entire project structure and metrics"""
    try:
        import os
        from pathlib import Path
        
        # Scan project
        project_path = Path(request.project_path)
        file_stats = {
            "total_files": len(list(project_path.rglob("*"))),
            "python_files": len(list(project_path.rglob("*.py"))),
            "js_files": len(list(project_path.rglob("*.js"))),
            "json_files": len(list(project_path.rglob("*.json"))),
            "md_files": len(list(project_path.rglob("*.md")))
        }
        
        analysis_prompt = f"""Analyze this software project:
        Path: {request.project_path}
        Files: {file_stats}
        
        Provide:
        1. Architecture assessment (score 0-100)
        2. Documentation quality (score 0-100)
        3. Test coverage estimate (score 0-100)
        4. Security posture (score 0-100)
        5. Performance recommendations
        6. Refactoring priorities"""
        
        response = await llm_bridge.orchestrate_multi_provider_call(
            analysis_prompt,
            strategy="best_match"
        )
        
        ai_metrics.log_analysis("project", request.project_path)
        
        return JSONResponse({
            "project": str(project_path),
            "file_stats": file_stats,
            "analysis": response,
            "depth": request.analysis_depth,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Project analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CHAT SESSION ENDPOINTS
# ============================================================================

chat_sessions: Dict[str, List[Dict]] = {}

@router.post("/chat")
async def chat(request: AIChatMessage):
    """Process chat message with session support"""
    try:
        # Initialize session if needed
        if request.session_id not in chat_sessions:
            chat_sessions[request.session_id] = []
        
        # Add message to history
        chat_sessions[request.session_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Get response
        response = await llm_bridge.orchestrate_multi_provider_call(
            request.message,
            strategy="best_match"
        )
        
        # Add to history
        chat_sessions[request.session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        ai_metrics.log_request(
            provider="chat",
            model=request.model or "auto",
            tokens=len(request.message.split())
        )
        
        return JSONResponse({
            "session_id": request.session_id,
            "message": request.message,
            "response": response,
            "history_length": len(chat_sessions[request.session_id]),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat session history"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return JSONResponse({
        "session_id": session_id,
        "messages": chat_sessions[session_id],
        "length": len(chat_sessions[session_id])
    })

@router.delete("/chat/{session_id}")
async def clear_chat_session(session_id: str):
    """Clear chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return JSONResponse({"status": "cleared"})
    raise HTTPException(status_code=404, detail="Session not found")

# ============================================================================
# CREDENTIALS MANAGEMENT
# ============================================================================

@router.post("/credentials")
async def add_credentials(request: CredentialRequest):
    """Register API credentials for provider"""
    try:
        # Store in universal adapter
        await universal_adapter.set_provider_credential(
            request.provider,
            request.api_key
        )
        
        return JSONResponse({
            "status": "registered",
            "provider": request.provider,
            "timestamp": datetime.utcnow().isoformat()
        }, status_code=201)
    except Exception as e:
        logger.error(f"Credential registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ADAPTER STATUS ENDPOINTS
# ============================================================================

@router.get("/status/adapters")
async def adapter_status():
    """Get status of all provider adapters"""
    try:
        status = {}
        for provider_name, adapter in universal_adapter.providers.items():
            status[provider_name] = {
                "available": await adapter.check_health(),
                "models": len(adapter.available_models) if hasattr(adapter, 'available_models') else 0,
                "latency_ms": 0  # Would need actual monitoring
            }
        
        return JSONResponse({
            "adapters": status,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Adapter status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# METRICS & MONITORING ENDPOINTS
# ============================================================================

@router.get("/metrics")
async def get_metrics():
    """Get AI system metrics"""
    return JSONResponse({
        "total_requests": ai_metrics.total_calls,
        "total_tokens": ai_metrics.total_tokens_used,
        "avg_latency_ms": ai_metrics.get_average_latency(),
        "providers": {
            name: {
                "calls": count,
                "avg_latency": latency
            }
            for name, count, latency in ai_metrics.get_provider_stats()
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@router.get("/metrics/providers/{provider}")
async def provider_metrics(provider: str):
    """Get metrics for specific provider"""
    try:
        stats = ai_metrics.get_provider_stats(provider)
        return JSONResponse({
            "provider": provider,
            "metrics": stats,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Provider metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STREAMING ENDPOINTS
# ============================================================================

@router.post("/stream")
async def stream_response(request: AIRouteRequest):
    """Stream response for long-running requests"""
    async def response_generator():
        try:
            # Start streaming from AI
            async for chunk in llm_bridge.orchestrate_streaming(
                request.prompt,
                strategy=request.strategy
            ):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream"
    )

# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket for real-time chat"""
    await websocket.accept()
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            if not message:
                continue
            
            # Process request
            response = await llm_bridge.orchestrate_multi_provider_call(
                message,
                strategy="best_match"
            )
            
            # Send response
            await websocket.send_json({
                "type": "response",
                "message": message,
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            ai_metrics.log_request("websocket", "auto", len(message.split()))
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1000)

# ============================================================================
# INTEGRATION WITH MAIN FASTAPI APP
# ============================================================================

def initialize_ai_routes(app):
    """Initialize AI routes in main FastAPI app"""
    app.include_router(router)
    
    # Initialize cache and metrics
    asyncio.create_task(initialize_ai_metrics())
    
    logger.info("✅ AI Intelligence Matrix endpoints initialized")

async def initialize_ai_metrics():
    """Initialize AI metrics collection"""
    # Would connect to monitoring system
    pass

# ============================================================================
# CLI INTEGRATION SUPPORT
# ============================================================================

@router.get("/registries/ai_registry.json")
async def get_ai_registry():
    """Get AI provider registry for Zsh CLI integration"""
    return JSONResponse({
        "providers": {
            provider: {
                "name": provider,
                "status": "active",
                "models": list(adapter.available_models.keys()) if hasattr(adapter, 'available_models') else [],
                "capabilities": []
            }
            for provider, adapter in universal_adapter.providers.items()
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@router.get("/health/adapters")
async def get_adapters_health():
    """Get adapter health for Zsh CLI"""
    return JSONResponse(await adapter_status())

# Export for integration
__all__ = ["router", "initialize_ai_routes"]
