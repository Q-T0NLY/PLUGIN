"""
🌌 UNIVERSAL HYPER REGISTRY v2.0
Advanced Dynamic Hyper-Meta Registry System
Central hub for all system components as sub-registries
"""

from typing import Any, Dict, List, Optional, Callable, Set
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import json
from abc import ABC, abstractmethod
import threading
from collections import defaultdict


class RegistryType(Enum):
    """Registry sub-categories for modular organization"""
    API = "api"
    MODELS = "models"
    MODULES = "modules"
    DATABASES = "databases"
    SERVICES = "services"
    MESSAGES = "messages"
    TASKS = "tasks"
    EVENTS = "events"
    INTEGRATIONS = "integrations"
    WEBHOOKS = "webhooks"
    TOOLS = "tools"
    ENDPOINTS = "endpoints"
    FEATURES = "features"
    ENGINES = "engines"
    PLUGINS = "plugins"
    DEPENDENCIES = "dependencies"
    PATCHES = "patches"
    MODALITY = "modality"
    EMBEDDINGS = "embeddings"
    DEPLOYERS = "deployers"
    PROMPT_LIBRARY = "prompt_library"
    CONTAINERS = "containers"
    GRAPHS = "graphs"
    INTELLIGENCE = "intelligence"
    VECTORS = "vectors"
    DATASETS = "datasets"
    PROJECTS = "projects"
    SCORING = "scoring"
    ROUTERS = "routers"
    ORCHESTRATORS = "orchestrators"
    SERVICE_MESH = "service_mesh"
    FEATURE_FLAGS = "feature_flags"
    PERMISSIONS = "permissions"
    THEMES = "themes"
    LAYOUTS = "layouts"
    ANIMATIONS = "animations"


class ServiceStatus(Enum):
    """Status of registered services"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    INITIALIZING = "initializing"
    DEGRADED = "degraded"
    ERROR = "error"
    LOCKED = "locked"


@dataclass
class RegistryEntry:
    """Individual registry entry with metadata"""
    id: str
    type: RegistryType
    name: str
    version: str
    status: ServiceStatus = ServiceStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: Set[str] = field(default_factory=set)
    dependencies_mapping: Dict[str, List[str]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
            "dependencies": list(self.dependencies),
            "dependencies_mapping": self.dependencies_mapping,
            "tags": self.tags,
            "config": self.config,
        }


@dataclass
class ToggleableService:
    """Service that can be toggled on/off with configuration"""
    service_id: str
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    
    def toggle(self):
        """Toggle service state"""
        self.enabled = not self.enabled


class SubRegistry:
    """Individual sub-registry for each component type"""
    
    def __init__(self, registry_type: RegistryType):
        self.registry_type = registry_type
        self.entries: Dict[str, RegistryEntry] = {}
        self.lock = threading.RLock()
    
    def register(self, entry: RegistryEntry) -> bool:
        """Register new entry"""
        with self.lock:
            if entry.id in self.entries:
                return False
            self.entries[entry.id] = entry
            return True
    
    def unregister(self, entry_id: str) -> bool:
        """Unregister entry"""
        with self.lock:
            if entry_id in self.entries:
                del self.entries[entry_id]
                return True
            return False
    
    def get(self, entry_id: str) -> Optional[RegistryEntry]:
        """Get entry by ID"""
        with self.lock:
            return self.entries.get(entry_id)
    
    def list_all(self) -> List[RegistryEntry]:
        """List all entries"""
        with self.lock:
            return list(self.entries.values())
    
    def get_by_tag(self, tag: str) -> List[RegistryEntry]:
        """Get entries by tag"""
        with self.lock:
            return [e for e in self.entries.values() if tag in e.tags]


class UniversalHyperRegistry:
    """
    Central Universal Hyper Registry
    Manages all sub-registries and component ecosystems
    """
    
    def __init__(self):
        self.sub_registries: Dict[RegistryType, SubRegistry] = {
            rt: SubRegistry(rt) for rt in RegistryType
        }
        self.toggleable_services: Dict[str, ToggleableService] = {}
        self.lock = threading.RLock()
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        self.metadata = {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_entries": 0,
        }
    
    def register(self, entry: RegistryEntry) -> bool:
        """Register entry in appropriate sub-registry"""
        sub_reg = self.sub_registries.get(entry.type)
        if not sub_reg:
            return False
        
        success = sub_reg.register(entry)
        if success:
            self._emit_event("registry:entry_registered", entry)
            self.metadata["last_updated"] = datetime.now().isoformat()
            self.metadata["total_entries"] = self._count_entries()
        
        return success
    
    def unregister(self, registry_type: RegistryType, entry_id: str) -> bool:
        """Unregister entry from sub-registry"""
        sub_reg = self.sub_registries.get(registry_type)
        if not sub_reg:
            return False
        
        success = sub_reg.unregister(entry_id)
        if success:
            self._emit_event("registry:entry_unregistered", {"type": registry_type, "id": entry_id})
            self.metadata["last_updated"] = datetime.now().isoformat()
            self.metadata["total_entries"] = self._count_entries()
        
        return success
    
    def get_entry(self, registry_type: RegistryType, entry_id: str) -> Optional[RegistryEntry]:
        """Get entry from sub-registry"""
        sub_reg = self.sub_registries.get(registry_type)
        return sub_reg.get(entry_id) if sub_reg else None
    
    def get_sub_registry(self, registry_type: RegistryType) -> Optional[SubRegistry]:
        """Get entire sub-registry"""
        return self.sub_registries.get(registry_type)
    
    def register_toggleable_service(self, service: ToggleableService):
        """Register a toggleable service (e.g., context-generative-dag-rag-fusion)"""
        with self.lock:
            self.toggleable_services[service.service_id] = service
            self._emit_event("registry:toggleable_service_registered", service)
    
    def toggle_service(self, service_id: str) -> bool:
        """Toggle a toggleable service"""
        with self.lock:
            service = self.toggleable_services.get(service_id)
            if service:
                service.toggle()
                self._emit_event("registry:service_toggled", {"id": service_id, "enabled": service.enabled})
                return True
            return False
    
    def is_service_enabled(self, service_id: str) -> bool:
        """Check if service is enabled"""
        service = self.toggleable_services.get(service_id)
        return service.enabled if service else False
    
    def get_service_config(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get service configuration"""
        service = self.toggleable_services.get(service_id)
        return service.config if service else None
    
    def on(self, event_type: str, handler: Callable):
        """Subscribe to registry events"""
        self.event_handlers[event_type].append(handler)
    
    def _emit_event(self, event_type: str, data: Any):
        """Emit event to subscribers"""
        for handler in self.event_handlers.get(event_type, []):
            try:
                handler(data)
            except Exception as e:
                print(f"Error in event handler: {e}")
    
    def _count_entries(self) -> int:
        """Count total entries across all sub-registries"""
        return sum(len(sr.entries) for sr in self.sub_registries.values())
    
    def export_snapshot(self) -> Dict[str, Any]:
        """Export complete registry snapshot"""
        snapshot = {
            "metadata": self.metadata,
            "sub_registries": {},
            "toggleable_services": {},
        }
        
        for rt, sub_reg in self.sub_registries.items():
            snapshot["sub_registries"][rt.value] = [
                entry.to_dict() for entry in sub_reg.list_all()
            ]
        
        for service_id, service in self.toggleable_services.items():
            snapshot["toggleable_services"][service_id] = {
                "name": service.name,
                "enabled": service.enabled,
                "config": service.config,
            }
        
        return snapshot
    
    def import_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """Import registry snapshot"""
        try:
            for rt_str, entries_data in snapshot.get("sub_registries", {}).items():
                rt = RegistryType(rt_str)
                for entry_data in entries_data:
                    entry = RegistryEntry(
                        id=entry_data["id"],
                        type=rt,
                        name=entry_data["name"],
                        version=entry_data["version"],
                        status=ServiceStatus(entry_data["status"]),
                        created_at=datetime.fromisoformat(entry_data["created_at"]),
                        updated_at=datetime.fromisoformat(entry_data["updated_at"]),
                        metadata=entry_data.get("metadata", {}),
                        dependencies=set(entry_data.get("dependencies", [])),
                        dependencies_mapping=entry_data.get("dependencies_mapping", {}),
                        tags=entry_data.get("tags", []),
                        config=entry_data.get("config", {}),
                    )
                    self.register(entry)
            
            return True
        except Exception as e:
            print(f"Error importing snapshot: {e}")
            return False


# Global instance
global_registry = UniversalHyperRegistry()


def get_global_registry() -> UniversalHyperRegistry:
    """Get global registry instance"""
    return global_registry
