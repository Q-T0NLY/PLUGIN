"""
🌐 REGISTRY API GATEWAY
RESTful and WebSocket API for registry access and management
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger("hyper_registry.api_gateway")

class RegistryAPIGateway:
    """
    🌐 REGISTRY API GATEWAY
    RESTful endpoints for registry operations
    """
    
    def __init__(self, registry_manager, analytics_engine):
        self.registry = registry_manager
        self.analytics = analytics_engine
        self.request_count = 0
        self.websocket_connections = set()
        
        logger.info("🌐 Registry API Gateway initialized")
    
    # ============== REGISTRY OPERATIONS ==============
    
    async def register_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST /v1/registry/entries
        Register new entry
        """
        try:
            self.request_count += 1
            
            logger.info(f"📝 Registering entry: {entry_data.get('title', 'unknown')}")
            
            # Validate entry
            if not self._validate_entry(entry_data):
                return {"error": "Invalid entry data"}
            
            # Register with manager
            entry_id = await self.registry.register_entry(entry_data)
            
            # Track metrics
            await self.analytics.record_metric("api.register_entry", 1)
            
            return {
                "success": True,
                "entry_id": entry_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Registration failed: {e}")
            await self.analytics.create_alert("registration_error", str(e), "error")
            return {"error": str(e)}
    
    async def get_entry(self, entry_id: str) -> Dict[str, Any]:
        """
        GET /v1/registry/entries/{entry_id}
        Retrieve entry
        """
        try:
            self.request_count += 1
            
            logger.info(f"🔍 Retrieving entry: {entry_id}")
            
            entry = await self.registry.get_entry(entry_id)
            
            if not entry:
                return {"error": "Entry not found"}
            
            await self.analytics.record_metric("api.get_entry", 1)
            
            return {
                "success": True,
                "entry": entry,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Retrieval failed: {e}")
            return {"error": str(e)}
    
    async def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        PUT /v1/registry/entries/{entry_id}
        Update entry
        """
        try:
            self.request_count += 1
            
            logger.info(f"✏️ Updating entry: {entry_id}")
            
            # Validate updates
            if not self._validate_entry(updates, partial=True):
                return {"error": "Invalid update data"}
            
            # Update entry
            result = await self.registry.update_entry(entry_id, updates)
            
            await self.analytics.record_metric("api.update_entry", 1)
            
            return {
                "success": True,
                "entry_id": entry_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Update failed: {e}")
            return {"error": str(e)}
    
    async def delete_entry(self, entry_id: str) -> Dict[str, Any]:
        """
        DELETE /v1/registry/entries/{entry_id}
        Delete entry
        """
        try:
            self.request_count += 1
            
            logger.info(f"🗑️ Deleting entry: {entry_id}")
            
            await self.registry.delete_entry(entry_id)
            
            await self.analytics.record_metric("api.delete_entry", 1)
            
            return {
                "success": True,
                "entry_id": entry_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Deletion failed: {e}")
            return {"error": str(e)}
    
    # ============== SEARCH OPERATIONS ==============
    
    async def search_entries(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        GET /v1/registry/search
        Search registry entries
        """
        try:
            self.request_count += 1
            
            logger.info(f"🔍 Searching: '{query}' with {len(filters or {})} filters")
            
            # Execute search
            results = await self.registry.search_entries(
                query=query,
                filters=filters,
                limit=limit
            )
            
            await self.analytics.record_metric("api.search_entries", 1)
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return {"error": str(e)}
    
    # ============== RELATIONSHIP OPERATIONS ==============
    
    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        POST /v1/registry/relationships
        Create relationship
        """
        try:
            self.request_count += 1
            
            logger.info(f"🔗 Creating relationship: {source_id} --[{rel_type}]--> {target_id}")
            
            rel_id = await self.registry.create_relationship(
                source_id=source_id,
                target_id=target_id,
                rel_type=rel_type,
                metadata=metadata
            )
            
            await self.analytics.record_metric("api.create_relationship", 1)
            
            return {
                "success": True,
                "relationship_id": rel_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Relationship creation failed: {e}")
            return {"error": str(e)}
    
    async def get_relationships(
        self,
        entry_id: str,
        rel_type: Optional[str] = None,
        direction: str = "both"
    ) -> Dict[str, Any]:
        """
        GET /v1/registry/entries/{entry_id}/relationships
        Get entry relationships
        """
        try:
            self.request_count += 1
            
            logger.info(f"🔗 Getting relationships for {entry_id} (direction: {direction})")
            
            relationships = await self.registry.get_relationships(
                entry_id=entry_id,
                rel_type=rel_type,
                direction=direction
            )
            
            await self.analytics.record_metric("api.get_relationships", 1)
            
            return {
                "success": True,
                "entry_id": entry_id,
                "relationships": relationships,
                "count": len(relationships),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Relationship retrieval failed: {e}")
            return {"error": str(e)}
    
    # ============== ANALYTICS OPERATIONS ==============
    
    async def get_analytics(self) -> Dict[str, Any]:
        """
        GET /v1/registry/analytics
        Get system analytics
        """
        try:
            self.request_count += 1
            
            logger.info("📊 Retrieving analytics")
            
            return {
                "success": True,
                "analytics": self.analytics.get_registry_analytics(),
                "performance": self.analytics.get_performance_summary(),
                "api_requests": self.request_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Analytics retrieval failed: {e}")
            return {"error": str(e)}
    
    async def get_health(self) -> Dict[str, Any]:
        """
        GET /v1/registry/health
        Get system health
        """
        try:
            logger.info("❤️ Health check")
            
            return {
                "success": True,
                "status": "operational",
                "version": "1.0.0",
                "uptime_seconds": 0,  # Would calculate from start time
                "requests": self.request_count,
                "active_connections": len(self.websocket_connections),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            return {"error": str(e)}
    
    # ============== BULK OPERATIONS ==============
    
    async def bulk_register(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        POST /v1/registry/bulk/register
        Bulk register entries
        """
        try:
            self.request_count += 1
            
            logger.info(f"📦 Bulk registering {len(entries)} entries")
            
            entry_ids = await self.registry.bulk_register_entries(entries)
            
            await self.analytics.record_metric("api.bulk_register", len(entries))
            
            return {
                "success": True,
                "count": len(entry_ids),
                "entry_ids": entry_ids,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Bulk registration failed: {e}")
            return {"error": str(e)}
    
    async def bulk_export(self, format: str = "json") -> Dict[str, Any]:
        """
        GET /v1/registry/bulk/export
        Export registry
        """
        try:
            self.request_count += 1
            
            logger.info(f"💾 Exporting registry as {format}")
            
            export_data = await self.registry.export_registry(format=format)
            
            await self.analytics.record_metric("api.bulk_export", 1)
            
            return {
                "success": True,
                "format": format,
                "data": export_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return {"error": str(e)}
    
    # ============== VALIDATION ==============
    
    def _validate_entry(self, entry: Dict[str, Any], partial: bool = False) -> bool:
        """
        ✅ Validate entry data
        """
        try:
            required_fields = ["title", "category"] if not partial else []
            
            for field in required_fields:
                if field not in entry or not entry[field]:
                    logger.warning(f"❌ Missing required field: {field}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return False
    
    # ============== STATISTICS ==============
    
    def get_gateway_stats(self) -> Dict[str, Any]:
        """
        📊 Get gateway statistics
        """
        return {
            "total_requests": self.request_count,
            "active_websockets": len(self.websocket_connections),
            "timestamp": datetime.utcnow().isoformat()
        }
