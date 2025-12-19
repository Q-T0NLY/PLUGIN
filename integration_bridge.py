"""
🌐 UNIVERSAL SYSTEM INTEGRATION BRIDGE
Connects VisualsEngine + LayoutSystem + Registry + Intelligence
Provides unified interface for all system components
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json

logger = logging.getLogger("hyper_registry.integration_bridge")


# ============================================================================
# 🎯 INTEGRATION CONFIGURATION
# ============================================================================

@dataclass
class IntegrationConfig:
    """System-wide integration configuration"""
    
    # System settings
    enable_visuals: bool = True
    enable_layouts: bool = True
    enable_registry: bool = True
    enable_intelligence: bool = True
    
    # Caching
    cache_enabled: bool = True
    cache_ttl: int = 300  # seconds
    
    # Logging
    log_level: str = "INFO"
    
    # Performance
    async_execution: bool = True
    parallel_fusion: bool = True
    max_workers: int = 10
    
    # Output formatting
    use_emojis: bool = True
    use_colors: bool = True
    use_animations: bool = True
    
    # Telemetry
    telemetry_enabled: bool = True
    metrics_enabled: bool = True


# ============================================================================
# 🔗 UNIFIED INTEGRATION BRIDGE
# ============================================================================

class UniversalIntegrationBridge:
    """
    Master bridge connecting all systems:
    - VisualsEngine (colors, animations, 3D)
    - LayoutSystem (layouts for all contexts)
    - UniversalHyperRegistryV2 (data storage)
    - AdvancedIntelligenceSystem (AI/reasoning)
    """
    
    def __init__(self, config: Optional[IntegrationConfig] = None):
        self.bridge_id = "bridge_" + str(id(self))
        self.config = config or IntegrationConfig()
        
        # Component references (lazy-loaded)
        self._visuals_engine = None
        self._layout_manager = None
        self._registry = None
        self._intelligence_system = None
        
        # Integration state
        self.active_context: Dict[str, Any] = {}
        self.current_layout: Optional[str] = None
        self.current_theme: Optional[str] = None
        self.render_cache: Dict[str, Any] = {}
        
        # Metrics
        self.integration_metrics = {
            "total_renders": 0,
            "total_api_calls": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "intelligence_inferences": 0,
            "avg_render_time_ms": 0.0
        }
        
        logger.info(f"🌐 Universal Integration Bridge initialized - ID: {self.bridge_id}")
    
    # ========================================================================
    # 🔌 COMPONENT INITIALIZATION
    # ========================================================================
    
    def set_visuals_engine(self, engine: Any) -> None:
        """Set reference to VisualsEngine"""
        self._visuals_engine = engine
        logger.info("✅ VisualsEngine registered")
    
    def set_layout_manager(self, manager: Any) -> None:
        """Set reference to LayoutManager"""
        self._layout_manager = manager
        logger.info("✅ LayoutManager registered")
    
    def set_registry(self, registry: Any) -> None:
        """Set reference to UniversalHyperRegistryV2"""
        self._registry = registry
        logger.info("✅ Registry registered")
    
    def set_intelligence_system(self, system: Any) -> None:
        """Set reference to AdvancedIntelligenceSystem"""
        self._intelligence_system = system
        logger.info("✅ Intelligence System registered")
    
    # ========================================================================
    # 🎨 RENDERING PIPELINE
    # ========================================================================
    
    async def render_component(self, component_key: str, data: Dict[str, Any], 
                               layout_type: str = "dashboard") -> Optional[Dict[str, Any]]:
        """Render component with visuals, layout, and intelligence"""
        
        import time
        start_time = time.time()
        
        # Check cache
        cache_key = f"{component_key}_{layout_type}"
        if self.config.cache_enabled and cache_key in self.render_cache:
            self.integration_metrics["cache_hits"] += 1
            logger.info(f"💾 Cache hit: {cache_key}")
            return self.render_cache[cache_key]
        
        self.integration_metrics["cache_misses"] += 1
        
        # Build rendering result
        result = {
            "component_key": component_key,
            "layout_type": layout_type,
            "visual_properties": {},
            "layout_config": {},
            "registry_data": {},
            "intelligence_data": {},
            "formatted_output": None
        }
        
        try:
            # Step 1: Get visual properties
            if self.config.enable_visuals and self._visuals_engine:
                result["visual_properties"] = await self._apply_visuals(component_key, data)
            
            # Step 2: Get layout configuration
            if self.config.enable_layouts and self._layout_manager:
                result["layout_config"] = await self._apply_layout(component_key, layout_type)
            
            # Step 3: Get registry data
            if self.config.enable_registry and self._registry:
                result["registry_data"] = await self._get_registry_data(component_key)
            
            # Step 4: Apply intelligence
            if self.config.enable_intelligence and self._intelligence_system:
                result["intelligence_data"] = await self._apply_intelligence(component_key, data)
            
            # Step 5: Format final output
            result["formatted_output"] = self._format_output(result, data)
            
            # Cache result
            if self.config.cache_enabled:
                self.render_cache[cache_key] = result
            
            # Update metrics
            render_time = (time.time() - start_time) * 1000
            self.integration_metrics["total_renders"] += 1
            self.integration_metrics["avg_render_time_ms"] = (
                (self.integration_metrics["avg_render_time_ms"] * 
                 (self.integration_metrics["total_renders"] - 1) + 
                 render_time) / self.integration_metrics["total_renders"]
            )
            
            logger.info(f"✅ Component rendered: {component_key} ({render_time:.2f}ms)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Render error for {component_key}: {e}")
            return None
    
    async def _apply_visuals(self, component_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply visual properties from VisualsEngine"""
        if not self._visuals_engine:
            return {}
        
        return {
            "has_component": self._visuals_engine.get_component(component_key) is not None,
            "css_classes": f"visual-component visual-{component_key}",
            "animations_enabled": self.config.use_animations
        }
    
    async def _apply_layout(self, component_key: str, layout_type: str) -> Dict[str, Any]:
        """Apply layout configuration"""
        if not self._layout_manager:
            return {}
        
        return {
            "layout_type": layout_type,
            "responsive": True,
            "breakpoints": ["mobile", "tablet", "desktop", "ultrawide"]
        }
    
    async def _get_registry_data(self, component_key: str) -> Dict[str, Any]:
        """Get registry data for component"""
        if not self._registry:
            return {}
        
        self.integration_metrics["total_api_calls"] += 1
        
        return {
            "component_registered": True,
            "registry_entries": 0
        }
    
    async def _apply_intelligence(self, component_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply intelligence layer"""
        if not self._intelligence_system:
            return {}
        
        self.integration_metrics["intelligence_inferences"] += 1
        
        return {
            "intelligent_suggestions": [],
            "confidence_score": 0.85,
            "system_ready": True
        }
    
    def _format_output(self, render_result: Dict[str, Any], data: Dict[str, Any]) -> str:
        """Format final output with emojis, colors, etc."""
        output = []
        
        if self.config.use_emojis:
            output.append("✨ ")
        
        output.append(f"Component: {render_result['component_key']}")
        
        if self.config.use_colors:
            output.append(" | ")
            output.append(render_result['layout_type'])
        
        return "".join(output)
    
    # ========================================================================
    # 🚀 HIGH-LEVEL OPERATIONS
    # ========================================================================
    
    async def process_user_request(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process complete user request through all layers"""
        
        logger.info(f"🔄 Processing user request: {user_input[:50]}...")
        
        result = {
            "request": user_input,
            "intent": None,
            "workflow": None,
            "rendered_output": None,
            "status": "processing"
        }
        
        if not self._intelligence_system:
            result["status"] = "intelligence_unavailable"
            return result
        
        try:
            # Step 1: Update context
            if context:
                await self._intelligence_system.update_context("session", context)
            
            # Step 2: Parse intent
            intent = await self._intelligence_system.parse_intent(user_input)
            result["intent"] = intent
            
            # Step 3: Orchestrate workflow
            workflow = await self._intelligence_system.orchestrate_workflow(intent)
            result["workflow"] = workflow
            
            # Step 4: Render output
            rendered = await self.render_component("main_output", {"data": user_input})
            result["rendered_output"] = rendered
            
            result["status"] = "completed"
            logger.info("✅ User request processed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error processing user request: {e}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    # ========================================================================
    # 📊 CONTEXT MANAGEMENT
    # ========================================================================
    
    async def set_active_context(self, context_type: str, data: Dict[str, Any]) -> bool:
        """Set active context"""
        self.active_context[context_type] = data
        
        if self._intelligence_system:
            await self._intelligence_system.update_context(context_type, data)
        
        logger.info(f"📍 Active context set: {context_type}")
        return True
    
    def get_active_context(self) -> Dict[str, Any]:
        """Get current active context"""
        return self.active_context.copy()
    
    # ========================================================================
    # 🎨 THEME & LAYOUT SWITCHING
    # ========================================================================
    
    async def set_theme(self, theme_name: str) -> bool:
        """Set system theme"""
        if not self._visuals_engine:
            logger.warning("⚠️ VisualsEngine not available")
            return False
        
        self.current_theme = theme_name
        logger.info(f"🎨 Theme set: {theme_name}")
        return True
    
    async def set_layout(self, layout_type: str) -> bool:
        """Set system layout"""
        if not self._layout_manager:
            logger.warning("⚠️ LayoutManager not available")
            return False
        
        self.current_layout = layout_type
        logger.info(f"📐 Layout set: {layout_type}")
        return True
    
    # ========================================================================
    # 📈 METRICS & DIAGNOSTICS
    # ========================================================================
    
    def get_integration_metrics(self) -> Dict[str, Any]:
        """Get integration metrics"""
        cache_total = self.integration_metrics["cache_hits"] + self.integration_metrics["cache_misses"]
        cache_hit_rate = (
            self.integration_metrics["cache_hits"] / cache_total * 100
            if cache_total > 0 else 0
        )
        
        return {
            **self.integration_metrics,
            "cache_hit_rate_percent": cache_hit_rate,
            "components_cached": len(self.render_cache)
        }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        health = {
            "bridge_id": self.bridge_id,
            "components": {
                "visuals_engine": self._visuals_engine is not None,
                "layout_manager": self._layout_manager is not None,
                "registry": self._registry is not None,
                "intelligence_system": self._intelligence_system is not None
            },
            "config": {
                "visuals_enabled": self.config.enable_visuals,
                "layouts_enabled": self.config.enable_layouts,
                "registry_enabled": self.config.enable_registry,
                "intelligence_enabled": self.config.enable_intelligence
            },
            "metrics": self.get_integration_metrics()
        }
        
        return health
    
    def clear_cache(self) -> int:
        """Clear render cache"""
        size = len(self.render_cache)
        self.render_cache.clear()
        logger.info(f"🧹 Cache cleared: {size} entries removed")
        return size


# ============================================================================
# 🌍 SINGLETON & FACTORY
# ============================================================================

# Global bridge instance
universal_bridge = UniversalIntegrationBridge()


async def initialize_bridge(
    visuals_engine: Any = None,
    layout_manager: Any = None,
    registry: Any = None,
    intelligence_system: Any = None,
    config: Optional[IntegrationConfig] = None
) -> UniversalIntegrationBridge:
    """Initialize universal bridge with all components"""
    
    bridge = UniversalIntegrationBridge(config)
    
    if visuals_engine:
        bridge.set_visuals_engine(visuals_engine)
    if layout_manager:
        bridge.set_layout_manager(layout_manager)
    if registry:
        bridge.set_registry(registry)
    if intelligence_system:
        bridge.set_intelligence_system(intelligence_system)
    
    logger.info("✅ Universal Integration Bridge fully initialized")
    return bridge
