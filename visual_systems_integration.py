"""
🔌 VISUAL SYSTEMS INTEGRATION
Bridge between LayoutConfigurationEngine, VisualStylingEngine, and Registry Subsystems
Enables universal layout and visual application across all modules
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger("hyper_registry.visual_integration")


class VisualSystemsIntegration:
    """
    🎨 VISUAL SYSTEMS INTEGRATION
    Unified interface for layout, visual, animation, and theme management
    """
    
    def __init__(self):
        """Initialize integration with all visual engines"""
        try:
            from .layout_engine import layout_engine
            from .visual_styling import visual_engine
            from .registry_subsystems import subsystem_manager
            
            self.layout_engine = layout_engine
            self.visual_engine = visual_engine
            self.subsystem_manager = subsystem_manager
            
            logger.info("✅ Visual Systems Integration initialized")
            logger.info("   - Layout Engine: ✓")
            logger.info("   - Visual Engine: ✓")
            logger.info("   - Registry Subsystems: ✓")
            
        except ImportError as e:
            logger.error(f"❌ Failed to import visual engines: {e}")
            raise
    
    def create_dashboard_with_visuals(self) -> Dict[str, Any]:
        """
        📊 Create complete dashboard with layout + visuals
        Returns configuration for dashboard with all visual systems applied
        """
        try:
            # Get dashboard layout
            dashboard_layout = self.layout_engine.create_custom_layout(
                name="Dashboard",
                layout_type="dashboard",
                modules=[
                    {
                        "name": "header",
                        "position": "top",
                        "size_mode": "fill",
                        "height_percentage": 15
                    },
                    {
                        "name": "metadata",
                        "position": "left",
                        "size_mode": "percentage",
                        "width_percentage": 20,
                        "height_percentage": 35
                    },
                    {
                        "name": "telemetry",
                        "position": "right",
                        "size_mode": "percentage",
                        "width_percentage": 30,
                        "height_percentage": 35
                    },
                    {
                        "name": "content",
                        "position": "center",
                        "size_mode": "fill",
                        "height_percentage": 40
                    },
                    {
                        "name": "input",
                        "position": "bottom",
                        "size_mode": "fill",
                        "height_percentage": 10
                    }
                ]
            )
            
            # Get quantum theme visual styles
            quantum_header_style = self.visual_engine.get_style("quantum_header")
            quantum_button_style = self.visual_engine.get_style("quantum_button")
            
            # Combine layout and visuals
            config = {
                "type": "dashboard",
                "layout": dashboard_layout.to_dict() if hasattr(dashboard_layout, 'to_dict') else dashboard_layout,
                "modules": {
                    "header": {
                        "visual_style": quantum_header_style.to_dict() if quantum_header_style else {},
                        "emoji": "🚀",
                        "title": "NEXUS AI STUDIO MATRIX",
                        "animations": ["particle_flow", "gradient_cycle"],
                        "gradient": "linear_cyan_purple_magenta"
                    },
                    "metadata": {
                        "emoji": "📊",
                        "title": "System Metadata",
                        "visual_style": "panel",
                        "refresh_rate": 1000
                    },
                    "telemetry": {
                        "emoji": "📈",
                        "title": "Live Telemetry",
                        "visual_style": "panel",
                        "metrics": ["cpu", "gpu", "memory", "models", "tasks"],
                        "refresh_rate": 500
                    },
                    "content": {
                        "emoji": "💬",
                        "title": "Model Response",
                        "visual_style": "content_panel",
                        "interactive": True,
                        "switchable_to_chatbox": True
                    },
                    "input": {
                        "emoji": "⌨️",
                        "title": "Input Panel",
                        "visual_style": "input_panel",
                        "auto_scaling": True,
                        "placeholder": "Select AI Model or type your query..."
                    }
                },
                "theme": "quantum",
                "responsive": True,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info("✅ Dashboard with visuals created successfully")
            return config
            
        except Exception as e:
            logger.error(f"❌ Failed to create dashboard with visuals: {e}")
            raise
    
    def create_chat_interface_with_visuals(self) -> Dict[str, Any]:
        """
        💬 Create chat interface with layout + visuals
        Returns configuration for chat with 30% chat + 70% visuals split
        """
        try:
            # Get chat layout
            chat_layout = self.layout_engine.create_custom_layout(
                name="Chat Interface",
                layout_type="chat",
                modules=[
                    {
                        "name": "chat_panel",
                        "position": "left",
                        "size_mode": "percentage",
                        "width_percentage": 30
                    },
                    {
                        "name": "visual_panel",
                        "position": "right",
                        "size_mode": "percentage",
                        "width_percentage": 70
                    }
                ]
            )
            
            config = {
                "type": "chat",
                "layout": chat_layout.to_dict() if hasattr(chat_layout, 'to_dict') else chat_layout,
                "modules": {
                    "chat_panel": {
                        "emoji": "💬",
                        "title": "Chat Interface",
                        "visual_style": "chat",
                        "components": ["message_list", "input_box", "send_button"],
                        "streaming": True,
                        "show_thinking": True
                    },
                    "visual_panel": {
                        "emoji": "🎨",
                        "title": "Visual Analytics",
                        "visual_style": "glassmorphism",
                        "sub_modules": [
                            {
                                "name": "confidence_gauge",
                                "type": "gauge",
                                "emoji": "📊"
                            },
                            {
                                "name": "ensemble_visualization",
                                "type": "ensemble_gauges",
                                "emoji": "🎯"
                            },
                            {
                                "name": "token_counter",
                                "type": "counter",
                                "emoji": "🔢"
                            },
                            {
                                "name": "latency_chart",
                                "type": "chart",
                                "emoji": "⏱️"
                            }
                        ]
                    }
                },
                "theme": "quantum",
                "responsive": True,
                "interactive": True,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info("✅ Chat interface with visuals created successfully")
            return config
            
        except Exception as e:
            logger.error(f"❌ Failed to create chat interface with visuals: {e}")
            raise
    
    def create_builder_interface_with_visuals(self) -> Dict[str, Any]:
        """
        🏗️ Create builder interface with layout + visuals
        Returns configuration for builder with 3-column layout (workflow + code + preview)
        """
        try:
            # Get builder layout
            builder_layout = self.layout_engine.create_custom_layout(
                name="Builder Interface",
                layout_type="builder",
                modules=[
                    {
                        "name": "workflow_panel",
                        "position": "left",
                        "size_mode": "percentage",
                        "width_percentage": 33
                    },
                    {
                        "name": "code_panel",
                        "position": "center",
                        "size_mode": "percentage",
                        "width_percentage": 33
                    },
                    {
                        "name": "preview_panel",
                        "position": "right",
                        "size_mode": "percentage",
                        "width_percentage": 34
                    }
                ]
            )
            
            config = {
                "type": "builder",
                "layout": builder_layout.to_dict() if hasattr(builder_layout, 'to_dict') else builder_layout,
                "modules": {
                    "workflow_panel": {
                        "emoji": "📋",
                        "title": "Workflow",
                        "visual_style": "panel",
                        "components": ["node_canvas", "connector_lines"]
                    },
                    "code_panel": {
                        "emoji": "📝",
                        "title": "Code Editor",
                        "visual_style": "code_editor",
                        "syntax_highlighting": True,
                        "line_numbers": True
                    },
                    "preview_panel": {
                        "emoji": "👁️",
                        "title": "Preview",
                        "visual_style": "preview",
                        "real_time": True
                    }
                },
                "theme": "minimal",
                "responsive": True,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info("✅ Builder interface with visuals created successfully")
            return config
            
        except Exception as e:
            logger.error(f"❌ Failed to create builder interface with visuals: {e}")
            raise
    
    def create_analytics_interface_with_visuals(self) -> Dict[str, Any]:
        """
        📊 Create analytics interface with layout + visuals
        Returns configuration for analytics dashboard
        """
        try:
            # Get analytics layout
            analytics_layout = self.layout_engine.create_custom_layout(
                name="Analytics Dashboard",
                layout_type="analytics",
                modules=[
                    {
                        "name": "sparklines_panel",
                        "position": "top",
                        "size_mode": "fill",
                        "height_percentage": 25
                    },
                    {
                        "name": "metrics_panel",
                        "position": "center",
                        "size_mode": "fill",
                        "height_percentage": 50
                    },
                    {
                        "name": "activity_panel",
                        "position": "bottom",
                        "size_mode": "fill",
                        "height_percentage": 25
                    }
                ]
            )
            
            config = {
                "type": "analytics",
                "layout": analytics_layout.to_dict() if hasattr(analytics_layout, 'to_dict') else analytics_layout,
                "modules": {
                    "sparklines_panel": {
                        "emoji": "📈",
                        "title": "System Metrics Overview",
                        "metrics": ["cpu_sparkline", "gpu_sparkline", "memory_sparkline", "network_sparkline"]
                    },
                    "metrics_panel": {
                        "emoji": "📊",
                        "title": "Detailed Metrics",
                        "grid": "2x2",
                        "charts": [
                            {"name": "CPU Usage", "type": "line"},
                            {"name": "GPU Utilization", "type": "line"},
                            {"name": "Model Performance", "type": "bar"},
                            {"name": "Task Queue", "type": "gauge"}
                        ]
                    },
                    "activity_panel": {
                        "emoji": "🎯",
                        "title": "Live Activity",
                        "show_latest": 10,
                        "auto_scroll": True
                    }
                },
                "theme": "quantum",
                "responsive": True,
                "refresh_rate": 1000,
                "created_at": datetime.utcnow().isoformat()
            }
            
            logger.info("✅ Analytics interface with visuals created successfully")
            return config
            
        except Exception as e:
            logger.error(f"❌ Failed to create analytics interface with visuals: {e}")
            raise
    
    def apply_responsive_layout(self, config: Dict[str, Any], terminal_width: int) -> Dict[str, Any]:
        """
        📐 Apply responsive layout based on terminal width
        Automatically adjusts layout for mobile/tablet/desktop/ultra-wide
        """
        try:
            # Detect breakpoint
            if terminal_width < 100:
                breakpoint = "mobile"
            elif terminal_width < 120:
                breakpoint = "tablet"
            elif terminal_width < 200:
                breakpoint = "desktop"
            else:
                breakpoint = "ultra_wide"
            
            config["breakpoint"] = breakpoint
            config["terminal_width"] = terminal_width
            
            # Compute responsive adjustments
            responsive_config = self.layout_engine.compute_module_geometry(
                config.get("layout", {}),
                terminal_width=terminal_width
            )
            
            config["responsive_geometry"] = responsive_config
            
            logger.info(f"✅ Responsive layout applied: {breakpoint} ({terminal_width}col)")
            return config
            
        except Exception as e:
            logger.error(f"❌ Failed to apply responsive layout: {e}")
            raise
    
    def get_available_layouts(self) -> List[Dict[str, str]]:
        """Get list of available layouts"""
        try:
            return [
                {"name": "Dashboard", "type": "dashboard", "emoji": "📊", "description": "Main dashboard with header, metadata, telemetry, content, input"},
                {"name": "Chat", "type": "chat", "emoji": "💬", "description": "Chat interface with 30% chat + 70% visuals"},
                {"name": "Builder", "type": "builder", "emoji": "🏗️", "description": "Builder with 3-column layout (workflow, code, preview)"},
                {"name": "Analytics", "type": "analytics", "emoji": "📈", "description": "Analytics dashboard with metrics and charts"},
                {"name": "Monitor", "type": "monitor", "emoji": "🔍", "description": "System monitoring interface"},
                {"name": "Settings", "type": "settings", "emoji": "⚙️", "description": "Configuration interface"},
                {"name": "Minimal", "type": "minimal", "emoji": "📋", "description": "Minimal interface"},
                {"name": "Fullscreen", "type": "fullscreen", "emoji": "🖥️", "description": "Fullscreen interface"}
            ]
        except Exception as e:
            logger.error(f"❌ Failed to get available layouts: {e}")
            return []
    
    def get_available_themes(self) -> List[Dict[str, str]]:
        """Get list of available themes"""
        try:
            return [
                {"name": "Quantum", "theme_id": "quantum", "emoji": "⚛️", "description": "Cyberpunk neon theme with gradients and glow"},
                {"name": "Glassmorphism", "theme_id": "glassmorphism", "emoji": "🔮", "description": "Transparent glass-like effects"},
                {"name": "Minimal", "theme_id": "minimal", "emoji": "⚪", "description": "Clean and minimal design"},
                {"name": "Dark", "theme_id": "dark", "emoji": "🌙", "description": "Dark mode theme"},
                {"name": "Light", "theme_id": "light", "emoji": "☀️", "description": "Light mode theme"}
            ]
        except Exception as e:
            logger.error(f"❌ Failed to get available themes: {e}")
            return []
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrated systems"""
        try:
            return {
                "layout_engine": {
                    "status": "active" if self.layout_engine else "inactive",
                    "available_layouts": len(self.layout_engine.templates) if self.layout_engine else 0,
                    "emoji": "📐"
                },
                "visual_engine": {
                    "status": "active" if self.visual_engine else "inactive",
                    "available_themes": len(self.visual_engine.themes) if self.visual_engine else 0,
                    "available_styles": len(self.visual_engine.styles) if self.visual_engine else 0,
                    "emoji": "🎨"
                },
                "registry_subsystems": {
                    "status": "active" if self.subsystem_manager else "inactive",
                    "stats": self.subsystem_manager.get_subsystem_stats() if self.subsystem_manager else {},
                    "emoji": "📋"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Failed to get integration status: {e}")
            return {"status": "error", "error": str(e)}


# Global instance
visual_systems_integration = VisualSystemsIntegration()

logger.info("✅ Visual Systems Integration ready for use")
logger.info("   Available interfaces: dashboard, chat, builder, analytics")
logger.info("   Available themes: quantum, glassmorphism, minimal")
