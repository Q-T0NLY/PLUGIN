#!/usr/bin/env python3
# ============================================================================
# 🌐 NEXUS PRODUCTION API GATEWAY v1.0.0
# ============================================================================
# FastAPI gateway with dual WebSocket support (native + socket.io),
# DAG visualization streaming, and complete orchestration API.
# ============================================================================

from fastapi import FastAPI, HTTPException, WebSocket, Depends, Header
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import logging
import importlib.util
from typing import Set, Dict, Any, Optional
from datetime import datetime
import os

# Import orchestrator
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dag_engine'))
from core import (
    LiveDAGOrchestrator,
    get_orchestrator,
    DAGWorkflow,
    DAGNode,
    DAGEdge,
    NodeType,
    ExecutionRequest,
    ExecutionResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 🚀 FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title="Nexus Production API Gateway",
    version="1.0.0",
    description="Real-time DAG orchestration with multi-modal visualization"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamically load optional discovery router if present
try:
    discovery_path = os.path.join(os.path.dirname(__file__), "discovery_endpoints.py")
    if os.path.exists(discovery_path):
        spec = importlib.util.spec_from_file_location("discovery_endpoints", discovery_path)
        discovery_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(discovery_mod)
        if hasattr(discovery_mod, "router"):
            app.include_router(discovery_mod.router, prefix="/api/discovery")
            logger.info("Discovery router included at /api/discovery")
except Exception as e:
    logger.warning(f"Failed to include discovery router: {e}")

# Dynamically load multimodal ingestion router if present
try:
    multimodal_path = os.path.join(os.path.dirname(__file__), "multimodal_endpoints.py")
    if os.path.exists(multimodal_path):
        spec = importlib.util.spec_from_file_location("multimodal_endpoints", multimodal_path)
        multimodal_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(multimodal_mod)
        if hasattr(multimodal_mod, "router"):
            app.include_router(multimodal_mod.router, prefix="/api")
            logger.info("Multimodal ingest router included at /api/ingest")
except Exception as e:
    logger.warning(f"Failed to include multimodal router: {e}")

# Dynamically load intelligence router if present
try:
    intelligence_path = os.path.join(os.path.dirname(__file__), "intelligence_endpoints.py")
    if os.path.exists(intelligence_path):
        spec = importlib.util.spec_from_file_location("intelligence_endpoints", intelligence_path)
        intelligence_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(intelligence_mod)
        if hasattr(intelligence_mod, "router"):
            app.include_router(intelligence_mod.router)
            logger.info("Intelligence router included at /api/intelligence")
except Exception as e:
    logger.warning(f"Failed to include intelligence router: {e}")

# ============================================================================
# 🔐 AUTHENTICATION
# ============================================================================

async def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """Verify API token (simple header check)."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # For production, validate against token store
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = authorization.replace("Bearer ", "")
    
    # Simple validation (in production use JWT or similar)
    if len(token) < 16:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token


# ============================================================================
# 📡 WEBSOCKET CONNECTION MANAGEMENT (Dual Mode)
# ============================================================================

class WebSocketManager:
    """Manages both native WebSocket and socket.io connections."""

    def __init__(self):
        self.active_native_connections: Dict[str, Set[WebSocket]] = {}
        self.active_socketio_connections: Dict[str, Set[str]] = {}

    async def add_native_connection(self, workflow_id: str, websocket: WebSocket) -> None:
        """Add native WebSocket connection."""
        await websocket.accept()
        if workflow_id not in self.active_native_connections:
            self.active_native_connections[workflow_id] = set()
        self.active_native_connections[workflow_id].add(websocket)
        logger.info(f"Native WebSocket connected for workflow {workflow_id}")

    async def remove_native_connection(self, workflow_id: str, websocket: WebSocket) -> None:
        """Remove native WebSocket connection."""
        if workflow_id in self.active_native_connections:
            self.active_native_connections[workflow_id].discard(websocket)
            if not self.active_native_connections[workflow_id]:
                del self.active_native_connections[workflow_id]
        logger.info(f"Native WebSocket disconnected for workflow {workflow_id}")

    async def broadcast_native(self, workflow_id: str, message: Dict[str, Any]) -> None:
        """Broadcast message to all native WebSocket clients."""
        if workflow_id in self.active_native_connections:
            disconnected = set()
            for connection in self.active_native_connections[workflow_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send to WebSocket: {e}")
                    disconnected.add(connection)
            
            # Cleanup disconnected
            for conn in disconnected:
                await self.remove_native_connection(workflow_id, conn)

    def add_socketio_connection(self, workflow_id: str, client_id: str) -> None:
        """Add socket.io connection."""
        if workflow_id not in self.active_socketio_connections:
            self.active_socketio_connections[workflow_id] = set()
        self.active_socketio_connections[workflow_id].add(client_id)
        logger.info(f"Socket.io connected for workflow {workflow_id}: {client_id}")

    def remove_socketio_connection(self, workflow_id: str, client_id: str) -> None:
        """Remove socket.io connection."""
        if workflow_id in self.active_socketio_connections:
            self.active_socketio_connections[workflow_id].discard(client_id)
            if not self.active_socketio_connections[workflow_id]:
                del self.active_socketio_connections[workflow_id]

    def broadcast_socketio_pending(self, workflow_id: str, message: Dict[str, Any]) -> None:
        """Queue message for socket.io broadcast (implement with python-socketio)."""
        # This would integrate with python-socketio if used
        # For now, return the pending broadcasts
        return {"workflow_id": workflow_id, "message": message}


ws_manager = WebSocketManager()


# ============================================================================
# 📊 REST ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "nexus-api-gateway",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/metrics")
async def metrics(token: str = Depends(verify_token)):
    """Prometheus metrics endpoint."""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return CONTENT_TYPE_LATEST(generate_latest())


@app.post("/api/workflows")
async def create_workflow(req: Dict[str, Any], token: str = Depends(verify_token)):
    """Create a new DAG workflow."""
    try:
        orchestrator = await get_orchestrator()
        workflow_name = req.get("name", f"workflow_{datetime.utcnow().timestamp()}")
        workflow = orchestrator.create_workflow(workflow_name)

        # Add nodes
        for node_spec in req.get("nodes", []):
            node = DAGNode(
                id=node_spec.get("id"),
                type=NodeType(node_spec.get("type", "transform")),
                name=node_spec.get("name"),
                config=node_spec.get("config", {}),
                dependencies=node_spec.get("dependencies", []),
                emoji=node_spec.get("emoji"),
                color=node_spec.get("color"),
                animation=node_spec.get("animation", "pulse"),
            )
            workflow.add_node(node)

        # Add edges
        for edge_spec in req.get("edges", []):
            edge = DAGEdge(
                source=edge_spec.get("source"),
                target=edge_spec.get("target"),
            )
            workflow.add_edge(edge)

        return {
            "workflow_id": workflow.id,
            "name": workflow.name,
            "nodes_count": len(workflow.nodes),
            "edges_count": len(workflow.edges),
            "created_at": workflow.created_at.isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflows/{workflow_id}")
async def get_workflow(workflow_id: str, token: str = Depends(verify_token)):
    """Get workflow details."""
    try:
        orchestrator = await get_orchestrator()
        workflow = await orchestrator.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        return {
            "workflow_id": workflow.id,
            "name": workflow.name,
            "nodes_count": len(workflow.nodes),
            "edges_count": len(workflow.edges),
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workflows/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, req: Dict[str, Any], token: str = Depends(verify_token)):
    """Execute a DAG workflow."""
    try:
        orchestrator = await get_orchestrator()
        execution_req = ExecutionRequest(
            workflow_id=workflow_id,
            params=req.get("params", {}),
            timeout_seconds=req.get("timeout_seconds", 600),
        )
        
        execution = await orchestrator.execute_workflow(workflow_id, execution_req)

        return {
            "execution_id": execution.execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
        }
    except Exception as e:
        logger.error(f"Failed to execute workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/executions/{execution_id}")
async def get_execution(execution_id: str, token: str = Depends(verify_token)):
    """Get execution status and results."""
    try:
        orchestrator = await get_orchestrator()
        execution = await orchestrator.get_execution(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        return {
            "execution_id": execution.execution_id,
            "workflow_id": execution.workflow_id,
            "status": execution.status.value,
            "nodes_executed": execution.nodes_executed,
            "nodes_failed": execution.nodes_failed,
            "result": execution.result,
            "error": execution.error,
            "start_time": execution.start_time.isoformat() if execution.start_time else None,
            "end_time": execution.end_time.isoformat() if execution.end_time else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dag/{workflow_id}/visualization")
async def get_dag_visualization(workflow_id: str, execution_id: Optional[str] = None):
    """Get DAG visualization data."""
    try:
        orchestrator = await get_orchestrator()
        workflow = await orchestrator.get_workflow(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Use provided execution or latest
        if not execution_id:
            execution_id = list(orchestrator.executions.keys())[-1] if orchestrator.executions else None

        if not execution_id:
            execution = ExecutionResponse(
                execution_id="none",
                workflow_id=workflow_id,
                status=workflow.status
            )
        else:
            execution = await orchestrator.get_execution(execution_id)
            if not execution:
                raise HTTPException(status_code=404, detail="Execution not found")

        viz_data = orchestrator.generate_visualization(workflow, execution)
        return viz_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get visualization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 🔌 NATIVE WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/api/ws/dag-updates")
async def websocket_dag_updates(websocket: WebSocket):
    """Native WebSocket endpoint for real-time DAG updates."""
    workflow_id = None
    try:
        await websocket.accept()
        
        # First message should contain workflow_id
        init_msg = await websocket.receive_json()
        workflow_id = init_msg.get("workflow_id")
        execution_id = init_msg.get("execution_id")

        if not workflow_id:
            await websocket.send_json({"error": "workflow_id required"})
            await websocket.close()
            return

        await ws_manager.add_native_connection(workflow_id, websocket)

        # Send initial visualization
        orchestrator = await get_orchestrator()
        workflow = await orchestrator.get_workflow(workflow_id)
        if workflow and execution_id:
            execution = await orchestrator.get_execution(execution_id)
            if execution:
                viz_data = orchestrator.generate_visualization(workflow, execution)
                await websocket.send_json({
                    "type": "initial",
                    "data": viz_data
                })

        # Listen for connection (keep-alive)
        while True:
            try:
                msg = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo pings
                if msg == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # Send keep-alive ping
                await websocket.send_json({"type": "ping"})

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if workflow_id:
            await ws_manager.remove_native_connection(workflow_id, websocket)


# ============================================================================
# 🔗 SOCKET.IO INTEGRATION (STUB FOR PYTHON-SOCKETIO)
# ============================================================================

# To use with python-socketio, uncomment and configure:
# from socketio import AsyncServer
# sio = AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# 
# @sio.on('connect')
# async def socketio_connect(sid, environ):
#     logger.info(f"Socket.io client connected: {sid}")
#
# @sio.on('subscribe_dag')
# async def subscribe_dag(sid, data):
#     workflow_id = data.get('workflow_id')
#     ws_manager.add_socketio_connection(workflow_id, sid)
#
# @sio.on('disconnect')
# async def socketio_disconnect(sid):
#     # Clean up all subscriptions for this client
#     pass
#
# # Mount socket.io app
# sio_app = socketio.ASGIApp(sio, app)


# ============================================================================
# 📢 REDIS PUB/SUB FOR BROADCASTING UPDATES
# ============================================================================

async def redis_listener_task():
    """Background task to listen for Redis pub/sub and broadcast updates."""
    import redis.asyncio as redis
    
    try:
        redis_client = await redis.from_url("redis://localhost:6379", decode_responses=True)
        pubsub = redis_client.pubsub()
        
        # Subscribe to all DAG update channels
        await pubsub.psubscribe("nexuspro:dag:updates:*")
        
        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"]
                data = json.loads(message["data"])
                
                # Extract workflow_id from channel
                workflow_id = channel.split(":")[-1]
                
                # Broadcast to connected native WebSocket clients
                await ws_manager.broadcast_native(workflow_id, {
                    "type": "update",
                    "data": data
                })
                
    except Exception as e:
        logger.error(f"Redis listener error: {e}")


# ============================================================================
# 🎯 STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    logger.info("Starting Nexus API Gateway...")
    
    # Initialize orchestrator
    orchestrator = await get_orchestrator()
    logger.info("Orchestrator initialized")
    
    # Start Redis listener
    asyncio.create_task(redis_listener_task())
    logger.info("Redis listener started")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    logger.info("Shutting down Nexus API Gateway...")
    orchestrator = await get_orchestrator()
    await orchestrator.shutdown()


# ============================================================================
# 📁 STATIC FILES (Optional)
# ============================================================================

# Uncomment to serve frontend from /static
# app.mount("/static", StaticFiles(directory="/path/to/frontend/build"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
