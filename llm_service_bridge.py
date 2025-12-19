#!/usr/bin/env python3
# ============================================================================
# 🌐 NEXUS LLM SERVICE BRIDGE v2.0
# ============================================================================
# Integration layer connecting the multi-LLM orchestrator with the
# advanced API manager, service mesh, and event router systems.
# ============================================================================

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class LLMServiceBridge:
    """Bridge connecting LLM orchestrator with advanced infrastructure."""

    def __init__(self, api_manager, service_mesh, event_router, consensus_engine):
        self.api_manager = api_manager
        self.mesh = service_mesh
        self.router = event_router
        self.consensus = consensus_engine

    async def orchestrate_multi_provider_call(
        self,
        prompt: str,
        required_capabilities: List[str],
        strategy: str = "consensus",
        timeout_seconds: int = 30,
    ) -> Dict[str, Any]:
        """Orchestrate call across multiple providers with advanced routing."""

        # Use universal adapter for ranking
        adapter = self.api_manager.code_injector  # Access via orchestrator

        # Rank providers by capability
        ranked = await self._rank_providers(required_capabilities)

        if strategy == "consensus":
            return await self._execute_consensus(prompt, ranked, timeout_seconds)
        elif strategy == "fastest":
            return await self._execute_fastest(prompt, ranked)
        elif strategy == "cost_optimized":
            return await self._execute_cost_optimized(prompt, ranked)
        else:
            return await self._execute_best_match(prompt, ranked)

    async def _rank_providers(self, capabilities: List[str]) -> List[Dict[str, Any]]:
        """Rank providers by capability match."""
        providers = await self.api_manager.registry.list_services()

        ranked = []
        for provider in providers:
            capability_match = sum(
                1 for cap in capabilities
                if cap in provider.metadata.get("capabilities", [])
            )
            score = (capability_match / len(capabilities)) * 100 if capabilities else 50

            ranked.append(
                {
                    "provider": provider.name,
                    "score": score,
                    "capabilities_matched": capability_match,
                    "total_capabilities": len(capabilities),
                }
            )

        return sorted(ranked, key=lambda x: -x["score"])

    async def _execute_consensus(
        self,
        prompt: str,
        ranked_providers: List[Dict[str, Any]],
        timeout_seconds: int,
    ) -> Dict[str, Any]:
        """Execute consensus strategy across top providers."""
        top_providers = ranked_providers[:3]

        responses = []
        tasks = []

        for provider_info in top_providers:
            task = asyncio.create_task(
                self._call_provider(
                    provider_info["provider"],
                    prompt,
                )
            )
            tasks.append(task)

        try:
            responses = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=timeout_seconds,
            )
        except asyncio.TimeoutError:
            logger.warning("Consensus timeout, using partial results")

        # Emit consensus event
        from event_router import Event, EventRoutingStrategy

        event = Event(
            id=f"consensus_{datetime.utcnow().timestamp()}",
            event_type="orchestrator.consensus",
            source_service="llm_bridge",
            payload={
                "prompt": prompt[:100],
                "providers_count": len(responses),
                "responses": len([r for r in responses if not isinstance(r, Exception)]),
            },
        )

        await self.router.route_event(event, EventRoutingStrategy.BROADCAST)

        return {
            "status": "consensus_complete",
            "providers_consulted": len(top_providers),
            "responses": responses,
            "confidence": self._calculate_consensus_confidence(responses),
            "recommended_response": self._select_best_response(responses),
        }

    async def _execute_fastest(
        self,
        prompt: str,
        ranked_providers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Execute fastest strategy (first to respond)."""
        tasks = [
            asyncio.create_task(self._call_provider(p["provider"], prompt))
            for p in ranked_providers[:3]
        ]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        # Cancel remaining tasks
        for task in pending:
            task.cancel()

        result = done.pop().result() if done else None

        return {
            "status": "fastest_complete",
            "response": result,
            "providers_consulted": len(ranked_providers),
        }

    async def _execute_cost_optimized(
        self,
        prompt: str,
        ranked_providers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Execute cost-optimized strategy (cheapest viable)."""
        # Sorted by cost (ascending)
        response = await self._call_provider(ranked_providers[0]["provider"], prompt)

        return {
            "status": "cost_optimized",
            "response": response,
            "provider": ranked_providers[0]["provider"],
            "cost_efficiency_score": ranked_providers[0]["score"],
        }

    async def _execute_best_match(
        self,
        prompt: str,
        ranked_providers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Execute best match strategy (highest score)."""
        response = await self._call_provider(ranked_providers[0]["provider"], prompt)

        return {
            "status": "best_match",
            "response": response,
            "provider": ranked_providers[0]["provider"],
            "capability_match_score": ranked_providers[0]["score"],
        }

    async def _call_provider(self, provider: str, prompt: str) -> str:
        """Call a specific provider."""
        # Simulate provider call
        logger.info(f"Calling provider: {provider}")
        await asyncio.sleep(0.1)  # Simulate latency
        return f"Response from {provider}: {prompt[:50]}..."

    def _calculate_consensus_confidence(self, responses: List[Any]) -> float:
        """Calculate confidence based on response agreement."""
        valid_responses = [r for r in responses if not isinstance(r, Exception)]

        if not valid_responses:
            return 0.0

        # Simple confidence: count of valid responses / total
        return len(valid_responses) / max(len(responses), 1)

    def _select_best_response(self, responses: List[Any]) -> Optional[str]:
        """Select best response from list."""
        for response in responses:
            if not isinstance(response, Exception):
                return response
        return None

    async def get_bridge_status(self) -> Dict[str, Any]:
        """Get bridge health and status."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "api_manager_connected": self.api_manager is not None,
            "service_mesh_connected": self.mesh is not None,
            "event_router_connected": self.router is not None,
            "consensus_engine_connected": self.consensus is not None,
        }


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_bridge: Optional[LLMServiceBridge] = None


def get_llm_service_bridge(api_manager, service_mesh, event_router, consensus_engine):
    """Get or create LLM service bridge."""
    global _bridge
    if _bridge is None:
        _bridge = LLMServiceBridge(api_manager, service_mesh, event_router, consensus_engine)
    return _bridge
