#!/usr/bin/env python3
# ============================================================================
# 🎛️ NEXUS EVENT & MESSAGE ROUTER v2.0
# ============================================================================
# Advanced event routing with filtering, transformations, saga patterns,
# dead-letter queues, and comprehensive event sourcing.
# ============================================================================

import asyncio
import json
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable, Any, Set
from datetime import datetime, timedelta
from collections import defaultdict
import logging

# Optional integration with Hyper Registry
try:
    from services.hyper_registry.integrated import get_hyper_registry
    _HYPER_REGISTRY_AVAILABLE = True
except Exception:
    get_hyper_registry = None
    _HYPER_REGISTRY_AVAILABLE = False

logger = logging.getLogger(__name__)


class EventRoutingStrategy(str, Enum):
    """Event routing strategies."""
    DIRECT = "direct"  # Direct route to single handler
    BROADCAST = "broadcast"  # Route to all matching handlers
    ROUND_ROBIN = "round_robin"  # Route to handlers in round-robin
    WEIGHTED = "weighted"  # Route to handlers by weight
    FANOUT = "fanout"  # Route to multiple handlers asynchronously


class SagaTransactionState(str, Enum):
    """Saga transaction state."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass
class EventFilter:
    """Filter for routing events."""
    event_type: Optional[str] = None
    source_service: Optional[str] = None
    priority_min: Optional[int] = None
    priority_max: Optional[int] = None
    metadata_conditions: Dict[str, Any] = field(default_factory=dict)

    def matches(self, event: "Event") -> bool:
        """Check if event matches filter."""
        if self.event_type and event.event_type != self.event_type:
            return False

        if self.source_service and event.source_service != self.source_service:
            return False

        if self.priority_min and event.priority < self.priority_min:
            return False

        if self.priority_max and event.priority > self.priority_max:
            return False

        for key, value in self.metadata_conditions.items():
            if event.metadata.get(key) != value:
                return False

        return True


@dataclass
class Event:
    """Event for pub/sub system."""
    id: str
    event_type: str
    source_service: str
    payload: Dict[str, Any]
    priority: int = 5  # 1-10, where 10 is highest
    timestamp: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str = ""
    causation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_event: Optional[str] = None
    saga_id: Optional[str] = None


@dataclass
class EventHandler:
    """Handler for events."""
    id: str
    filter: EventFilter
    handler_func: Callable
    weight: int = 1
    max_retries: int = 3
    enabled: bool = True


@dataclass
class SagaTransaction:
    """Saga transaction for distributed operations."""
    id: str
    steps: List["SagaStep"] = field(default_factory=list)
    state: SagaTransactionState = SagaTransactionState.PENDING
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    failed_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SagaStep:
    """Individual step in a saga."""
    id: str
    name: str
    action: Callable
    compensation: Optional[Callable] = None
    status: str = "pending"  # pending, completed, failed, compensated
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class DeadLetterMessage:
    """Message that failed to process."""
    id: str
    event: Event
    handler_id: str
    error: str
    attempt_count: int
    first_failure_time: datetime = field(default_factory=datetime.utcnow)
    last_failure_time: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# 📨 EVENT ROUTER
# ============================================================================

class EventRouter:
    """Advanced event router with filtering, transformation, and saga support."""

    def __init__(self):
        self.handlers: Dict[str, List[EventHandler]] = defaultdict(list)
        self.handler_counter = 0
        self.event_history: List[Event] = []
        self.dead_letter_queue: List[DeadLetterMessage] = []
        self.sagas: Dict[str, SagaTransaction] = {}
        self.transformers: Dict[str, Callable] = {}
        self.route_stats: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"routed": 0, "failed": 0}
        )

        # If hyper-registry integration is available, auto-register discovery handler
        if _HYPER_REGISTRY_AVAILABLE:
            try:
                # Register handler for discovery events
                self.register_handler(
                    event_type="discovery.found",
                    handler_func=self._discovery_event_handler,
                    filter_config=EventFilter(event_type="discovery.found"),
                )
                logger.info("EventRouter: discovery.found handler registered for hyper-registry integration")
            except Exception as e:
                logger.warning(f"Failed to register discovery handler: {e}")

    def register_handler(
        self,
        event_type: str,
        handler_func: Callable,
        filter_config: Optional[EventFilter] = None,
        weight: int = 1,
    ) -> str:
        """Register event handler."""
        handler_id = f"handler_{self.handler_counter}"
        self.handler_counter += 1

        filter_obj = filter_config or EventFilter(event_type=event_type)
        handler = EventHandler(
            id=handler_id,
            filter=filter_obj,
            handler_func=handler_func,
            weight=weight,
        )

        self.handlers[event_type].append(handler)

        logger.info(f"Handler registered: {handler_id} for {event_type}")
        return handler_id

    def register_transformer(
        self,
        event_type: str,
        transformer: Callable[[Event], Event],
    ) -> None:
        """Register event transformer."""
        self.transformers[event_type] = transformer
        logger.info(f"Transformer registered for {event_type}")

    async def route_event(
        self,
        event: Event,
        strategy: EventRoutingStrategy = EventRoutingStrategy.BROADCAST,
    ) -> Dict[str, Any]:
        """Route event to handlers."""
        # Apply transformations
        if event.event_type in self.transformers:
            transformer = self.transformers[event.event_type]
            event = transformer(event)

        # Get matching handlers
        handlers = self._get_matching_handlers(event)

        if not handlers:
            logger.warning(f"No handlers for event: {event.event_type}")
            return {"status": "no_handlers", "event_id": event.id}

        # Store event
        self.event_history.append(event)
        self.route_stats[event.event_type]["routed"] += 1

        # Route based on strategy
        if strategy == EventRoutingStrategy.DIRECT:
            return await self._route_direct(event, handlers)

        elif strategy == EventRoutingStrategy.BROADCAST:
            return await self._route_broadcast(event, handlers)

        elif strategy == EventRoutingStrategy.ROUND_ROBIN:
            return await self._route_round_robin(event, handlers)

        elif strategy == EventRoutingStrategy.WEIGHTED:
            return await self._route_weighted(event, handlers)

        elif strategy == EventRoutingStrategy.FANOUT:
            return await self._route_fanout(event, handlers)

        return {"status": "unknown_strategy", "event_id": event.id}

    async def _route_direct(
        self,
        event: Event,
        handlers: List[EventHandler],
    ) -> Dict[str, Any]:
        """Route directly to first handler."""
        handler = handlers[0]

        try:
            result = await self._execute_handler(handler, event)
            return {"status": "success", "handler": handler.id, "result": result}

        except Exception as e:
            await self._handle_failure(event, handler, str(e))
            return {"status": "failed", "handler": handler.id, "error": str(e)}

    async def _route_broadcast(
        self,
        event: Event,
        handlers: List[EventHandler],
    ) -> Dict[str, Any]:
        """Route to all handlers."""
        results = {}

        for handler in handlers:
            try:
                result = await self._execute_handler(handler, event)
                results[handler.id] = {"status": "success", "result": result}

            except Exception as e:
                await self._handle_failure(event, handler, str(e))
                results[handler.id] = {"status": "failed", "error": str(e)}

        return {"status": "broadcast_complete", "handlers": results}

    async def _route_round_robin(
        self,
        event: Event,
        handlers: List[EventHandler],
    ) -> Dict[str, Any]:
        """Route in round-robin fashion."""
        if not handlers:
            return {"status": "no_handlers"}

        # Select based on previous routing
        index = hash(event.event_type) % len(handlers)
        handler = handlers[index]

        try:
            result = await self._execute_handler(handler, event)
            return {"status": "success", "handler": handler.id, "result": result}

        except Exception as e:
            await self._handle_failure(event, handler, str(e))
            return {"status": "failed", "handler": handler.id, "error": str(e)}

    async def _route_weighted(
        self,
        event: Event,
        handlers: List[EventHandler],
    ) -> Dict[str, Any]:
        """Route based on handler weights."""
        total_weight = sum(h.weight for h in handlers)
        selection_value = hash(event.id) % total_weight

        cumulative = 0
        selected_handler = handlers[0]

        for handler in handlers:
            cumulative += handler.weight
            if selection_value < cumulative:
                selected_handler = handler
                break

        try:
            result = await self._execute_handler(selected_handler, event)
            return {"status": "success", "handler": selected_handler.id, "result": result}

        except Exception as e:
            await self._handle_failure(event, selected_handler, str(e))
            return {"status": "failed", "handler": selected_handler.id, "error": str(e)}

    async def _route_fanout(
        self,
        event: Event,
        handlers: List[EventHandler],
    ) -> Dict[str, Any]:
        """Route to all handlers asynchronously (fanout)."""
        tasks = []

        for handler in handlers:
            task = asyncio.create_task(self._safe_execute(handler, event))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            "status": "fanout_complete",
            "handlers_count": len(handlers),
            "results_count": len(results),
        }

    async def _execute_handler(
        self,
        handler: EventHandler,
        event: Event,
    ) -> Any:
        """Execute handler with retry logic."""
        for attempt in range(handler.max_retries):
            try:
                result = handler.handler_func(event)

                if asyncio.iscoroutine(result):
                    result = await result

                logger.info(f"Handler executed: {handler.id} for {event.event_type}")
                return result

            except Exception as e:
                if attempt < handler.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise

    async def _safe_execute(
        self,
        handler: EventHandler,
        event: Event,
    ) -> None:
        """Safely execute handler, catching errors."""
        try:
            await self._execute_handler(handler, event)

        except Exception as e:
            await self._handle_failure(event, handler, str(e))

    async def _handle_failure(
        self,
        event: Event,
        handler: EventHandler,
        error: str,
    ) -> None:
        """Handle handler failure."""
        dlm = DeadLetterMessage(
            id=f"dlm_{len(self.dead_letter_queue)}",
            event=event,
            handler_id=handler.id,
            error=error,
        )

        self.dead_letter_queue.append(dlm)
        self.route_stats[event.event_type]["failed"] += 1

        logger.error(f"Event failed: {event.id} in {handler.id}: {error}")

    async def _discovery_event_handler(self, event: Event) -> Dict[str, Any]:
        """Handle discovery.found events by registering discovered resources into the hyper-registry.

        Expected payload format: {"resources": [{"id":..., "type":..., "meta": {...}}, ...]}
        """
        logger.info(f"Discovery handler invoked for event {event.id}")

        if not _HYPER_REGISTRY_AVAILABLE:
            logger.warning("Hyper registry not available; skipping registration")
            return {"status": "registry_unavailable"}

        try:
            registry = get_hyper_registry()
            resources = event.payload.get("resources", []) if isinstance(event.payload, dict) else []
            registered = []

            for r in resources:
                try:
                    # Normalize resource dict
                    entry = {
                        "title": r.get("id") if isinstance(r, dict) else str(r),
                        "description": r.get("meta", {}),
                        "source": event.source_service,
                        "discovery_timestamp": event.timestamp.isoformat(),
                        "raw": r,
                    }

                    # Async register - registry.register_entry is async
                    entry_id = await registry.register_entry(entry)
                    registered.append(entry_id)
                    logger.info(f"Registered discovery resource {r.get('id')} as {entry_id}")

                except Exception as e:
                    logger.error(f"Failed to register resource {r}: {e}")

            return {"status": "registered", "count": len(registered), "ids": registered}

        except Exception as e:
            logger.error(f"Discovery handler error: {e}")
            return {"status": "error", "error": str(e)}

    def _get_matching_handlers(self, event: Event) -> List[EventHandler]:
        """Get handlers matching event."""
        candidates = self.handlers.get(event.event_type, [])
        matching = [h for h in candidates if h.enabled and h.filter.matches(event)]
        return sorted(matching, key=lambda h: -h.weight)

    async def replay_dead_letter_queue(self) -> Dict[str, int]:
        """Replay dead letter messages."""
        recovered = 0
        still_failed = 0

        for dlm in self.dead_letter_queue[:]:
            try:
                result = await self.route_event(dlm.event)
                if result.get("status") == "success":
                    self.dead_letter_queue.remove(dlm)
                    recovered += 1
                else:
                    still_failed += 1

            except Exception as e:
                still_failed += 1

        logger.info(f"DLQ Replay: {recovered} recovered, {still_failed} still failed")
        return {"recovered": recovered, "still_failed": still_failed}

    def get_event_history(self, limit: int = 100) -> List[Event]:
        """Get recent event history."""
        return self.event_history[-limit:]

    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        total_routed = sum(s["routed"] for s in self.route_stats.values())
        total_failed = sum(s["failed"] for s in self.route_stats.values())

        return {
            "total_routed": total_routed,
            "total_failed": total_failed,
            "dlq_size": len(self.dead_letter_queue),
            "by_event_type": dict(self.route_stats),
        }


# ============================================================================
# 🎭 SAGA ORCHESTRATOR
# ============================================================================

class SagaOrchestrator:
    """Orchestrate distributed transactions using saga pattern."""

    def __init__(self):
        self.sagas: Dict[str, SagaTransaction] = {}

    async def execute_saga(
        self,
        saga_id: str,
        steps: List[SagaStep],
    ) -> SagaTransaction:
        """Execute saga with compensation on failure."""
        saga = SagaTransaction(id=saga_id, steps=steps)
        self.sagas[saga_id] = saga

        try:
            saga.state = SagaTransactionState.IN_PROGRESS

            # Execute forward steps
            for step in saga.steps:
                try:
                    step.status = "pending"
                    result = step.action()

                    if asyncio.iscoroutine(result):
                        result = await result

                    step.result = result
                    step.status = "completed"

                    logger.info(f"Saga step completed: {step.name} ({saga_id})")

                except Exception as e:
                    step.status = "failed"
                    step.error = str(e)

                    logger.error(f"Saga step failed: {step.name}: {e}")

                    # Begin compensation
                    await self._compensate_saga(saga)
                    saga.state = SagaTransactionState.FAILED
                    saga.failed_reason = str(e)

                    return saga

            saga.state = SagaTransactionState.COMPLETED
            saga.completed_at = datetime.utcnow()

            logger.info(f"Saga completed successfully: {saga_id}")

        except Exception as e:
            saga.state = SagaTransactionState.FAILED
            saga.failed_reason = str(e)
            logger.error(f"Saga execution failed: {e}")

        return saga

    async def _compensate_saga(self, saga: SagaTransaction) -> None:
        """Execute compensation steps in reverse order."""
        saga.state = SagaTransactionState.COMPENSATING

        logger.info(f"Starting saga compensation: {saga.id}")

        # Execute compensation steps in reverse
        for step in reversed(saga.steps):
            if step.status == "completed" and step.compensation:
                try:
                    result = step.compensation()

                    if asyncio.iscoroutine(result):
                        result = await result

                    step.status = "compensated"

                    logger.info(f"Saga step compensated: {step.name} ({saga.id})")

                except Exception as e:
                    logger.error(f"Saga compensation failed: {step.name}: {e}")

    def get_saga_status(self, saga_id: str) -> Optional[SagaTransaction]:
        """Get saga status."""
        return self.sagas.get(saga_id)
