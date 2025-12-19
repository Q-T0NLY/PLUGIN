#!/usr/bin/env python3
# ============================================================================
# 🔗 NEXUS INFRASTRUCTURE BRIDGE v2.0
# ============================================================================
# Integration layer connecting API Manager, Service Mesh, and Event Router
# into a unified orchestration platform with lifecycle management.
# ============================================================================

import asyncio
import json
from dataclasses import asdict
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class InfrastructureBridge:
    """Unified infrastructure orchestration bridge."""

    def __init__(self, api_manager, service_mesh, event_router):
        self.api_manager = api_manager
        self.mesh = service_mesh
        self.router = event_router
        self.service_lifecycle_hooks: Dict[str, Dict[str, Any]] = {}

    # ========================================================================
    # 🚀 SERVICE LIFECYCLE MANAGEMENT
    # ========================================================================

    async def register_service(
        self,
        service_id: str,
        name: str,
        version: str,
        endpoints: List[Dict[str, str]],
        on_start: Optional[callable] = None,
        on_shutdown: Optional[callable] = None,
        on_health_check: Optional[callable] = None,
        health_check_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Complete service registration with lifecycle hooks."""

        # Register in service registry
        descriptor = {
            "id": service_id,
            "name": name,
            "version": version,
            "namespace": "default",
            "endpoints": {ep["path"]: ep.get("method", "GET") for ep in endpoints},
            "health_check_url": health_check_url,
        }

        from api_manager import ServiceDescriptor

        service_desc = ServiceDescriptor(**descriptor)
        await self.api_manager.registry.register(service_desc)

        # Store lifecycle hooks
        self.service_lifecycle_hooks[service_id] = {
            "on_start": on_start,
            "on_shutdown": on_shutdown,
            "on_health_check": on_health_check,
        }

        # Emit service started event
        from event_router import Event, EventRoutingStrategy

        event = Event(
            id=f"svc_start_{service_id}",
            event_type="service.started",
            source_service="infrastructure",
            payload={"service_id": service_id, "name": name, "version": version},
            correlation_id=service_id,
        )

        await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

        # Execute startup hook
        if on_start:
            try:
                result = on_start()
                if asyncio.iscoroutine(result):
                    await result
                logger.info(f"Service startup hook executed: {service_id}")
            except Exception as e:
                logger.error(f"Service startup hook failed: {e}")

        return {"status": "registered", "service_id": service_id}

    async def deregister_service(self, service_id: str) -> Dict[str, Any]:
        """Deregister service with cleanup."""

        # Execute shutdown hook
        hooks = self.service_lifecycle_hooks.get(service_id, {})
        on_shutdown = hooks.get("on_shutdown")

        if on_shutdown:
            try:
                result = on_shutdown()
                if asyncio.iscoroutine(result):
                    await result
                logger.info(f"Service shutdown hook executed: {service_id}")
            except Exception as e:
                logger.error(f"Service shutdown hook failed: {e}")

        # Deregister from registry
        await self.api_manager.registry.deregister(service_id)

        # Emit service stopped event
        from event_router import Event, EventRoutingStrategy

        event = Event(
            id=f"svc_stop_{service_id}",
            event_type="service.stopped",
            source_service="infrastructure",
            payload={"service_id": service_id},
            correlation_id=service_id,
        )

        await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

        # Cleanup hooks
        del self.service_lifecycle_hooks[service_id]

        return {"status": "deregistered", "service_id": service_id}

    # ========================================================================
    # 💉 MICROSERVICE CODE INJECTION
    # ========================================================================

    async def inject_microservice_code(
        self,
        service_id: str,
        code: str,
        handler_name: str,
        security_level: str = "sandboxed",
    ) -> Dict[str, Any]:
        """Inject code into running microservice."""

        injected = await self.api_manager.code_injector.inject(
            service_id=service_id,
            code=code,
            handler_name=handler_name,
            security_level=security_level,
        )

        # Emit code injection event
        from event_router import Event, EventRoutingStrategy

        event = Event(
            id=f"code_inject_{injected.id}",
            event_type="code.injected",
            source_service="infrastructure",
            payload={
                "service_id": service_id,
                "injected_id": injected.id,
                "handler_name": handler_name,
                "security_level": security_level,
                "checksum": injected.checksum,
            },
            metadata={"execution_count": injected.execution_count},
        )

        await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

        return {
            "status": "injected",
            "injected_id": injected.id,
            "checksum": injected.checksum,
        }

    async def execute_injected_code(
        self,
        injected_id: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """Execute previously injected code."""

        try:
            result = await self.api_manager.code_injector.execute(
                injected_id,
                **kwargs,
            )

            # Emit code executed event
            from event_router import Event, EventRoutingStrategy

            event = Event(
                id=f"code_exec_{injected_id}",
                event_type="code.executed",
                source_service="infrastructure",
                payload={"injected_id": injected_id, "result": str(result)[:100]},
            )

            await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

            return {"status": "executed", "result": result}

        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return {"status": "failed", "error": str(e)}

    # ========================================================================
    # 🌐 MESH ROUTING & LOAD BALANCING
    # ========================================================================

    async def route_request_through_mesh(
        self,
        source_service: str,
        target_service: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Route request through service mesh."""

        result = await self.mesh.route_request(
            service_id=target_service,
            source_service=source_service,
            payload=payload,
        )

        # Record metric
        if result.get("status") == "success":
            response_time = result.get("response_time", 0)
            metrics = self.mesh.load_balancers[target_service].endpoint_stats[
                result.get("endpoint", "unknown")
            ]
            metrics["request_count"] += 1
        else:
            metrics = self.mesh.load_balancers[target_service].endpoint_stats.get(
                "error", {"request_count": 0, "error_count": 0}
            )
            metrics["error_count"] += 1

        return result

    # ========================================================================
    # 📨 MESSAGE & EVENT ROUTING
    # ========================================================================

    async def publish_message(
        self,
        source_service: str,
        message_type: str,
        payload: Dict[str, Any],
        target_service: Optional[str] = None,
        priority: str = "normal",
        ttl_seconds: int = 3600,
    ) -> Dict[str, Any]:
        """Publish message to bus."""

        from api_manager import Message, MessagePriority

        message = Message(
            source_service=source_service,
            target_service=target_service,
            message_type=message_type,
            payload=payload,
            priority=MessagePriority[priority.upper()],
            ttl_seconds=ttl_seconds,
        )

        await self.api_manager.message_bus.publish(message)

        return {"status": "published", "message_id": message.id}

    async def emit_event(
        self,
        source_service: str,
        event_type: str,
        payload: Dict[str, Any],
        routing_strategy: str = "broadcast",
        priority: int = 5,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Emit event with routing strategy."""

        from event_router import Event, EventRoutingStrategy

        event = Event(
            id=f"evt_{datetime.utcnow().timestamp()}",
            event_type=event_type,
            source_service=source_service,
            payload=payload,
            priority=priority,
            metadata=metadata or {},
        )

        strategy = EventRoutingStrategy[routing_strategy.upper()]

        result = await self.router.route_event(event, strategy)

        return {"status": "routed", "event_id": event.id, "routing": result}

    # ========================================================================
    # 🎯 TASK MANAGEMENT
    # ========================================================================

    async def submit_task(
        self,
        service_id: str,
        handler_name: str,
        params: Dict[str, Any] = None,
        priority: str = "normal",
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Submit async task."""

        from api_manager import Task, MessagePriority

        task = Task(
            service_id=service_id,
            handler_name=handler_name,
            params=params or {},
            priority=MessagePriority[priority.upper()],
            max_retries=max_retries,
        )

        task_id = await self.api_manager.task_router.submit_task(task)

        return {"status": "submitted", "task_id": task_id}

    async def execute_pending_tasks(self) -> Dict[str, Any]:
        """Process pending tasks."""

        executed = 0
        failed = 0

        while True:
            task = await self.api_manager.task_router.get_next_task()
            if not task:
                break

            try:
                await self.api_manager.task_router.execute_task(task)
                executed += 1

                # Emit task completion event
                from event_router import Event, EventRoutingStrategy

                event = Event(
                    id=f"task_complete_{task.id}",
                    event_type="task.completed",
                    source_service="infrastructure",
                    payload={"task_id": task.id, "service_id": task.service_id},
                )

                await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

            except Exception as e:
                failed += 1
                logger.error(f"Task execution failed: {e}")

        return {"executed": executed, "failed": failed}

    # ========================================================================
    # 🔐 API KEY MANAGEMENT
    # ========================================================================

    async def add_api_key(
        self,
        name: str,
        key: str,
        provider: str,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Add API key."""

        api_key = await self.api_manager.api_key_manager.add_key(
            name=name,
            key=key,
            provider=provider,
            metadata=metadata,
        )

        return {
            "status": "added",
            "name": api_key.name,
            "provider": api_key.provider,
        }

    async def rotate_api_key(self, name: str, new_key: str) -> Dict[str, Any]:
        """Rotate API key."""

        api_key = await self.api_manager.api_key_manager.rotate_key(name, new_key)

        return {"status": "rotated", "name": api_key.name}

    # ========================================================================
    # 📊 SYSTEM MONITORING
    # ========================================================================

    async def get_infrastructure_status(self) -> Dict[str, Any]:
        """Get complete infrastructure status."""

        api_manager_status = await self.api_manager.get_system_status()
        mesh_status = await self.mesh.get_mesh_status()
        router_stats = self.router.get_routing_stats()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "api_manager": api_manager_status,
            "service_mesh": mesh_status,
            "event_router": {
                "stats": router_stats,
                "event_history_size": len(self.router.event_history),
                "dlq_size": len(self.router.dead_letter_queue),
            },
            "lifecycle_hooks": {
                "services_with_hooks": len(self.service_lifecycle_hooks)
            },
        }

    def get_service_health(self, service_id: str) -> Dict[str, Any]:
        """Get health status of service."""

        service = self.service_lifecycle_hooks.get(service_id)
        if not service:
            return {"status": "unknown", "service_id": service_id}

        hook = service.get("on_health_check")

        try:
            if hook:
                health = hook()
                if asyncio.iscoroutine(health):
                    health = asyncio.run(health)
                return {
                    "status": "healthy",
                    "service_id": service_id,
                    "health": health,
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "service_id": service_id,
                "error": str(e),
            }

        return {"status": "unknown", "service_id": service_id}

    # ========================================================================
    # 🐛 DEBUGGING & OBSERVABILITY
    # ========================================================================

    def get_event_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent event history for debugging."""

        events = self.router.get_event_history(limit)
        return [asdict(e) for e in events]

    def get_dead_letter_queue(self) -> List[Dict[str, Any]]:
        """Get messages in dead letter queue."""

        dlq = self.router.dead_letter_queue
        return [asdict(dlm) for dlm in dlq]

    async def replay_dead_letter_queue(self) -> Dict[str, int]:
        """Replay all messages in dead letter queue."""

        return await self.router.replay_dead_letter_queue()
