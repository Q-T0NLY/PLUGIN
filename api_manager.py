#!/usr/bin/env python3
# ============================================================================
# 🚀 NEXUS ADVANCED API MANAGER v2.0
# ============================================================================
# Enterprise-grade API management with dynamic microservices, code injection,
# service mesh, message/event bus, task routing, and advanced lifecycle management.
# ============================================================================

import asyncio
import json
import uuid
import hashlib
import inspect
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable, Coroutine, Set
from datetime import datetime, timedelta
from pathlib import Path
import logging
import redis.asyncio as redis
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 📋 ENUMS & DOMAIN MODELS
# ============================================================================

class ServiceStatus(str, Enum):
    """Service lifecycle status."""
    CREATED = "created"
    REGISTERING = "registering"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    TERMINATING = "terminating"
    TERMINATED = "terminated"


class MessagePriority(str, Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    """System event types."""
    SERVICE_STARTED = "service.started"
    SERVICE_STOPPED = "service.stopped"
    SERVICE_HEALTH_CHECK = "service.health_check"
    MESSAGE_RECEIVED = "message.received"
    MESSAGE_ROUTED = "message.routed"
    TASK_SUBMITTED = "task.submitted"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    CODE_INJECTED = "code.injected"
    CODE_EXECUTED = "code.executed"


@dataclass
class APIKey:
    """API Key configuration."""
    name: str
    key: str
    provider: str  # openai, claude, deepseek, etc.
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_used(self):
        """Update last used timestamp."""
        self.last_used = datetime.utcnow()


@dataclass
class ServiceDescriptor:
    """Microservice descriptor for registration."""
    id: str
    name: str
    version: str
    namespace: str
    endpoints: Dict[str, str]  # path -> method mapping
    dependencies: List[str] = field(default_factory=list)
    health_check_url: Optional[str] = None
    max_retries: int = 3
    timeout_seconds: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Bus message for inter-service communication."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_service: str = ""
    target_service: Optional[str] = None
    message_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    ttl_seconds: int = 3600


@dataclass
class Task:
    """Async task for the task bus/router."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    service_id: str = ""
    handler_name: str = ""
    params: Dict[str, Any] = field(default_factory=dict)
    priority: MessagePriority = MessagePriority.NORMAL
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 60


@dataclass
class InjectedCode:
    """Dynamic code injection descriptor."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    service_id: str = ""
    code: str = ""
    handler_name: str = ""
    checksum: str = ""
    injected_at: datetime = field(default_factory=datetime.utcnow)
    execution_count: int = 0
    security_level: str = "sandboxed"  # isolated, sandboxed, trusted
    metadata: Dict[str, Any] = field(default_factory=dict)

    def compute_checksum(self):
        """Compute code checksum for verification."""
        self.checksum = hashlib.sha256(self.code.encode()).hexdigest()


# ============================================================================
# 🏗️ SERVICE REGISTRY
# ============================================================================

class ServiceRegistry:
    """Centralized service discovery and registration."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.local_services: Dict[str, ServiceDescriptor] = {}

    async def register(self, descriptor: ServiceDescriptor) -> None:
        """Register a microservice."""
        self.local_services[descriptor.id] = descriptor

        # Persist to Redis
        key = f"nexus:service:{descriptor.id}"
        await self.redis.setex(
            key,
            3600,  # 1 hour TTL
            json.dumps(asdict(descriptor), default=str),
        )

        logger.info(f"Service registered: {descriptor.name} ({descriptor.id})")

    async def deregister(self, service_id: str) -> None:
        """Deregister a microservice."""
        if service_id in self.local_services:
            del self.local_services[service_id]

        # Remove from Redis
        key = f"nexus:service:{service_id}"
        await self.redis.delete(key)

        logger.info(f"Service deregistered: {service_id}")

    async def get_service(self, service_id: str) -> Optional[ServiceDescriptor]:
        """Get service by ID."""
        if service_id in self.local_services:
            return self.local_services[service_id]

        # Try Redis
        key = f"nexus:service:{service_id}"
        data = await self.redis.get(key)
        if data:
            service_dict = json.loads(data)
            return ServiceDescriptor(**service_dict)

        return None

    async def find_service_by_name(self, name: str) -> Optional[ServiceDescriptor]:
        """Find service by name."""
        for service in self.local_services.values():
            if service.name == name:
                return service
        return None

    async def list_services(self) -> List[ServiceDescriptor]:
        """List all registered services."""
        return list(self.local_services.values())


# ============================================================================
# 📬 MESSAGE BUS
# ============================================================================

class MessageBus:
    """Pub/Sub message bus for inter-service communication."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.subscribers: Dict[str, Set[Callable]] = {}
        self.message_queue: List[Message] = []

    async def publish(self, message: Message) -> None:
        """Publish message to bus."""
        # Store in Redis
        key = f"nexus:message:{message.id}"
        await self.redis.setex(
            key,
            message.ttl_seconds,
            json.dumps(asdict(message), default=str),
        )

        # Publish to channel
        channel = f"nexus:messages:{message.message_type}"
        await self.redis.publish(channel, json.dumps(asdict(message), default=str))

        self.message_queue.append(message)
        logger.info(f"Message published: {message.id} ({message.message_type})")

    async def subscribe(
        self,
        message_type: str,
        handler: Callable[[Message], Coroutine],
    ) -> None:
        """Subscribe to message type."""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = set()

        self.subscribers[message_type].add(handler)
        logger.info(f"Subscribed to {message_type}")

    async def listen(self):
        """Listen for messages (blocking)."""
        pubsub = self.redis.pubsub()

        # Subscribe to all message channels
        await pubsub.psubscribe("nexus:messages:*")

        async for message in pubsub.listen():
            if message["type"] == "pmessage":
                try:
                    msg_data = json.loads(message["data"])
                    msg = Message(**msg_data)
                    await self._dispatch(msg)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

    async def _dispatch(self, message: Message) -> None:
        """Dispatch message to handlers."""
        handlers = self.subscribers.get(message.message_type, set())

        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Handler error: {e}")


# ============================================================================
# 🎯 TASK ROUTER & SCHEDULER
# ============================================================================

class TaskRouter:
    """Route and execute tasks with priority scheduling."""

    def __init__(self, redis_client: redis.Redis, service_registry: ServiceRegistry):
        self.redis = redis_client
        self.registry = service_registry
        self.task_queue: Dict[str, List[Task]] = {
            "critical": [],
            "high": [],
            "normal": [],
            "low": [],
        }
        self.handlers: Dict[str, Callable] = {}
        self.running_tasks: Dict[str, Task] = {}

    async def submit_task(self, task: Task) -> str:
        """Submit task to queue."""
        priority_queue = self.task_queue.get(task.priority.value, self.task_queue["normal"])
        priority_queue.append(task)

        # Store in Redis
        key = f"nexus:task:{task.id}"
        await self.redis.setex(
            key,
            task.timeout_seconds * 2,
            json.dumps(asdict(task), default=str),
        )

        logger.info(f"Task submitted: {task.id} ({task.handler_name})")
        return task.id

    async def get_next_task(self) -> Optional[Task]:
        """Get next task by priority."""
        for priority_level in ["critical", "high", "normal", "low"]:
            if self.task_queue[priority_level]:
                return self.task_queue[priority_level].pop(0)
        return None

    async def execute_task(self, task: Task) -> Any:
        """Execute a task."""
        task.status = "running"
        self.running_tasks[task.id] = task

        try:
            handler = self.handlers.get(task.handler_name)
            if not handler:
                raise ValueError(f"Handler not found: {task.handler_name}")

            # Execute with timeout
            result = await asyncio.wait_for(
                handler(**task.params),
                timeout=task.timeout_seconds,
            )

            task.status = "completed"
            task.result = result

            logger.info(f"Task completed: {task.id}")
            return result

        except Exception as e:
            task.retry_count += 1

            if task.retry_count < task.max_retries:
                task.status = "pending"
                await self.submit_task(task)
                logger.warning(f"Task retry: {task.id} (attempt {task.retry_count})")
            else:
                task.status = "failed"
                task.error = str(e)
                logger.error(f"Task failed: {task.id}: {e}")

        finally:
            del self.running_tasks[task.id]

    def register_handler(self, name: str, handler: Callable) -> None:
        """Register task handler."""
        self.handlers[name] = handler
        logger.info(f"Handler registered: {name}")


# ============================================================================
# 💉 CODE INJECTOR & SANDBOX
# ============================================================================

class CodeInjector:
    """Dynamic code injection with security sandboxing."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.injected_code: Dict[str, InjectedCode] = {}
        self.execution_globals: Dict[str, Any] = {}

    async def inject(
        self,
        service_id: str,
        code: str,
        handler_name: str,
        security_level: str = "sandboxed",
    ) -> InjectedCode:
        """Inject code into service."""
        injected = InjectedCode(
            service_id=service_id,
            code=code,
            handler_name=handler_name,
            security_level=security_level,
        )
        injected.compute_checksum()

        # Security validation
        if security_level == "sandboxed":
            await self._validate_sandbox_safety(code)

        # Store in Redis
        key = f"nexus:injected:{injected.id}"
        await self.redis.setex(
            key,
            86400,  # 24 hours
            json.dumps(asdict(injected), default=str),
        )

        self.injected_code[injected.id] = injected

        logger.info(
            f"Code injected into {service_id}: {injected.id} ({security_level})"
        )

        return injected

    async def execute(self, injected_id: str, **kwargs) -> Any:
        """Execute injected code."""
        injected = self.injected_code.get(injected_id)
        if not injected:
            raise ValueError(f"Injected code not found: {injected_id}")

        try:
            # Create safe execution environment
            safe_globals = {
                "asyncio": asyncio,
                "json": json,
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "dict": dict,
                    "list": list,
                },
            }

            # Execute code
            exec(injected.code, safe_globals)
            handler = safe_globals.get(injected.handler_name)

            if not handler:
                raise ValueError(f"Handler not found: {injected.handler_name}")

            result = handler(**kwargs)

            if inspect.iscoroutine(result):
                result = await result

            injected.execution_count += 1

            logger.info(f"Injected code executed: {injected_id}")
            return result

        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            raise

    async def _validate_sandbox_safety(self, code: str) -> None:
        """Validate code for sandbox execution."""
        dangerous_patterns = [
            "import os",
            "import subprocess",
            "exec(",
            "eval(",
            "__import__",
            "open(",
            "compile(",
        ]

        for pattern in dangerous_patterns:
            if pattern in code:
                raise ValueError(f"Dangerous pattern detected: {pattern}")

        logger.info("Code passed sandbox validation")


# ============================================================================
# 🔐 API KEY MANAGER
# ============================================================================

class APIKeyManager:
    """Manage API keys for external services."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.keys: Dict[str, APIKey] = {}

    async def add_key(
        self,
        name: str,
        key: str,
        provider: str,
        metadata: Dict[str, Any] = None,
    ) -> APIKey:
        """Add API key."""
        api_key = APIKey(
            name=name,
            key=key,
            provider=provider,
            metadata=metadata or {},
        )

        # Store securely in Redis
        key_data = f"nexus:api_key:{name}"
        await self.redis.setex(
            key_data,
            31536000,  # 1 year
            json.dumps(asdict(api_key), default=str),
        )

        self.keys[name] = api_key

        logger.info(f"API Key added: {name} ({provider})")
        return api_key

    async def get_key(self, name: str) -> Optional[APIKey]:
        """Get API key by name."""
        if name in self.keys:
            key = self.keys[name]
            key.mark_used()
            return key

        # Try Redis
        data = await self.redis.get(f"nexus:api_key:{name}")
        if data:
            key_dict = json.loads(data)
            api_key = APIKey(**key_dict)
            api_key.mark_used()
            return api_key

        return None

    async def rotate_key(self, name: str, new_key: str) -> APIKey:
        """Rotate API key."""
        old_key = await self.get_key(name)
        if not old_key:
            raise ValueError(f"Key not found: {name}")

        updated_key = APIKey(
            name=name,
            key=new_key,
            provider=old_key.provider,
            metadata=old_key.metadata,
        )

        await self.redis.setex(
            f"nexus:api_key:{name}",
            31536000,
            json.dumps(asdict(updated_key), default=str),
        )

        self.keys[name] = updated_key

        logger.info(f"API Key rotated: {name}")
        return updated_key


# ============================================================================
# 🌐 ADVANCED API MANAGER (MASTER)
# ============================================================================

class AdvancedAPIManager:
    """Master API Manager with all subsystems."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.registry: Optional[ServiceRegistry] = None
        self.message_bus: Optional[MessageBus] = None
        self.task_router: Optional[TaskRouter] = None
        self.code_injector: Optional[CodeInjector] = None
        self.api_key_manager: Optional[APIKeyManager] = None

    async def init(self) -> None:
        """Initialize all subsystems."""
        self.redis = await redis.from_url(self.redis_url, decode_responses=True)

        self.registry = ServiceRegistry(self.redis)
        self.message_bus = MessageBus(self.redis)
        self.code_injector = CodeInjector(self.redis)
        self.api_key_manager = APIKeyManager(self.redis)
        self.task_router = TaskRouter(self.redis, self.registry)

        logger.info("Advanced API Manager initialized")

    async def shutdown(self) -> None:
        """Shutdown all subsystems."""
        if self.redis:
            await self.redis.close()
        logger.info("Advanced API Manager shutdown")

    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        services = await self.registry.list_services()
        running_tasks = len(self.task_router.running_tasks)
        total_tasks_queued = sum(
            len(queue) for queue in self.task_router.task_queue.values()
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "services_registered": len(services),
            "tasks_running": running_tasks,
            "tasks_queued": total_tasks_queued,
            "injected_code_modules": len(self.code_injector.injected_code),
            "api_keys_stored": len(self.api_key_manager.keys),
            "services": [asdict(s) for s in services],
        }


# ============================================================================
# 🏭 SINGLETON INSTANCE
# ============================================================================

_manager: Optional[AdvancedAPIManager] = None


async def get_api_manager() -> AdvancedAPIManager:
    """Get or create singleton API Manager instance."""
    global _manager
    if _manager is None:
        _manager = AdvancedAPIManager()
        await _manager.init()
    return _manager
