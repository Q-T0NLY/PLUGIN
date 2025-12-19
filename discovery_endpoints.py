from fastapi import APIRouter, HTTPException
from fastapi import Body
import asyncio
import os
import sys
import logging
from typing import Any, Dict, List
import uuid
from datetime import datetime

# EventRouter import (optional)
try:
    from services.api_gateway.event_router import EventRouter, Event
except Exception:
    EventRouter = None
    Event = None

LOGGER = logging.getLogger("discovery_endpoints")

# Ensure discovery module is importable (relative path)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'discovery'))
try:
    from hop_orchestrator import NeuralDiscoveryOrchestrator, DiscoveredResource
except Exception as e:  # pragma: no cover - import guard for scaffold
    LOGGER.warning("Could not import hop_orchestrator: %s", e)
    NeuralDiscoveryOrchestrator = None

router = APIRouter()

# Singleton orchestrator for the router
_orch: NeuralDiscoveryOrchestrator = None
_orch_lock = asyncio.Lock()
_last_report: Dict[str, Any] = {}


def get_orchestrator() -> NeuralDiscoveryOrchestrator:
    global _orch
    if _orch is None:
        if NeuralDiscoveryOrchestrator is None:
            raise RuntimeError("NeuralDiscoveryOrchestrator not available")
        _orch = NeuralDiscoveryOrchestrator()
    return _orch


@router.post("/trigger")
async def trigger_discovery(payload: Dict[str, Any] = Body(...)):
    """Trigger a discovery cycle. Payload: {"mode": "full|services|datastores|incremental"}

    This endpoint will serialize concurrent runs using an asyncio lock.
    """
    mode = payload.get("mode", "full")
    orch = get_orchestrator()

    if _orch_lock.locked():
        raise HTTPException(status_code=409, detail="Discovery already running")

    async with _orch_lock:
        report = await orch.run_cycle(mode=mode)
        global _last_report
        _last_report = report
        # Emit discovery event to EventRouter if available
        try:
            if EventRouter is not None and Event is not None:
                er = EventRouter()
                event = Event(
                    id=str(uuid.uuid4()),
                    event_type="discovery.found",
                    source_service="hop_orchestrator",
                    payload={"resources": getattr(orch, '_results', [])},
                    priority=5,
                    timestamp=datetime.utcnow(),
                )

                # Fire-and-forget routing
                asyncio.create_task(er.route_event(event))
        except Exception as e:
            LOGGER.warning("Failed to emit discovery event: %s", e)
        return {"status": "ok", "report": report}


@router.get("/status")
async def discovery_status():
    orch = get_orchestrator()
    return {
        "running": getattr(orch, "_running", False),
        "found": len(getattr(orch, "_results", [])),
        "last_report": _last_report,
    }


@router.get("/results")
async def discovery_results():
    orch = get_orchestrator()
    results = getattr(orch, "_results", [])
    # Serialize DiscoveredResource objects
    serialized = [
        {"id": r.id, "type": r.type, "meta": r.meta} for r in results
    ]
    return {"count": len(serialized), "results": serialized}


@router.get("/topology")
async def discovery_topology():
    """Return nodes/edges representing discovered resources for visualization.

    Simple heuristic: create node per resource and link services to databases/caches
    if ports or engine types are present in meta.
    """
    orch = get_orchestrator()
    results = getattr(orch, "_results", [])
    nodes = []
    edges = []

    # Build nodes
    for r in results:
        nodes.append({"id": r.id, "label": f"{r.id}\n({r.type})", "meta": r.meta})

    # Simple linking heuristics
    id_map = {r.id: r for r in results}
    for r in results:
        if r.type == "service":
            # connect service to any database/cache matching common keywords
            for other in results:
                if other.id == r.id:
                    continue
                if other.type in ("database", "cache"):
                    edges.append({"source": r.id, "target": other.id})

    return {"nodes": nodes, "edges": edges}
