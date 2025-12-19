#!/usr/bin/env python3
# ============================================================================
# 📊 NEXUS REGISTRY SYSTEM - Centralized Configuration Management
# ============================================================================
# Hierarchical registry system with 7 sub-registries orchestrated by master
# Syncs with Zsh CLI and provides real-time provider discovery
# ============================================================================

import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import hashlib
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# ============================================================================
# REGISTRY CONFIGURATION
# ============================================================================

REGISTRY_BASE_PATH = Path.home() / ".nexus" / "registries"
REGISTRY_SYNC_INTERVAL = 300  # 5 minutes
REGISTRY_TTL = 3600  # 1 hour

# ============================================================================
# DATA MODELS
# ============================================================================

class RegistryType(Enum):
    """Registry types in hierarchical system"""
    MASTER = "master"
    TOOLS = "tools"
    PROVIDERS = "providers"
    MODELS = "models"
    PLUGINS = "plugins"
    MICROSERVICES = "microservices"
    ADAPTERS = "adapters"
    ML_FRAMEWORKS = "ml_frameworks"

@dataclass
class ProviderInfo:
    """Provider information in registry"""
    name: str
    type: str  # openai, anthropic, google, deepseek, mistral, ollama
    status: str = "active"  # active, inactive, degraded
    api_endpoint: str = ""
    models: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    cost_per_1k_tokens: float = 0.0
    latency_ms: float = 0.0
    max_tokens: int = 4096
    rate_limit: int = 100
    healthcheck_interval: int = 300
    last_health_check: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelInfo:
    """Model information in registry"""
    name: str
    provider: str
    type: str  # text, image, audio, video, multimodal
    capabilities: List[str]
    context_window: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    release_date: str
    status: str = "available"
    is_latest: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdapterInfo:
    """Adapter implementation information"""
    name: str
    provider: str
    language: str  # python, zsh, go, rust
    status: str
    version: str
    models_supported: List[str]
    capabilities: List[str]
    implementation_path: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolInfo:
    """Development tool information"""
    name: str
    category: str  # code-analysis, code-generation, testing, deployment
    description: str
    icon: str
    command: str
    ai_enabled: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RegistrySync:
    """Registry sync metadata"""
    last_sync: str
    next_sync: str
    version: str
    hash: str
    status: str
    entries: int

# ============================================================================
# REGISTRY STORAGE
# ============================================================================

class Registry(ABC):
    """Abstract registry base class"""
    
    def __init__(self, registry_type: RegistryType):
        self.registry_type = registry_type
        self.path = REGISTRY_BASE_PATH / f"{registry_type.value}_registry.json"
        self.data: Dict[str, Any] = {}
        self.sync_info: Optional[RegistrySync] = None
        
    async def load(self):
        """Load registry from disk"""
        try:
            if self.path.exists():
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
                logger.info(f"✅ Loaded {self.registry_type.value} registry ({len(self.data)} entries)")
            else:
                logger.warning(f"Registry file not found: {self.path}")
                self.data = {}
        except Exception as e:
            logger.error(f"Failed to load {self.registry_type.value} registry: {e}")
            self.data = {}
    
    async def save(self):
        """Save registry to disk"""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=2)
            logger.info(f"✅ Saved {self.registry_type.value} registry")
        except Exception as e:
            logger.error(f"Failed to save {self.registry_type.value} registry: {e}")
    
    @abstractmethod
    async def sync(self):
        """Sync registry from source"""
        pass
    
    def calculate_hash(self) -> str:
        """Calculate registry content hash"""
        content = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

# ============================================================================
# PROVIDER REGISTRY
# ============================================================================

class ProviderRegistry(Registry):
    """Registry for AI providers and their capabilities"""
    
    def __init__(self):
        super().__init__(RegistryType.PROVIDERS)
        self.providers: Dict[str, ProviderInfo] = {}
    
    async def sync(self):
        """Sync provider information"""
        logger.info("🔄 Syncing provider registry...")
        
        # Initialize providers
        providers = {
            "openai": ProviderInfo(
                name="OpenAI",
                type="openai",
                api_endpoint="https://api.openai.com/v1",
                models=["gpt-5.1", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
                capabilities=["text_generation", "code_generation", "reasoning", "multimodal"],
                cost_per_1k_tokens=0.01,
                latency_ms=150,
                max_tokens=128000
            ),
            "anthropic": ProviderInfo(
                name="Anthropic",
                type="anthropic",
                api_endpoint="https://api.anthropic.com/v1",
                models=["claude-3-7-opus", "claude-3-7-sonnet", "claude-3-7-haiku"],
                capabilities=["text_generation", "reasoning", "code_analysis", "security"],
                cost_per_1k_tokens=0.015,
                latency_ms=200,
                max_tokens=200000
            ),
            "google": ProviderInfo(
                name="Google",
                type="google",
                api_endpoint="https://generativelanguage.googleapis.com/v1",
                models=["gemini-3", "gemini-2.0-pro", "gemini-2.0-flash"],
                capabilities=["text_generation", "image_understanding", "multimodal"],
                cost_per_1k_tokens=0.008,
                latency_ms=180,
                max_tokens=1000000
            ),
            "deepseek": ProviderInfo(
                name="DeepSeek",
                type="deepseek",
                api_endpoint="https://api.deepseek.com/v1",
                models=["deepseek-v3", "deepseek-r1", "deepseek-chat"],
                capabilities=["code_generation", "reasoning", "fast_inference"],
                cost_per_1k_tokens=0.003,
                latency_ms=100,
                max_tokens=128000
            ),
            "mistral": ProviderInfo(
                name="Mistral",
                type="mistral",
                api_endpoint="https://api.mistral.ai/v1",
                models=["mistral-large", "mistral-medium"],
                capabilities=["text_generation", "code_generation"],
                cost_per_1k_tokens=0.005,
                latency_ms=120,
                max_tokens=32768
            ),
            "ollama": ProviderInfo(
                name="Ollama",
                type="ollama",
                api_endpoint="http://localhost:11434",
                models=["llama3.1", "mistral", "codellama", "phi"],
                capabilities=["text_generation", "code_generation", "local_inference"],
                cost_per_1k_tokens=0.0,
                latency_ms=200,
                max_tokens=8192,
                metadata={"local": True}
            )
        }
        
        self.providers = providers
        self.data = {name: asdict(info) for name, info in providers.items()}
        await self.save()
        logger.info(f"✅ Provider registry synced ({len(providers)} providers)")

# ============================================================================
# MODEL REGISTRY
# ============================================================================

class ModelRegistry(Registry):
    """Registry for AI models and their specifications"""
    
    def __init__(self):
        super().__init__(RegistryType.MODELS)
        self.models: Dict[str, ModelInfo] = {}
    
    async def sync(self):
        """Sync model information"""
        logger.info("🔄 Syncing model registry...")
        
        models = {
            "gpt-5.1": ModelInfo(
                name="GPT-5.1",
                provider="openai",
                type="text",
                capabilities=["reasoning", "code_generation", "analysis"],
                context_window=128000,
                cost_per_1k_input=0.03,
                cost_per_1k_output=0.06,
                release_date="2025-01-01",
                is_latest=True
            ),
            "gpt-4o": ModelInfo(
                name="GPT-4o",
                provider="openai",
                type="multimodal",
                capabilities=["text", "image", "reasoning"],
                context_window=128000,
                cost_per_1k_input=0.005,
                cost_per_1k_output=0.015,
                release_date="2024-11-01"
            ),
            "claude-3-7-opus": ModelInfo(
                name="Claude 3.7 Opus",
                provider="anthropic",
                type="text",
                capabilities=["reasoning", "analysis", "code"],
                context_window=200000,
                cost_per_1k_input=0.015,
                cost_per_1k_output=0.075,
                release_date="2024-12-01",
                is_latest=True
            ),
            "gemini-3": ModelInfo(
                name="Gemini 3",
                provider="google",
                type="multimodal",
                capabilities=["text", "image", "video", "reasoning"],
                context_window=1000000,
                cost_per_1k_input=0.0075,
                cost_per_1k_output=0.03,
                release_date="2025-01-01",
                is_latest=True
            ),
            "deepseek-v3": ModelInfo(
                name="DeepSeek v3",
                provider="deepseek",
                type="text",
                capabilities=["code_generation", "reasoning", "fast"],
                context_window=128000,
                cost_per_1k_input=0.0014,
                cost_per_1k_output=0.0042,
                release_date="2024-12-26"
            )
        }
        
        self.models = models
        self.data = {name: asdict(info) for name, info in models.items()}
        await self.save()
        logger.info(f"✅ Model registry synced ({len(models)} models)")

# ============================================================================
# ADAPTER REGISTRY
# ============================================================================

class AdapterRegistry(Registry):
    """Registry for provider adapters"""
    
    def __init__(self):
        super().__init__(RegistryType.ADAPTERS)
        self.adapters: Dict[str, AdapterInfo] = {}
    
    async def sync(self):
        """Sync adapter information"""
        logger.info("🔄 Syncing adapter registry...")
        
        adapters = {
            "openai_adapter": AdapterInfo(
                name="OpenAI Adapter",
                provider="openai",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["gpt-5.1", "gpt-4o", "gpt-4-turbo"],
                capabilities=["streaming", "function_calling"],
                implementation_path="/services/llm_orchestrator/adapters/openai_adapter.py"
            ),
            "anthropic_adapter": AdapterInfo(
                name="Anthropic Adapter",
                provider="anthropic",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["claude-3-7-opus", "claude-3-7-sonnet"],
                capabilities=["streaming", "vision"],
                implementation_path="/services/llm_orchestrator/adapters/claude_adapter.py"
            ),
            "google_adapter": AdapterInfo(
                name="Google Adapter",
                provider="google",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["gemini-3", "gemini-2.0-pro"],
                capabilities=["multimodal", "vision"],
                implementation_path="/services/llm_orchestrator/adapters/gemini_adapter.py"
            ),
            "deepseek_adapter": AdapterInfo(
                name="DeepSeek Adapter",
                provider="deepseek",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["deepseek-v3", "deepseek-r1"],
                capabilities=["fast_inference", "streaming"],
                implementation_path="/services/llm_orchestrator/adapters/deepseek_adapter.py"
            ),
            "mistral_adapter": AdapterInfo(
                name="Mistral Adapter",
                provider="mistral",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["mistral-large", "mistral-medium"],
                capabilities=["streaming"],
                implementation_path="/services/llm_orchestrator/adapters/mistral_adapter.py"
            ),
            "ollama_adapter": AdapterInfo(
                name="Ollama Adapter",
                provider="ollama",
                language="python",
                status="active",
                version="1.0.0",
                models_supported=["llama3.1", "mistral"],
                capabilities=["local_inference"],
                implementation_path="/services/llm_orchestrator/adapters/ollama_adapter.py"
            )
        }
        
        self.adapters = adapters
        self.data = {name: asdict(info) for name, info in adapters.items()}
        await self.save()
        logger.info(f"✅ Adapter registry synced ({len(adapters)} adapters)")

# ============================================================================
# TOOL REGISTRY
# ============================================================================

class ToolRegistry(Registry):
    """Registry for development tools"""
    
    def __init__(self):
        super().__init__(RegistryType.TOOLS)
        self.tools: Dict[str, ToolInfo] = {}
    
    async def sync(self):
        """Sync tool information"""
        logger.info("🔄 Syncing tool registry...")
        
        tools = {
            "code_review": ToolInfo(
                name="Code Review",
                category="code-analysis",
                description="AI-powered code review with security analysis",
                icon="🔍",
                command="ai_code_review",
                ai_enabled=True
            ),
            "test_generator": ToolInfo(
                name="Test Generator",
                category="testing",
                description="Generate unit tests from code",
                icon="✓",
                command="ai_generate_tests",
                ai_enabled=True
            ),
            "documentation": ToolInfo(
                name="Documentation",
                category="code-generation",
                description="Generate and improve documentation",
                icon="📚",
                command="ai_generate_docs",
                ai_enabled=True
            ),
            "security_scan": ToolInfo(
                name="Security Scanner",
                category="code-analysis",
                description="Scan for security vulnerabilities",
                icon="🔒",
                command="ai_security_scan",
                ai_enabled=True
            ),
            "refactoring": ToolInfo(
                name="Refactoring Assistant",
                category="code-analysis",
                description="Suggest code refactoring improvements",
                icon="♻️",
                command="ai_refactor",
                ai_enabled=True
            )
        }
        
        self.tools = tools
        self.data = {name: asdict(info) for name, info in tools.items()}
        await self.save()
        logger.info(f"✅ Tool registry synced ({len(tools)} tools)")

# ============================================================================
# MASTER REGISTRY (ORCHESTRATOR)
# ============================================================================

class MasterRegistry(Registry):
    """Master registry orchestrating all sub-registries"""
    
    def __init__(self):
        super().__init__(RegistryType.MASTER)
        self.sub_registries: Dict[str, Registry] = {}
        self._init_sub_registries()
    
    def _init_sub_registries(self):
        """Initialize all sub-registries"""
        self.sub_registries = {
            "providers": ProviderRegistry(),
            "models": ModelRegistry(),
            "adapters": AdapterRegistry(),
            "tools": ToolRegistry(),
            # Additional registries would be initialized here
        }
    
    async def sync(self):
        """Sync all sub-registries"""
        logger.info("🔄 Syncing master registry...")
        
        sync_start = datetime.utcnow()
        total_entries = 0
        
        # Sync each sub-registry
        for name, registry in self.sub_registries.items():
            try:
                await registry.sync()
                total_entries += len(registry.data)
            except Exception as e:
                logger.error(f"Failed to sync {name} registry: {e}")
        
        sync_end = datetime.utcnow()
        
        # Update master registry
        self.data = {
            "registries": {
                name: {
                    "type": registry.registry_type.value,
                    "entries": len(registry.data),
                    "hash": registry.calculate_hash(),
                    "path": str(registry.path)
                }
                for name, registry in self.sub_registries.items()
            },
            "sync_info": {
                "last_sync": sync_start.isoformat(),
                "sync_duration_ms": int((sync_end - sync_start).total_seconds() * 1000),
                "total_entries": total_entries,
                "version": "2.0"
            }
        }
        
        await self.save()
        logger.info(f"✅ Master registry synced ({total_entries} total entries)")
    
    async def load(self):
        """Load master registry and all sub-registries"""
        await super().load()
        for registry in self.sub_registries.values():
            await registry.load()

# ============================================================================
# REGISTRY MANAGER
# ============================================================================

class RegistryManager:
    """Manages registry system lifecycle"""
    
    def __init__(self):
        self.master_registry = MasterRegistry()
        self.sync_task: Optional[asyncio.Task] = None
    
    async def initialize(self):
        """Initialize registry system"""
        logger.info("🚀 Initializing registry system...")
        
        # Create directories
        REGISTRY_BASE_PATH.mkdir(parents=True, exist_ok=True)
        
        # Load and sync
        await self.master_registry.load()
        await self.master_registry.sync()
        
        # Start periodic sync
        self.sync_task = asyncio.create_task(self._periodic_sync())
        
        logger.info("✅ Registry system initialized")
    
    async def _periodic_sync(self):
        """Periodic registry synchronization"""
        while True:
            try:
                await asyncio.sleep(REGISTRY_SYNC_INTERVAL)
                await self.master_registry.sync()
            except Exception as e:
                logger.error(f"Periodic sync failed: {e}")
    
    async def shutdown(self):
        """Shutdown registry system"""
        if self.sync_task:
            self.sync_task.cancel()
        logger.info("✅ Registry system shutdown")
    
    def get_registry(self, registry_type: RegistryType) -> Optional[Registry]:
        """Get specific registry"""
        if registry_type == RegistryType.MASTER:
            return self.master_registry
        return self.master_registry.sub_registries.get(registry_type.value)
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all registry data"""
        return self.master_registry.data

# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_registry_manager: Optional[RegistryManager] = None

def get_registry_manager() -> RegistryManager:
    """Get or create registry manager singleton"""
    global _registry_manager
    if _registry_manager is None:
        _registry_manager = RegistryManager()
    return _registry_manager

# ============================================================================
# CLI INTEGRATION
# ============================================================================

async def initialize_registry_from_cli():
    """Initialize registry for CLI usage"""
    manager = get_registry_manager()
    await manager.initialize()
    return manager

if __name__ == "__main__":
    import asyncio
    
    async def main():
        manager = get_registry_manager()
        await manager.initialize()
        print(json.dumps(manager.get_all_data(), indent=2))
    
    asyncio.run(main())
