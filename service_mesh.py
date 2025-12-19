#!/usr/bin/env python3
# ============================================================================
# 🌐 NEXUS SERVICE MESH v2.0
# ============================================================================
# Advanced service mesh with load balancing, circuit breaking, health checks,
# traffic routing, rate limiting, and comprehensive metrics.
# ============================================================================

import asyncio
import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class LoadBalancingStrategy(str, Enum):
    """Load balancing strategies."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    RANDOM = "random"
    WEIGHTED = "weighted"


@dataclass
class ServiceEndpoint:
    """Individual service endpoint."""
    id: str
    host: str
    port: int
    weight: int = 1
    active_connections: int = 0
    healthy: bool = True
    response_times: List[float] = field(default_factory=list)

    @property
    def avg_response_time(self) -> float:
        """Get average response time."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times[-100:]) / len(self.response_times[-100:])


@dataclass
class CircuitBreaker:
    """Circuit breaker for fault tolerance."""
    service_id: str
    failure_threshold: int = 5
    success_threshold: int = 2
    timeout_seconds: int = 60
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[float] = None

    def record_success(self) -> None:
        """Record successful call."""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info(f"Circuit closed for {self.service_id}")

    def record_failure(self) -> None:
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                logger.warning(f"Circuit opened for {self.service_id}")

        elif self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
            logger.warning(f"Circuit reopened for {self.service_id}")

    def can_attempt_request(self) -> bool:
        """Check if request can be attempted."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if self.last_failure_time is None:
                return False

            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                logger.info(f"Circuit half-open for {self.service_id}")
                return True

            return False

        # HALF_OPEN
        return True


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    requests_per_second: int = 100
    burst_size: int = 200
    window_seconds: int = 1


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.tokens = config.burst_size
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        """Check if request is allowed."""
        now = time.time()
        elapsed = now - self.last_refill

        # Refill tokens
        self.tokens = min(
            self.config.burst_size,
            self.tokens
            + elapsed * (self.config.requests_per_second / self.config.window_seconds),
        )
        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True

        return False


@dataclass
class TrafficPolicy:
    """Traffic routing policy."""
    name: str
    source_service: str
    destination_service: str
    routing_rules: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict[str, int] = field(default_factory=dict)
    timeout_seconds: int = 30
    circuit_breaker: Optional[CircuitBreaker] = None
    rate_limiter: Optional[RateLimiter] = None


# ============================================================================
# 🔄 LOAD BALANCER
# ============================================================================

class LoadBalancer:
    """Intelligent load balancer for service mesh."""

    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN):
        self.strategy = strategy
        self.current_index = 0
        self.endpoint_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"request_count": 0, "error_count": 0}
        )

    def select_endpoint(self, endpoints: List[ServiceEndpoint]) -> Optional[ServiceEndpoint]:
        """Select endpoint based on strategy."""
        healthy_endpoints = [e for e in endpoints if e.healthy]

        if not healthy_endpoints:
            return None

        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            endpoint = healthy_endpoints[self.current_index % len(healthy_endpoints)]
            self.current_index += 1
            return endpoint

        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return min(healthy_endpoints, key=lambda e: e.active_connections)

        elif self.strategy == LoadBalancingStrategy.WEIGHTED:
            total_weight = sum(e.weight for e in healthy_endpoints)
            if total_weight <= 0:
                return healthy_endpoints[0]

            rand_value = time.time() % total_weight
            cumulative = 0
            for endpoint in healthy_endpoints:
                cumulative += endpoint.weight
                if rand_value <= cumulative:
                    return endpoint

            return healthy_endpoints[-1]

        else:  # RANDOM
            import random
            return random.choice(healthy_endpoints)

    def record_request(
        self,
        endpoint_id: str,
        response_time: float,
        success: bool,
    ) -> None:
        """Record request metrics."""
        stats = self.endpoint_stats[endpoint_id]
        stats["request_count"] += 1
        if not success:
            stats["error_count"] += 1


# ============================================================================
# 🏥 HEALTH CHECKER
# ============================================================================

class HealthChecker:
    """Service health checking."""

    def __init__(self, check_interval_seconds: int = 10):
        self.check_interval_seconds = check_interval_seconds
        self.last_check_time: Dict[str, float] = {}

    async def check_endpoint_health(
        self,
        endpoint: ServiceEndpoint,
        health_check_url: Optional[str] = None,
    ) -> bool:
        """Check endpoint health."""
        try:
            # Simulate health check (in real implementation, make HTTP request)
            if health_check_url:
                # Mock implementation - would use aiohttp in production
                logger.info(f"Health check for {endpoint.id}: OK")
                return True

            # Default: assume healthy
            endpoint.healthy = True
            return True

        except Exception as e:
            logger.error(f"Health check failed for {endpoint.id}: {e}")
            endpoint.healthy = False
            return False

    async def monitor_endpoints(
        self,
        endpoints: List[ServiceEndpoint],
        health_check_url: Optional[str] = None,
    ) -> None:
        """Continuously monitor endpoint health."""
        while True:
            for endpoint in endpoints:
                now = time.time()
                last_check = self.last_check_time.get(endpoint.id, 0)

                if now - last_check >= self.check_interval_seconds:
                    await self.check_endpoint_health(endpoint, health_check_url)
                    self.last_check_time[endpoint.id] = now

            await asyncio.sleep(self.check_interval_seconds)


# ============================================================================
# 🌐 SERVICE MESH
# ============================================================================

class ServiceMesh:
    """Advanced service mesh with routing, load balancing, and fault tolerance."""

    def __init__(self):
        self.services: Dict[str, List[ServiceEndpoint]] = {}
        self.load_balancers: Dict[str, LoadBalancer] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.traffic_policies: Dict[str, TrafficPolicy] = {}
        self.health_checker = HealthChecker()
        self.active_connections: Dict[str, int] = defaultdict(int)

    def register_service(
        self,
        service_id: str,
        endpoints: List[ServiceEndpoint],
        strategy: LoadBalancingStrategy = LoadBalancingStrategy.ROUND_ROBIN,
    ) -> None:
        """Register service with endpoints."""
        self.services[service_id] = endpoints
        self.load_balancers[service_id] = LoadBalancer(strategy)
        self.circuit_breakers[service_id] = CircuitBreaker(service_id)

        logger.info(f"Service registered: {service_id} with {len(endpoints)} endpoints")

    def get_service_endpoint(self, service_id: str) -> Optional[ServiceEndpoint]:
        """Get next endpoint for service."""
        endpoints = self.services.get(service_id, [])
        if not endpoints:
            return None

        lb = self.load_balancers[service_id]
        return lb.select_endpoint(endpoints)

    async def route_request(
        self,
        service_id: str,
        source_service: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Route request through mesh."""
        # Get circuit breaker
        cb = self.circuit_breakers.get(service_id)

        if cb and not cb.can_attempt_request():
            return {"error": "Circuit breaker open", "status": "unavailable"}

        # Get endpoint
        endpoint = self.get_service_endpoint(service_id)
        if not endpoint:
            if cb:
                cb.record_failure()
            return {"error": "No healthy endpoints", "status": "unavailable"}

        # Check rate limits
        policy = self.traffic_policies.get(f"{source_service}→{service_id}")
        if policy and policy.rate_limiter:
            if not policy.rate_limiter.allow_request():
                return {"error": "Rate limit exceeded", "status": "rate_limited"}

        # Simulate request
        try:
            start_time = time.time()
            endpoint.active_connections += 1

            # Simulated async operation
            await asyncio.sleep(0.01)

            response_time = time.time() - start_time

            endpoint.active_connections -= 1
            endpoint.response_times.append(response_time)

            # Record success
            lb = self.load_balancers[service_id]
            lb.record_request(endpoint.id, response_time, True)

            if cb:
                cb.record_success()

            return {
                "status": "success",
                "endpoint": f"{endpoint.host}:{endpoint.port}",
                "response_time": response_time,
                "payload": payload,
            }

        except Exception as e:
            endpoint.active_connections -= 1

            if cb:
                cb.record_failure()

            logger.error(f"Request routing failed: {e}")
            return {"error": str(e), "status": "error"}

    def add_traffic_policy(self, policy: TrafficPolicy) -> None:
        """Add traffic routing policy."""
        key = f"{policy.source_service}→{policy.destination_service}"
        self.traffic_policies[key] = policy

        logger.info(f"Traffic policy added: {key}")

    async def get_mesh_status(self) -> Dict[str, Any]:
        """Get mesh status and metrics."""
        status = {
            "services": len(self.services),
            "endpoints": sum(len(eps) for eps in self.services.values()),
            "active_connections": sum(self.active_connections.values()),
            "circuit_breakers": {},
            "traffic_policies": len(self.traffic_policies),
        }

        for service_id, cb in self.circuit_breakers.items():
            status["circuit_breakers"][service_id] = {
                "state": cb.state.value,
                "failure_count": cb.failure_count,
                "success_count": cb.success_count,
            }

        return status


# ============================================================================
# 🎯 REQUEST ROUTER
# ============================================================================

class RequestRouter:
    """Advanced request router with retry logic and fallbacks."""

    def __init__(self, mesh: ServiceMesh):
        self.mesh = mesh

    async def route_with_retries(
        self,
        service_id: str,
        source_service: str,
        payload: Dict[str, Any],
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ) -> Dict[str, Any]:
        """Route request with exponential backoff retries."""
        last_error = None

        for attempt in range(max_retries):
            try:
                result = await self.mesh.route_request(
                    service_id,
                    source_service,
                    payload,
                )

                if result.get("status") == "success":
                    return result

                # Check if retriable
                if result.get("status") in ["rate_limited", "unavailable"]:
                    last_error = result
                    if attempt < max_retries - 1:
                        wait_time = (backoff_factor ** attempt)
                        logger.info(
                            f"Retry {attempt + 1}/{max_retries} after {wait_time}s"
                        )
                        await asyncio.sleep(wait_time)
                        continue

                return result

            except Exception as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_factor ** attempt)

        return {"error": last_error, "status": "failed", "attempts": max_retries}


# ============================================================================
# 📊 MESH METRICS
# ============================================================================

class MeshMetrics:
    """Mesh performance metrics."""

    def __init__(self):
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.latencies: Dict[str, List[float]] = defaultdict(list)
        self.start_time = time.time()

    def record_request(
        self,
        service_id: str,
        latency: float,
        success: bool,
    ) -> None:
        """Record request metric."""
        self.request_counts[service_id] += 1
        self.latencies[service_id].append(latency)

        if not success:
            self.error_counts[service_id] += 1

    def get_service_metrics(self, service_id: str) -> Dict[str, Any]:
        """Get metrics for service."""
        request_count = self.request_counts[service_id]
        error_count = self.error_counts[service_id]
        latencies = self.latencies[service_id]

        return {
            "service_id": service_id,
            "total_requests": request_count,
            "total_errors": error_count,
            "error_rate": error_count / request_count if request_count > 0 else 0,
            "avg_latency": sum(latencies) / len(latencies) if latencies else 0,
            "p50_latency": sorted(latencies)[len(latencies) // 2] if latencies else 0,
            "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
        }
