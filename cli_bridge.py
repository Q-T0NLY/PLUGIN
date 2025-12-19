"""
Zsh CLI to Hyper Registry Backend Bridge
Connects shell commands to REST API
"""
import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class RegistryClient:
    """HTTP client for Hyper Registry API"""
    base_url: str = "http://localhost:8000"
    timeout: int = 30
    session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        
        async with self.session.request(
            method, url, json=data, params=params,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as resp:
            return await resp.json()

    # ====================================================================
    # REGISTRY OPERATIONS
    # ====================================================================

    async def health_check(self) -> Dict:
        """Check API health"""
        return await self._request("GET", "/health")

    async def register_entry(
        self,
        category: str,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        owner_id: Optional[str] = None
    ) -> Dict:
        """Register new entry"""
        data = {
            "category": category,
            "title": title,
            "description": description,
            "metadata": metadata or {},
            "tags": tags or [],
            "owner_id": owner_id
        }
        return await self._request("POST", "/api/v1/registry/entries", data=data)

    async def get_entry(self, entry_id: str) -> Dict:
        """Get entry details"""
        return await self._request("GET", f"/api/v1/registry/entries/{entry_id}")

    async def update_entry(
        self,
        entry_id: str,
        **kwargs
    ) -> Dict:
        """Update entry"""
        return await self._request("PUT", f"/api/v1/registry/entries/{entry_id}", data=kwargs)

    async def delete_entry(self, entry_id: str) -> Dict:
        """Delete entry"""
        return await self._request("DELETE", f"/api/v1/registry/entries/{entry_id}")

    # ====================================================================
    # SEARCH OPERATIONS
    # ====================================================================

    async def search(
        self,
        query: str,
        search_type: str = "hybrid",
        filters: Optional[Dict] = None,
        limit: int = 10
    ) -> Dict:
        """Search entries"""
        data = {
            "query": query,
            "search_type": search_type,
            "filters": filters or {},
            "limit": limit
        }
        return await self._request("POST", "/api/v1/search", data=data)

    async def search_autocomplete(self, query: str) -> Dict:
        """Get autocomplete suggestions"""
        return await self._request("GET", "/api/v1/search/autocomplete", params={"q": query})

    async def get_trending(self) -> Dict:
        """Get trending searches"""
        return await self._request("GET", "/api/v1/search/trending")

    # ====================================================================
    # RELATIONSHIP OPERATIONS
    # ====================================================================

    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Create relationship"""
        data = {
            "source_id": source_id,
            "target_id": target_id,
            "relationship_type": relationship_type,
            "metadata": metadata or {}
        }
        return await self._request("POST", "/api/v1/relationships", data=data)

    async def get_relationships(
        self,
        entry_id: str,
        rel_type: Optional[str] = None
    ) -> Dict:
        """Get relationships for entry"""
        params = {"rel_type": rel_type} if rel_type else {}
        return await self._request(
            "GET",
            f"/api/v1/relationships/{entry_id}",
            params=params
        )

    async def analyze_graph(self, entry_ids: List[str]) -> Dict:
        """Analyze relationship graph"""
        return await self._request("POST", "/api/v1/relationships/graph", data=entry_ids)

    # ====================================================================
    # ANALYTICS OPERATIONS
    # ====================================================================

    async def get_metrics(self, metric_type: str = "all") -> Dict:
        """Get system metrics"""
        return await self._request(
            "GET",
            "/api/v1/analytics/metrics",
            params={"metric_type": metric_type}
        )

    async def get_registry_stats(self) -> Dict:
        """Get registry statistics"""
        return await self._request("GET", "/api/v1/analytics/registry-stats")

    async def get_performance_analytics(self) -> Dict:
        """Get performance analytics"""
        return await self._request("GET", "/api/v1/analytics/performance")

    # ====================================================================
    # BULK OPERATIONS
    # ====================================================================

    async def bulk_register(self, entries: List[Dict]) -> Dict:
        """Register multiple entries"""
        entry_objects = [
            {
                "category": e.get("category"),
                "title": e.get("title"),
                "description": e.get("description"),
                "metadata": e.get("metadata", {}),
                "tags": e.get("tags", []),
                "owner_id": e.get("owner_id")
            }
            for e in entries
        ]
        return await self._request("POST", "/api/v1/bulk/register", data=entry_objects)

    async def export_registry(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        format: str = "json"
    ) -> Dict:
        """Export registry"""
        params = {
            "category": category,
            "status": status,
            "format": format
        }
        return await self._request("GET", "/api/v1/bulk/export", params=params)

    # ====================================================================
    # AI OPERATIONS
    # ====================================================================

    async def classify(self, text: str) -> Dict:
        """Classify text"""
        return await self._request("POST", "/api/v1/ai/classify", data=text)

    async def suggest_tags(self, entry_id: str) -> Dict:
        """Get suggested tags"""
        return await self._request("POST", "/api/v1/ai/suggest-tags", data=entry_id)


# ============================================================================
# CLI INTEGRATION FUNCTIONS
# ============================================================================

class RegistryCLIBridge:
    """Bridge between Zsh CLI and Registry backend"""

    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.client = None

    async def init(self):
        """Initialize client"""
        self.client = RegistryClient(base_url=self.api_url)
        self.client.__enter__ = self.client.__aenter__
        self.client.__exit__ = self.client.__aexit__
        self.client.session = aiohttp.ClientSession()
        return self

    async def close(self):
        """Close client"""
        if self.client and self.client.session:
            await self.client.session.close()

    async def register_agent(self, name: str, description: str, **kwargs):
        """Register an AI agent"""
        return await self.client.register_entry(
            category="agent",
            title=name,
            description=description,
            **kwargs
        )

    async def register_service(self, name: str, description: str, **kwargs):
        """Register a service"""
        return await self.client.register_entry(
            category="service",
            title=name,
            description=description,
            **kwargs
        )

    async def register_workflow(self, name: str, description: str, **kwargs):
        """Register a workflow"""
        return await self.client.register_entry(
            category="workflow",
            title=name,
            description=description,
            **kwargs
        )

    async def register_model(self, name: str, description: str, **kwargs):
        """Register a model"""
        return await self.client.register_entry(
            category="model",
            title=name,
            description=description,
            **kwargs
        )

    async def quick_search(self, query: str, limit: int = 5):
        """Quick search"""
        return await self.client.search(query, limit=limit)

    async def get_status(self):
        """Get system status"""
        return await self.client.health_check()

    async def get_all_stats(self):
        """Get all statistics"""
        return {
            "metrics": await self.client.get_metrics(),
            "registry_stats": await self.client.get_registry_stats(),
            "performance": await self.client.get_performance_analytics()
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage"""
    bridge = RegistryCLIBridge()
    await bridge.init()

    try:
        # Check health
        print("📡 Checking API health...")
        health = await bridge.get_status()
        print(f"✓ Status: {health['status']}")

        # Register an agent
        print("\n📝 Registering new agent...")
        agent_result = await bridge.register_agent(
            name="DataProcessor",
            description="Processes and transforms data",
            tags=["production", "critical"]
        )
        print(f"✓ Registered: {agent_result['entry_id']}")

        # Search
        print("\n🔍 Searching for 'processor'...")
        search_result = await bridge.quick_search("processor")
        print(f"✓ Found {search_result['total_results']} results")

        # Get stats
        print("\n📊 Getting system statistics...")
        stats = await bridge.get_all_stats()
        print(f"✓ Total entries: {stats['registry_stats']['total_entries']}")

    finally:
        await bridge.close()


if __name__ == "__main__":
    asyncio.run(main())
