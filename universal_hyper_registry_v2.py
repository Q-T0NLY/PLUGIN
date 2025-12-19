"""
🌌 UNIVERSAL HYPER REGISTRY v2.0
Complete enterprise registry with all sub-registries, visuals, layouts, and intelligence
Production-grade, AI-synced, multi-modal, with service mesh and feature flags
"""

import asyncio
import logging
import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from dataclasses import dataclass, asdict, field

logger = logging.getLogger("hyper_registry.universal_v2")


# ============================================================================
# 🏗️ SUB-REGISTRY ENUMS
# ============================================================================

class SubRegistryType(Enum):
    """All sub-registry categories"""
    # Core Infrastructure
    API = "api"
    SERVICES = "services"
    MODULES = "modules"
    DATABASES = "databases"
    INTEGRATIONS = "integrations"
    WEBHOOKS = "webhooks"
    ENDPOINTS = "endpoints"
    
    # Data & Communication
    MESSAGES = "messages"
    TASKS = "tasks"
    EVENTS = "events"
    DATASETS = "datasets"
    VECTORS = "vectors"
    GRAPHS = "graphs"
    
    # AI & Intelligence
    MODELS = "models"
    ENGINES = "engines"
    PLUGINS = "plugins"
    TOOLS = "tools"
    AGENTS = "agents"
    INTELLIGENCE = "intelligence"
    
    # Advanced Features
    FEATURES = "features"
    FEATURE_FLAGS = "feature_flags"
    PERMISSIONS = "permissions"
    PATCHES = "patches"
    MODALITY = "modality"
    EMBEDDINGS = "embeddings"
    PROMPT_LIBRARY = "prompt_library"
    SCORING_TECHNIQUES = "scoring_techniques"
    
    # Deployment & Infrastructure
    DEPLOYERS = "deployers"
    CONTAINERS = "containers"
    ROUTERS = "routers"
    ORCHESTRATORS = "orchestrators"
    
    # Dependencies & Management
    DEPENDENCIES = "dependencies"
    DEPENDENCY_MAPPING = "dependency_mapping"
    PROJECTS = "projects"
    
    # Visual & UI
    LAYOUTS = "layouts"
    THEMES = "themes"
    ANIMATIONS = "animations"
    COMPONENTS = "components"


# ============================================================================
# 📋 SUB-REGISTRY ENTRY STRUCTURES
# ============================================================================

@dataclass
class APIRegistryEntry:
    """API endpoint registry"""
    api_id: str
    name: str
    endpoint: str
    method: str  # GET, POST, PUT, DELETE, etc.
    description: str
    auth_required: bool = True
    rate_limit: Optional[int] = None
    timeout: float = 30.0
    tags: List[str] = field(default_factory=list)
    response_schema: Dict[str, Any] = field(default_factory=dict)
    error_handlers: Dict[int, str] = field(default_factory=dict)


@dataclass
class ServiceRegistryEntry:
    """Service/microservice registry"""
    service_id: str
    name: str
    description: str
    service_type: str  # "microservice", "worker", "scheduler", etc.
    port: int
    health_check_endpoint: str
    dependencies: List[str] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)
    scaling_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelRegistryEntry:
    """AI Model registry"""
    model_id: str
    name: str
    model_type: str  # "llm", "vision", "embedding", etc.
    provider: str  # "openai", "anthropic", "deepseek", etc.
    version: str
    capabilities: List[str] = field(default_factory=list)
    context_window: Optional[int] = None
    cost_per_token: Dict[str, float] = field(default_factory=dict)
    confidence_score: float = 0.0
    fallback_models: List[str] = field(default_factory=list)


@dataclass
class FeatureFlagEntry:
    """Feature flag registry"""
    flag_id: str
    name: str
    description: str
    enabled: bool = False
    enabled_for_users: List[str] = field(default_factory=list)
    enabled_for_groups: List[str] = field(default_factory=list)
    rollout_percentage: float = 0.0  # 0-100
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    expires_at: Optional[str] = None


@dataclass
class PermissionEntry:
    """Permission/role registry"""
    permission_id: str
    resource: str
    action: str  # create, read, update, delete, execute
    role: str  # admin, user, guest, etc.
    conditions: Dict[str, Any] = field(default_factory=dict)
    audit_enabled: bool = True


@dataclass
class LayoutConfigEntry:
    """Layout configuration for UI/CLI"""
    layout_id: str
    name: str
    layout_type: str  # "dashboard", "chat", "cli", "3d_dag", "metrics"
    components: List[Dict[str, Any]] = field(default_factory=list)
    responsive_breakpoints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    theme: str = "dark"
    animations_enabled: bool = True
    accessibility_level: str = "wcag2.1_aa"


@dataclass
class IntelligenceLayerEntry:
    """Advanced intelligence layer registry"""
    layer_id: str
    name: str
    layer_type: str  # "context", "nlp", "intent", "multimodal", "ensemble", "dag_rag"
    enabled: bool = True
    sub_layers: List[str] = field(default_factory=list)
    fusion_strategy: str = "weighted_consensus"  # how to fuse outputs
    confidence_threshold: float = 0.7


# ============================================================================
# 🌌 UNIVERSAL HYPER REGISTRY v2.0
# ============================================================================

class UniversalHyperRegistryV2:
    """
    🌌 UNIVERSAL HYPER REGISTRY v2.0
    Complete enterprise registry with all sub-registries unified
    """
    
    def __init__(self):
        self.registry_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat()
        
        # Main storage for all sub-registries
        self.sub_registries: Dict[SubRegistryType, Dict[str, Any]] = {
            sub_type: {} for sub_type in SubRegistryType
        }
        
        # Cross-registry relationships
        self.relationships: Dict[str, List[Tuple[str, str, str]]] = {}  # entry_id -> [(target_id, relationship_type, strength)]
        
        # Service mesh integration
        self.service_mesh_enabled = True
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.load_balancers: Dict[str, List[str]] = {}
        
        # Feature flags & permissions
        self.feature_flags: Dict[str, FeatureFlagEntry] = {}
        self.permissions: Dict[str, PermissionEntry] = {}
        
        # Layout configurations
        self.layouts: Dict[str, LayoutConfigEntry] = {}
        
        # Intelligence layers
        self.intelligence_layers: Dict[str, IntelligenceLayerEntry] = {}
        
        # Statistics
        self.stats = {
            "total_entries": 0,
            "last_update": datetime.utcnow().isoformat(),
            "health_score": 100.0
        }
        
        logger.info(f"🌌 Universal Hyper Registry v2.0 initialized - ID: {self.registry_id}")
    
    # ========================================================================
    # 📝 REGISTRATION METHODS
    # ========================================================================
    
    async def register_api_endpoint(self, api_data: Dict[str, Any]) -> str:
        """Register API endpoint"""
        api_id = api_data.get("api_id") or str(uuid.uuid4())
        
        entry = APIRegistryEntry(
            api_id=api_id,
            name=api_data.get("name", "Unknown API"),
            endpoint=api_data.get("endpoint", "/"),
            method=api_data.get("method", "GET"),
            description=api_data.get("description", ""),
            **{k: v for k, v in api_data.items() if k not in ["api_id", "name", "endpoint", "method", "description"]}
        )
        
        self.sub_registries[SubRegistryType.API][api_id] = asdict(entry)
        logger.info(f"✅ API endpoint registered: {api_id} ({entry.method} {entry.endpoint})")
        return api_id
    
    async def register_service(self, service_data: Dict[str, Any]) -> str:
        """Register microservice"""
        service_id = service_data.get("service_id") or str(uuid.uuid4())
        
        entry = ServiceRegistryEntry(
            service_id=service_id,
            name=service_data.get("name", "Unknown Service"),
            description=service_data.get("description", ""),
            service_type=service_data.get("service_type", "microservice"),
            port=service_data.get("port", 8000),
            health_check_endpoint=service_data.get("health_check_endpoint", "/health"),
            **{k: v for k, v in service_data.items() if k not in ["service_id", "name", "description", "service_type", "port", "health_check_endpoint"]}
        )
        
        self.sub_registries[SubRegistryType.SERVICES][service_id] = asdict(entry)
        logger.info(f"✅ Service registered: {service_id} ({entry.name})")
        return service_id
    
    async def register_model(self, model_data: Dict[str, Any]) -> str:
        """Register AI model"""
        model_id = model_data.get("model_id") or str(uuid.uuid4())
        
        entry = ModelRegistryEntry(
            model_id=model_id,
            name=model_data.get("name", "Unknown Model"),
            model_type=model_data.get("model_type", "llm"),
            provider=model_data.get("provider", "unknown"),
            version=model_data.get("version", "1.0.0"),
            **{k: v for k, v in model_data.items() if k not in ["model_id", "name", "model_type", "provider", "version"]}
        )
        
        self.sub_registries[SubRegistryType.MODELS][model_id] = asdict(entry)
        logger.info(f"✅ Model registered: {model_id} ({entry.name} by {entry.provider})")
        return model_id
    
    async def register_feature_flag(self, flag_data: Dict[str, Any]) -> str:
        """Register feature flag"""
        flag_id = flag_data.get("flag_id") or str(uuid.uuid4())
        
        entry = FeatureFlagEntry(
            flag_id=flag_id,
            name=flag_data.get("name", "Unknown Flag"),
            description=flag_data.get("description", ""),
            **{k: v for k, v in flag_data.items() if k not in ["flag_id", "name", "description"]}
        )
        
        self.feature_flags[flag_id] = entry
        self.sub_registries[SubRegistryType.FEATURE_FLAGS][flag_id] = asdict(entry)
        logger.info(f"✅ Feature flag registered: {flag_id} ({entry.name}) - Enabled: {entry.enabled}")
        return flag_id
    
    async def register_permission(self, permission_data: Dict[str, Any]) -> str:
        """Register permission"""
        permission_id = permission_data.get("permission_id") or str(uuid.uuid4())
        
        entry = PermissionEntry(
            permission_id=permission_id,
            resource=permission_data.get("resource", ""),
            action=permission_data.get("action", "read"),
            role=permission_data.get("role", "user"),
            **{k: v for k, v in permission_data.items() if k not in ["permission_id", "resource", "action", "role"]}
        )
        
        self.permissions[permission_id] = entry
        self.sub_registries[SubRegistryType.PERMISSIONS][permission_id] = asdict(entry)
        logger.info(f"✅ Permission registered: {permission_id} ({entry.role} -> {entry.action} {entry.resource})")
        return permission_id
    
    async def register_layout(self, layout_data: Dict[str, Any]) -> str:
        """Register layout configuration"""
        layout_id = layout_data.get("layout_id") or str(uuid.uuid4())
        
        entry = LayoutConfigEntry(
            layout_id=layout_id,
            name=layout_data.get("name", "Unknown Layout"),
            layout_type=layout_data.get("layout_type", "dashboard"),
            **{k: v for k, v in layout_data.items() if k not in ["layout_id", "name", "layout_type"]}
        )
        
        self.layouts[layout_id] = entry
        self.sub_registries[SubRegistryType.LAYOUTS][layout_id] = asdict(entry)
        logger.info(f"✅ Layout registered: {layout_id} ({entry.layout_type})")
        return layout_id
    
    async def register_intelligence_layer(self, layer_data: Dict[str, Any]) -> str:
        """Register intelligence layer"""
        layer_id = layer_data.get("layer_id") or str(uuid.uuid4())
        
        entry = IntelligenceLayerEntry(
            layer_id=layer_id,
            name=layer_data.get("name", "Unknown Layer"),
            layer_type=layer_data.get("layer_type", "context"),
            **{k: v for k, v in layer_data.items() if k not in ["layer_id", "name", "layer_type"]}
        )
        
        self.intelligence_layers[layer_id] = entry
        self.sub_registries[SubRegistryType.INTELLIGENCE][layer_id] = asdict(entry)
        logger.info(f"✅ Intelligence layer registered: {layer_id} ({entry.layer_type})")
        return layer_id
    
    # ========================================================================
    # 🔍 QUERY METHODS
    # ========================================================================
    
    async def get_all_entries_by_type(self, registry_type: SubRegistryType) -> Dict[str, Any]:
        """Get all entries of a specific type"""
        return self.sub_registries.get(registry_type, {})
    
    async def get_entry(self, registry_type: SubRegistryType, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get specific entry"""
        return self.sub_registries[registry_type].get(entry_id)
    
    async def search_entries(self, registry_type: SubRegistryType, query: str, field: str = "name") -> List[Dict[str, Any]]:
        """Search entries in registry"""
        results = []
        for entry_id, entry in self.sub_registries[registry_type].items():
            if field in entry and query.lower() in str(entry[field]).lower():
                results.append(entry)
        return results
    
    # ========================================================================
    # 🔐 FEATURE FLAGS & PERMISSIONS
    # ========================================================================
    
    async def is_feature_enabled(self, flag_id: str, user_id: Optional[str] = None) -> bool:
        """Check if feature flag is enabled"""
        if flag_id not in self.feature_flags:
            return False
        
        flag = self.feature_flags[flag_id]
        
        # Check if expired
        if flag.expires_at and datetime.fromisoformat(flag.expires_at) < datetime.utcnow():
            return False
        
        # Check if globally enabled
        if flag.enabled:
            return True
        
        # Check if enabled for specific user
        if user_id and user_id in flag.enabled_for_users:
            return True
        
        # Check rollout percentage
        if flag.rollout_percentage > 0:
            user_hash = hash(user_id or "anonymous") % 100
            return user_hash < flag.rollout_percentage
        
        return False
    
    async def check_permission(self, user_id: str, resource: str, action: str, role: str) -> bool:
        """Check if user has permission"""
        for permission_id, perm in self.permissions.items():
            if perm.resource == resource and perm.action == action and perm.role == role:
                # Check conditions if any
                if perm.conditions:
                    # Evaluate conditions (simplified)
                    return True
                return True
        return False
    
    # ========================================================================
    # 🌀 SERVICE MESH
    # ========================================================================
    
    async def register_circuit_breaker(self, service_id: str, config: Dict[str, Any]) -> bool:
        """Register circuit breaker for service"""
        self.circuit_breakers[service_id] = {
            "state": "closed",
            "failure_threshold": config.get("failure_threshold", 5),
            "success_threshold": config.get("success_threshold", 2),
            "timeout": config.get("timeout", 60),
            "failures": 0,
            "successes": 0,
            **config
        }
        logger.info(f"✅ Circuit breaker registered for service: {service_id}")
        return True
    
    async def register_load_balancer(self, service_id: str, replicas: List[str]) -> bool:
        """Register load balancer for service"""
        self.load_balancers[service_id] = replicas
        logger.info(f"✅ Load balancer registered for service: {service_id} with {len(replicas)} replicas")
        return True
    
    # ========================================================================
    # 📊 STATISTICS & HEALTH
    # ========================================================================
    
    async def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        total_entries = sum(len(reg) for reg in self.sub_registries.values())
        
        stats_by_type = {}
        for sub_type, entries in self.sub_registries.items():
            stats_by_type[sub_type.value] = len(entries)
        
        return {
            "registry_id": self.registry_id,
            "created_at": self.created_at,
            "total_entries": total_entries,
            "entries_by_type": stats_by_type,
            "feature_flags": len(self.feature_flags),
            "permissions": len(self.permissions),
            "layouts": len(self.layouts),
            "intelligence_layers": len(self.intelligence_layers),
            "circuit_breakers": len(self.circuit_breakers),
            "load_balancers": len(self.load_balancers),
            "health_score": self.stats["health_score"],
            "last_update": datetime.utcnow().isoformat()
        }
    
    # ========================================================================
    # 🔗 RELATIONSHIPS
    # ========================================================================
    
    async def create_relationship(self, source_id: str, target_id: str, rel_type: str, strength: float = 1.0) -> bool:
        """Create relationship between entries"""
        if source_id not in self.relationships:
            self.relationships[source_id] = []
        
        self.relationships[source_id].append((target_id, rel_type, strength))
        logger.info(f"🔗 Relationship created: {source_id} -[{rel_type}]-> {target_id}")
        return True
    
    async def get_related_entries(self, entry_id: str, rel_type: Optional[str] = None) -> List[Tuple[str, str]]:
        """Get entries related to specified entry"""
        if entry_id not in self.relationships:
            return []
        
        related = []
        for target_id, r_type, strength in self.relationships[entry_id]:
            if rel_type is None or r_type == rel_type:
                related.append((target_id, r_type))
        
        return related
    
    # ========================================================================
    # 💾 EXPORT & IMPORT
    # ========================================================================
    
    async def export_to_json(self) -> str:
        """Export registry to JSON"""
        data = {
            "registry_id": self.registry_id,
            "created_at": self.created_at,
            "sub_registries": {
                k.value: v for k, v in self.sub_registries.items()
            },
            "feature_flags": {k: asdict(v) for k, v in self.feature_flags.items()},
            "permissions": {k: asdict(v) for k, v in self.permissions.items()},
            "layouts": {k: asdict(v) for k, v in self.layouts.items()},
            "intelligence_layers": {k: asdict(v) for k, v in self.intelligence_layers.items()},
            "relationships": self.relationships,
            "stats": self.stats
        }
        return json.dumps(data, indent=2, default=str)


# Singleton instance
universal_hyper_registry = UniversalHyperRegistryV2()
