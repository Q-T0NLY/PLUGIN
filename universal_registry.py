"""
🏢 UNIVERSAL REGISTRY MANAGER
Complete enterprise registry with AI, search, relationships, and analytics
"""

import logging
import asyncio
import uuid
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum

from .database import EnterpriseDatabaseManager
from .search_engine import UniversalSearchEngine, SearchResult
from .relationships import AdvancedRelationshipManager, GraphNode, GraphEdge
from .analytics import AnalyticsEngine
from .ai_engine import AIInferenceEngine, Classification

logger = logging.getLogger("hyper_registry.universal_registry")

class RegistryCategory(Enum):
    """🏷️ All registry entry categories"""
    # AI Systems (9)
    AGENT = "agent"
    SERVICE = "service"
    ENGINE = "engine"
    MODEL = "model"
    SKILL = "skill"
    PLUGIN = "plugin"
    PROMPT = "prompt"
    EMBEDDING = "embedding"
    MEMORY = "memory"
    
    # Infrastructure (7)
    API = "api"
    INTEGRATION = "integration"
    COMPONENT = "component"
    RESOURCE = "resource"
    INFRASTRUCTURE = "infrastructure"
    PIPELINE = "pipeline"
    WEBHOOK = "webhook"
    
    # Data (5)
    DATASET = "dataset"
    KNOWLEDGE = "knowledge"
    SEARCH = "search"
    EVENT_SCHEMA = "event_schema"
    TASK_SCHEMA = "task_schema"
    
    # Business (2)
    WORKFLOW = "workflow"
    ORGANIZATION = "organization"
    
    # Other (3)
    TEMPLATE = "template"
    WIDGET = "widget"
    NOTIFICATION = "notification"

class RegistryStatus(Enum):
    """📊 Entry status lifecycle"""
    ACTIVE = "active"
    DRAFT = "draft"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    PENDING = "pending"

@dataclass
class UniversalRegistryEntry:
    """🏛️ Universal registry entry with 40+ fields"""
    entry_id: str
    category: RegistryCategory
    title: str
    description: str
    status: RegistryStatus = RegistryStatus.ACTIVE
    owner_id: Optional[str] = None
    created_by: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    accessed_at: Optional[str] = None
    
    # Content & Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    
    # AI/Classification
    ai_category: Optional[str] = None
    ai_confidence: float = 0.0
    embedding: Optional[List[float]] = None
    summary: Optional[str] = None
    
    # Relationships
    related_entries: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    
    # Security & Compliance
    security_context: Dict[str, Any] = field(default_factory=dict)
    compliance_status: Dict[str, Any] = field(default_factory=dict)
    encryption_enabled: bool = True
    
    # Performance & Analytics
    access_count: int = 0
    last_accessed_by: Optional[str] = None
    version: str = "1.0.0"
    checksum: Optional[str] = None


class UniversalRegistryManager:
    """
    🏢 UNIVERSAL REGISTRY MANAGER
    Complete enterprise registry orchestration
    """
    
    def __init__(self, db_manager: EnterpriseDatabaseManager):
        self.db = db_manager
        self.search_engine = UniversalSearchEngine(db_manager)
        self.relationship_manager = AdvancedRelationshipManager(db_manager)
        self.analytics_engine = AnalyticsEngine()
        self.ai_engine = AIInferenceEngine()
        
        self.entries: Dict[str, UniversalRegistryEntry] = {}
        self.entry_count = 0
        
        logger.info("🏢 Universal Registry Manager initialized")
    
    async def register_entry(self, entry_data: Dict[str, Any]) -> str:
        """
        📝 Register new entry with AI enhancement
        """
        try:
            import time
            start = time.time()
            
            entry_id = entry_data.get("entry_id") or str(uuid.uuid4())
            
            # AI Classification
            classification = await self.ai_engine.classify_entry(
                entry_id=entry_id,
                title=entry_data.get("title", ""),
                description=entry_data.get("description", ""),
                metadata=entry_data.get("metadata")
            )
            
            # Generate embedding
            text = f"{entry_data.get('title', '')} {entry_data.get('description', '')}"
            embedding = await self.ai_engine.generate_embedding(entry_id, text)
            
            # Generate tags
            tags = await self.ai_engine.suggest_tags(
                entry_id,
                entry_data.get("title", ""),
                entry_data.get("description", "")
            )
            
            # Create entry
            category_str = entry_data.get("category", "component")
            try:
                category = RegistryCategory[category_str.upper()]
            except KeyError:
                category = RegistryCategory.COMPONENT
            
            entry = UniversalRegistryEntry(
                entry_id=entry_id,
                category=category,
                title=entry_data.get("title", "Unknown"),
                description=entry_data.get("description", ""),
                status=RegistryStatus.ACTIVE,
                owner_id=entry_data.get("owner_id"),
                metadata=entry_data.get("metadata", {}),
                tags=tags,
                ai_category=classification.primary_category,
                ai_confidence=classification.confidence,
                embedding=embedding.vector,
                summary=await self.ai_engine.summarize_entry(
                    entry_data.get("title", ""),
                    entry_data.get("description", "")
                )
            )
            
            self.entries[entry_id] = entry
            self.entry_count += 1
            
            # Record metrics
            duration = (time.time() - start) * 1000
            await self.analytics_engine.record_metric("registry.register_entry", 1)
            await self.analytics_engine.track_operation("register_entry", duration, success=True)
            
            logger.info(f"✅ Entry registered: {entry_id} ({category.value})")
            return entry_id
            
        except Exception as e:
            logger.error(f"❌ Entry registration failed: {e}")
            await self.analytics_engine.track_operation("register_entry", 0, success=False)
            raise
    
    async def get_entry(self, entry_id: str) -> Optional[UniversalRegistryEntry]:
        """
        🔍 Retrieve entry with access tracking
        """
        try:
            if entry_id in self.entries:
                entry = self.entries[entry_id]
                entry.accessed_at = datetime.utcnow().isoformat()
                entry.access_count += 1
                
                await self.analytics_engine.record_metric("registry.get_entry", 1)
                return entry
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Entry retrieval failed: {e}")
            return None
    
    async def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """
        ✏️ Update entry with validation
        """
        try:
            if entry_id not in self.entries:
                return False
            
            entry = self.entries[entry_id]
            
            # Update fields
            for key, value in updates.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            
            entry.updated_at = datetime.utcnow().isoformat()
            
            await self.analytics_engine.record_metric("registry.update_entry", 1)
            logger.info(f"✏️ Entry updated: {entry_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Entry update failed: {e}")
            return False
    
    async def delete_entry(self, entry_id: str) -> bool:
        """
        🗑️ Delete entry
        """
        try:
            if entry_id in self.entries:
                del self.entries[entry_id]
                await self.analytics_engine.record_metric("registry.delete_entry", 1)
                logger.info(f"🗑️ Entry deleted: {entry_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Entry deletion failed: {e}")
            return False
    
    async def search_entries(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[SearchResult]:
        """
        🔍 Search entries with hybrid search
        """
        try:
            results = await self.search_engine.hybrid_search(
                query=query,
                filters=filters,
                limit=limit
            )
            
            await self.analytics_engine.record_metric("registry.search_entries", len(results))
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    async def create_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        🔗 Create relationship between entries
        """
        try:
            # Validate entries exist
            if source_id not in self.entries or target_id not in self.entries:
                logger.warning(f"⚠️ One or both entries not found for relationship")
                return ""
            
            # Create edge
            edge = GraphEdge(
                source_id=source_id,
                target_id=target_id,
                relationship_type=rel_type,
                metadata=metadata or {}
            )
            
            await self.relationship_manager.add_edge(edge)
            
            # Update entry relationships
            source_entry = self.entries[source_id]
            target_entry = self.entries[target_id]
            
            if target_id not in source_entry.related_entries:
                source_entry.related_entries.append(target_id)
            
            if source_id not in target_entry.related_entries:
                target_entry.related_entries.append(source_id)
            
            await self.analytics_engine.record_metric("registry.create_relationship", 1)
            logger.info(f"🔗 Relationship created: {source_id} --[{rel_type}]--> {target_id}")
            
            return f"{source_id}_{target_id}_{rel_type}"
            
        except Exception as e:
            logger.error(f"❌ Relationship creation failed: {e}")
            return ""
    
    async def get_relationships(
        self,
        entry_id: str,
        rel_type: Optional[str] = None,
        direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """
        🔗 Get entry relationships
        """
        try:
            relationships = []
            
            if entry_id not in self.entries:
                return relationships
            
            entry = self.entries[entry_id]
            
            # Return related entries
            for related_id in entry.related_entries:
                if related_id in self.entries:
                    related_entry = self.entries[related_id]
                    relationships.append({
                        "entry_id": related_id,
                        "title": related_entry.title,
                        "category": related_entry.category.value,
                        "status": related_entry.status.value
                    })
            
            await self.analytics_engine.record_metric("registry.get_relationships", len(relationships))
            return relationships
            
        except Exception as e:
            logger.error(f"❌ Relationship retrieval failed: {e}")
            return []
    
    async def bulk_register_entries(self, entries: List[Dict[str, Any]]) -> List[str]:
        """
        📦 Bulk register entries
        """
        try:
            entry_ids = []
            
            for entry_data in entries:
                try:
                    entry_id = await self.register_entry(entry_data)
                    entry_ids.append(entry_id)
                except Exception as e:
                    logger.error(f"❌ Bulk entry failed: {e}")
                    continue
            
            await self.analytics_engine.record_metric("registry.bulk_register", len(entry_ids))
            logger.info(f"📦 Bulk registered {len(entry_ids)} entries")
            return entry_ids
            
        except Exception as e:
            logger.error(f"❌ Bulk registration failed: {e}")
            return []
    
    async def export_registry(self, format: str = "json") -> str:
        """
        💾 Export registry
        """
        try:
            if format == "json":
                data = {
                    "entries": [asdict(entry) for entry in self.entries.values()],
                    "total": len(self.entries),
                    "timestamp": datetime.utcnow().isoformat()
                }
                return json.dumps(data, indent=2)
            
            elif format == "csv":
                lines = ["id,category,title,status,owner_id,created_at"]
                for entry in self.entries.values():
                    lines.append(
                        f"{entry.entry_id},{entry.category.value},{entry.title},"
                        f"{entry.status.value},{entry.owner_id},{entry.created_at}"
                    )
                return "\n".join(lines)
            
            return ""
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            return ""
    
    async def import_registry(self, data: str, format: str = "json") -> int:
        """
        📥 Import registry
        """
        try:
            if format == "json":
                parsed = json.loads(data)
                entries = parsed.get("entries", [])
                return len(await self.bulk_register_entries(entries))
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Import failed: {e}")
            return 0
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        📊 Get registry statistics
        """
        try:
            category_counts = {}
            status_counts = {}
            
            for entry in self.entries.values():
                cat = entry.category.value
                status = entry.status.value
                
                category_counts[cat] = category_counts.get(cat, 0) + 1
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "total_entries": len(self.entries),
                "categories": category_counts,
                "status_distribution": status_counts,
                "analytics": self.analytics_engine.get_registry_analytics(),
                "ai_stats": self.ai_engine.get_ai_engine_stats(),
                "graph_stats": self.relationship_manager.get_graph_stats(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Stats retrieval failed: {e}")
            return {}
