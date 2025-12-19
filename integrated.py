"""
🏢 INTEGRATED HYPER UNIVERSAL REGISTRY
Complete enterprise system with all components unified
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json

# Import all core components
from .core.database import EnterpriseDatabaseManager
from .core.universal_registry import UniversalRegistryManager, RegistryCategory, RegistryStatus
from .core.search_engine import UniversalSearchEngine
from .core.relationships import AdvancedRelationshipManager
from .core.analytics import AnalyticsEngine
from .core.ai_engine import AIInferenceEngine
from .api_gateway import RegistryAPIGateway

logger = logging.getLogger("hyper_registry.integrated")

class SystemStatus(Enum):
    """System operational status"""
    BOOTING = "🔵 booting"
    OPERATIONAL = "🟢 operational"
    DEGRADED = "🟠 degraded"
    MAINTENANCE = "🟡 maintenance"
    ERROR = "🔴 error"
    SHUTTING_DOWN = "🟣 shutting_down"

class HyperRegistryIntegrated:
    """
    🏢 INTEGRATED HYPER UNIVERSAL REGISTRY
    Complete enterprise system with all components unified
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.system_id = str(uuid.uuid4())
        self.status = SystemStatus.BOOTING
        self.start_time = datetime.utcnow()
        
        # Initialize configuration
        self.config = config or self._load_default_config()
        
        # Core components
        self.db_manager: Optional[EnterpriseDatabaseManager] = None
        self.registry_manager: Optional[UniversalRegistryManager] = None
        self.api_gateway: Optional[RegistryAPIGateway] = None
        self.analytics_engine: Optional[AnalyticsEngine] = None
        
        logger.info(f"🏢 Integrated Registry initialized - System ID: {self.system_id}")
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default enterprise configuration"""
        import os
        
        return {
            "database_url": os.getenv(
                "HYPER_DATABASE_URL",
                "postgresql://hyper:secure@localhost:5432/hyper_registry"
            ),
            "api_port": int(os.getenv("HYPER_API_PORT", "8000")),
            "api_host": os.getenv("HYPER_API_HOST", "0.0.0.0"),
            "environment": os.getenv("HYPER_ENV", "production"),
            "log_level": os.getenv("HYPER_LOG_LEVEL", "INFO"),
            "enable_analytics": os.getenv("HYPER_ANALYTICS", "true").lower() == "true",
            "enable_monitoring": os.getenv("HYPER_MONITORING", "true").lower() == "true"
        }
    
    async def start(self):
        """
        🚀 Start the complete integrated registry system
        """
        logger.info("🚀 Starting Integrated Hyper Registry System...")
        
        try:
            # Initialize database
            logger.info("💾 Initializing database manager...")
            self.db_manager = EnterpriseDatabaseManager(
                self.config.get("database_url")
            )
            await self.db_manager.start()
            logger.info("✅ Database manager initialized")
            
            # Initialize analytics
            logger.info("📊 Initializing analytics engine...")
            self.analytics_engine = AnalyticsEngine()
            logger.info("✅ Analytics engine initialized")
            
            # Initialize universal registry manager
            logger.info("📝 Initializing universal registry manager...")
            self.registry_manager = UniversalRegistryManager(self.db_manager)
            logger.info("✅ Universal registry manager initialized")
            
            # Initialize API gateway
            logger.info("🌐 Initializing API gateway...")
            self.api_gateway = RegistryAPIGateway(
                self.registry_manager,
                self.analytics_engine
            )
            logger.info("✅ API gateway initialized")
            
            # Update status
            self.status = SystemStatus.OPERATIONAL
            
            await self.analytics_engine.record_metric("system.startup", 1)
            
            logger.info("🟢 SYSTEM OPERATIONAL")
            logger.info(f"📊 Status: {self.status.value}")
            logger.info(f"🆔 System ID: {self.system_id}")
            
            return True
            
        except Exception as e:
            self.status = SystemStatus.ERROR
            logger.error(f"❌ System startup failed: {e}", exc_info=True)
            await self.analytics_engine.create_alert(
                "system_startup_error",
                str(e),
                severity="critical"
            )
            raise
    
    async def shutdown(self):
        """
        🛑 Graceful system shutdown
        """
        logger.info("🛑 Initiating graceful shutdown...")
        self.status = SystemStatus.SHUTTING_DOWN
        
        try:
            # Shutdown in order
            if self.api_gateway:
                logger.info("Shutting down API gateway...")
                # Gateway shutdown logic
            
            if self.registry_manager:
                logger.info("Shutting down registry manager...")
                # Registry shutdown logic
            
            if self.db_manager:
                logger.info("Shutting down database...")
                await self.db_manager.shutdown()
            
            logger.info("✅ System shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Shutdown error: {e}", exc_info=True)
    
    # ========== REGISTRY OPERATIONS ==========
    
    async def register_entry(self, entry_data: Dict[str, Any]) -> str:
        """Register new entry"""
        return await self.registry_manager.register_entry(entry_data)
    
    async def get_entry(self, entry_id: str) -> Optional[Any]:
        """Get entry by ID"""
        return await self.registry_manager.get_entry(entry_id)
    
    async def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update entry"""
        return await self.registry_manager.update_entry(entry_id, updates)
    
    async def delete_entry(self, entry_id: str) -> bool:
        """Delete entry"""
        return await self.registry_manager.delete_entry(entry_id)
    
    async def search_entries(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Any]:
        """Search entries"""
        return await self.registry_manager.search_entries(query, filters, limit)
    
    # ========== RELATIONSHIP OPERATIONS ==========
    
    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create relationship"""
        return await self.registry_manager.create_relationship(
            source_id, target_id, rel_type, metadata
        )
    
    async def get_relationships(
        self,
        entry_id: str,
        rel_type: Optional[str] = None,
        direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """Get relationships"""
        return await self.registry_manager.get_relationships(
            entry_id, rel_type, direction
        )
    
    # ========== BULK OPERATIONS ==========
    
    async def bulk_register(self, entries: List[Dict[str, Any]]) -> List[str]:
        """Bulk register entries"""
        return await self.registry_manager.bulk_register_entries(entries)
    
    async def export_registry(self, format: str = "json") -> str:
        """Export registry"""
        return await self.registry_manager.export_registry(format)
    
    async def import_registry(self, data: str, format: str = "json") -> int:
        """Import registry"""
        return await self.registry_manager.import_registry(data, format)
    
    # ========== ANALYTICS ==========
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return self.registry_manager.get_registry_stats()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get complete system status"""
        return {
            "system_id": self.system_id,
            "status": self.status.value,
            "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "registry_stats": self.get_registry_stats(),
            "api_stats": self.api_gateway.get_gateway_stats() if self.api_gateway else {},
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # ========== CONVENIENCE METHODS ==========
    
    async def register_agent(self, agent_data: Dict[str, Any]) -> str:
        """Register AI agent"""
        agent_data["category"] = "agent"
        return await self.register_entry(agent_data)
    
    async def register_service(self, service_data: Dict[str, Any]) -> str:
        """Register microservice"""
        service_data["category"] = "service"
        return await self.register_entry(service_data)
    
    async def register_model(self, model_data: Dict[str, Any]) -> str:
        """Register LLM/ML model"""
        model_data["category"] = "model"
        return await self.register_entry(model_data)
    
    async def register_workflow(self, workflow_data: Dict[str, Any]) -> str:
        """Register workflow"""
        workflow_data["category"] = "workflow"
        return await self.register_entry(workflow_data)
    
    async def register_dataset(self, dataset_data: Dict[str, Any]) -> str:
        """Register dataset"""
        dataset_data["category"] = "dataset"
        return await self.register_entry(dataset_data)
    
    async def register_api(self, api_data: Dict[str, Any]) -> str:
        """Register API endpoint"""
        api_data["category"] = "api"
        return await self.register_entry(api_data)


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

_global_registry: Optional[HyperRegistryIntegrated] = None

def get_hyper_registry(config: Optional[Dict[str, Any]] = None) -> HyperRegistryIntegrated:
    """Get or create global registry instance"""
    global _global_registry
    
    if _global_registry is None:
        _global_registry = HyperRegistryIntegrated(config)
    
    return _global_registry


# ============================================================================
# DEMO/TEST
# ============================================================================

async def demo():
    """Demo the integrated registry system"""
    
    registry = get_hyper_registry()
    await registry.start()
    
    try:
        # Register various entries
        print("\n📝 Registering entries...")
        
        agent_id = await registry.register_agent({
            "title": "Advanced Reasoning Agent",
            "description": "Multi-step reasoning with validation",
            "owner_id": "user123"
        })
        print(f"✅ Agent registered: {agent_id}")
        
        service_id = await registry.register_service({
            "title": "Data Pipeline Service",
            "description": "ETL and data processing",
            "owner_id": "user123"
        })
        print(f"✅ Service registered: {service_id}")
        
        # Create relationship
        print("\n🔗 Creating relationships...")
        rel_id = await registry.create_relationship(
            agent_id, service_id, "calls"
        )
        print(f"✅ Relationship created: {rel_id}")
        
        # Search
        print("\n🔍 Searching...")
        results = await registry.search_entries("agent", limit=5)
        print(f"✅ Found {len(results)} results")
        
        # Get stats
        print("\n📊 System Status:")
        status = registry.get_system_status()
        print(json.dumps(status, indent=2))
        
    finally:
        await registry.shutdown()


if __name__ == "__main__":
    asyncio.run(demo())
