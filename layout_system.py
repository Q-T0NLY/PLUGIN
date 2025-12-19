"""
🎨 LAYOUT CONFIGURATION SYSTEM
Multi-layout support for Dashboard, Chat, CLI, 3D DAG, Metrics, and more
Auto-selectable based on context, device, and user preference
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging

logger = logging.getLogger("hyper_registry.layout_system")


# ============================================================================
# 📐 LAYOUT TYPES
# ============================================================================

class LayoutType(Enum):
    """Available layout types"""
    DASHBOARD = "dashboard"
    CHAT = "chat"
    CLI_TERMINAL = "cli_terminal"
    METRICS = "metrics"
    DAG_3D = "dag_3d"
    WIREFRAME = "wireframe"
    REASONING = "reasoning"
    HYBRID = "hybrid"


class ComponentPosition(Enum):
    """Component positions in layout"""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"
    FLOATING = "floating"
    FULLSCREEN = "fullscreen"


class ResponsiveBreakpoint(Enum):
    """Responsive design breakpoints"""
    MOBILE = "mobile"  # < 480px
    TABLET = "tablet"  # 480px - 1024px
    DESKTOP = "desktop"  # 1024px - 1920px
    ULTRAWIDE = "ultrawide"  # > 1920px


# ============================================================================
# 🧩 LAYOUT COMPONENT DEFINITION
# ============================================================================

@dataclass
class LayoutComponent:
    """Single component in a layout"""
    component_id: str
    component_type: str  # "chat", "metrics", "dag", "header", "footer", etc.
    title: str
    description: str = ""
    
    # Positioning
    position: ComponentPosition = ComponentPosition.CENTER
    width: Optional[float] = None  # percentage or pixels
    height: Optional[float] = None
    min_width: Optional[float] = None
    min_height: Optional[float] = None
    
    # Display & Visibility
    visible: bool = True
    collapsible: bool = False
    collapsed: bool = False
    
    # Styling
    background_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: float = 1.0
    border_radius: float = 8.0
    shadow: bool = True
    shadow_blur: float = 10.0
    
    # Responsive behavior
    responsive_config: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Animation
    animation_enabled: bool = True
    animation_name: Optional[str] = None
    animation_duration: float = 300.0  # milliseconds
    
    # Content & Metadata
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Interaction
    interactive: bool = True
    clickable: bool = False
    draggable: bool = False
    resizable: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def get_responsive_config(self, breakpoint: ResponsiveBreakpoint) -> Dict[str, Any]:
        """Get responsive config for specific breakpoint"""
        return self.responsive_config.get(breakpoint.value, {})


# ============================================================================
# 📋 LAYOUT DEFINITION
# ============================================================================

@dataclass
class LayoutDefinition:
    """Complete layout definition"""
    layout_id: str
    name: str
    layout_type: LayoutType
    description: str = ""
    
    # Components
    components: List[LayoutComponent] = field(default_factory=list)
    component_order: List[str] = field(default_factory=list)
    
    # Styling
    theme: str = "dark"
    background_color: str = "#0a0e27"
    accent_color: str = "#00d9ff"
    text_color: str = "#ffffff"
    
    # Responsive Design
    responsive_mode: bool = True
    responsive_breakpoints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Animation & Transitions
    animations_enabled: bool = True
    animation_library: List[str] = field(default_factory=list)
    transition_duration: float = 250.0  # milliseconds
    
    # Accessibility
    accessibility_level: str = "wcag2.1_aa"
    focus_management_enabled: bool = True
    keyboard_navigation_enabled: bool = True
    
    # Layout behavior
    auto_layout: bool = True
    grid_columns: Optional[int] = None
    grid_rows: Optional[int] = None
    grid_gap: float = 16.0
    
    # Metadata
    created_at: Optional[str] = None
    last_modified: Optional[str] = None
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            **asdict(self),
            "layout_type": self.layout_type.value,
            "components": [c.to_dict() for c in self.components]
        }


# ============================================================================
# 🎯 LAYOUT TEMPLATES (PRE-BUILT LAYOUTS)
# ============================================================================

class LayoutTemplates:
    """Pre-built layout templates"""
    
    @staticmethod
    def create_dashboard_layout() -> LayoutDefinition:
        """Create dashboard layout with header, metrics, chat, visuals"""
        return LayoutDefinition(
            layout_id="dashboard_default",
            name="Dashboard",
            layout_type=LayoutType.DASHBOARD,
            description="Full-featured dashboard with header, metrics, chat, and visuals",
            theme="dark",
            components=[
                LayoutComponent(
                    component_id="header",
                    component_type="header",
                    title="Quantum Header",
                    position=ComponentPosition.TOP_CENTER,
                    height=120.0,
                    width=100.0,
                    shadow=True,
                    animation_enabled=True,
                    animation_name="fade_in"
                ),
                LayoutComponent(
                    component_id="chat",
                    component_type="chat",
                    title="Chat Interface",
                    position=ComponentPosition.CENTER_LEFT,
                    width=30.0,
                    height=70.0,
                    collapsible=True,
                    draggable=True,
                    resizable=True,
                    responsive_config={
                        "mobile": {"width": 100.0, "height": 50.0},
                        "tablet": {"width": 50.0, "height": 70.0},
                        "desktop": {"width": 30.0, "height": 70.0}
                    }
                ),
                LayoutComponent(
                    component_id="visuals",
                    component_type="visuals",
                    title="Visual Reasoning",
                    position=ComponentPosition.CENTER_RIGHT,
                    width=40.0,
                    height=70.0,
                    collapsible=True,
                    draggable=True,
                    resizable=True
                ),
                LayoutComponent(
                    component_id="metrics",
                    component_type="metrics",
                    title="Metrics & Telemetry",
                    position=ComponentPosition.BOTTOM_CENTER,
                    height=20.0,
                    width=100.0,
                    collapsible=True
                ),
                LayoutComponent(
                    component_id="ai_panel",
                    component_type="ai_reasoning",
                    title="AI Consensus",
                    position=ComponentPosition.CENTER_RIGHT,
                    width=30.0,
                    height=30.0,
                    collapsed=True,
                    collapsible=True
                ),
                LayoutComponent(
                    component_id="controls",
                    component_type="controls",
                    title="Quick Actions",
                    position=ComponentPosition.TOP_RIGHT,
                    width=15.0,
                    height=10.0,
                    interactive=True
                )
            ]
        )
    
    @staticmethod
    def create_chat_layout() -> LayoutDefinition:
        """Create chat-focused layout"""
        return LayoutDefinition(
            layout_id="chat_focused",
            name="Chat Focused",
            layout_type=LayoutType.CHAT,
            description="Chat-first layout with minimal sidebars",
            theme="dark",
            components=[
                LayoutComponent(
                    component_id="header",
                    component_type="header",
                    title="Header",
                    position=ComponentPosition.TOP_CENTER,
                    height=80.0,
                    width=100.0
                ),
                LayoutComponent(
                    component_id="chat_main",
                    component_type="chat",
                    title="Conversation",
                    position=ComponentPosition.CENTER,
                    width=100.0,
                    height=80.0,
                    resizable=True,
                    interactive=True
                ),
                LayoutComponent(
                    component_id="input",
                    component_type="input",
                    title="Input Area",
                    position=ComponentPosition.BOTTOM_CENTER,
                    height=15.0,
                    width=100.0,
                    interactive=True,
                    clickable=True
                ),
                LayoutComponent(
                    component_id="thinking",
                    component_type="reasoning",
                    title="AI Thinking",
                    position=ComponentPosition.FLOATING,
                    width=30.0,
                    height=25.0,
                    collapsed=True,
                    collapsible=True
                )
            ]
        )
    
    @staticmethod
    def create_cli_layout() -> LayoutDefinition:
        """Create terminal/CLI layout"""
        return LayoutDefinition(
            layout_id="cli_terminal",
            name="CLI Terminal",
            layout_type=LayoutType.CLI_TERMINAL,
            description="Command-line interface with TUI",
            theme="dark",
            components=[
                LayoutComponent(
                    component_id="banner",
                    component_type="header",
                    title="Banner",
                    position=ComponentPosition.TOP_CENTER,
                    height=15.0,
                    width=100.0,
                    animation_enabled=True
                ),
                LayoutComponent(
                    component_id="main_panel",
                    component_type="panel",
                    title="Main Panel",
                    position=ComponentPosition.CENTER,
                    width=100.0,
                    height=70.0,
                    resizable=True
                ),
                LayoutComponent(
                    component_id="status_bar",
                    component_type="status",
                    title="Status Bar",
                    position=ComponentPosition.BOTTOM_CENTER,
                    height=5.0,
                    width=100.0
                ),
                LayoutComponent(
                    component_id="input_prompt",
                    component_type="input",
                    title="Prompt",
                    position=ComponentPosition.BOTTOM_CENTER,
                    height=8.0,
                    width=100.0,
                    interactive=True
                )
            ],
            grid_columns=1,
            grid_rows=4
        )
    
    @staticmethod
    def create_dag_3d_layout() -> LayoutDefinition:
        """Create 3D DAG visualization layout"""
        return LayoutDefinition(
            layout_id="dag_3d_view",
            name="3D DAG Visualization",
            layout_type=LayoutType.DAG_3D,
            description="3D DAG visualization with controls",
            theme="dark",
            components=[
                LayoutComponent(
                    component_id="canvas",
                    component_type="3d_canvas",
                    title="3D Canvas",
                    position=ComponentPosition.CENTER,
                    width=100.0,
                    height=100.0,
                    interactive=True,
                    draggable=True
                ),
                LayoutComponent(
                    component_id="controls_panel",
                    component_type="controls",
                    title="3D Controls",
                    position=ComponentPosition.TOP_RIGHT,
                    width=20.0,
                    height=30.0,
                    interactive=True
                ),
                LayoutComponent(
                    component_id="info_panel",
                    component_type="info",
                    title="Node Information",
                    position=ComponentPosition.BOTTOM_RIGHT,
                    width=25.0,
                    height=20.0,
                    collapsible=True
                )
            ]
        )
    
    @staticmethod
    def create_metrics_layout() -> LayoutDefinition:
        """Create metrics/monitoring layout"""
        return LayoutDefinition(
            layout_id="metrics_dashboard",
            name="Metrics Dashboard",
            layout_type=LayoutType.METRICS,
            description="Real-time metrics and monitoring",
            theme="dark",
            components=[
                LayoutComponent(
                    component_id="header",
                    component_type="header",
                    title="Header",
                    position=ComponentPosition.TOP_CENTER,
                    height=10.0,
                    width=100.0
                ),
                LayoutComponent(
                    component_id="sparklines",
                    component_type="sparklines",
                    title="Live Metrics",
                    position=ComponentPosition.TOP_CENTER,
                    width=100.0,
                    height=25.0
                ),
                LayoutComponent(
                    component_id="charts",
                    component_type="charts",
                    title="Detailed Charts",
                    position=ComponentPosition.CENTER,
                    width=100.0,
                    height=50.0,
                    resizable=True
                ),
                LayoutComponent(
                    component_id="alerts",
                    component_type="alerts",
                    title="Alerts & Notifications",
                    position=ComponentPosition.BOTTOM_CENTER,
                    width=100.0,
                    height=15.0
                )
            ],
            grid_columns=2,
            grid_rows=3
        )


# ============================================================================
# 🎨 LAYOUT MANAGER
# ============================================================================

class LayoutManager:
    """
    Complete Layout Management System
    Handles layout selection, customization, and rendering
    """
    
    def __init__(self):
        self.layouts: Dict[str, LayoutDefinition] = {}
        self.current_layout: Optional[LayoutDefinition] = None
        self.layout_history: List[str] = []
        
        # Load default layouts
        self._load_default_layouts()
        
        logger.info("🎨 Layout Manager initialized")
    
    def _load_default_layouts(self):
        """Load all default layout templates"""
        default_layouts = [
            LayoutTemplates.create_dashboard_layout(),
            LayoutTemplates.create_chat_layout(),
            LayoutTemplates.create_cli_layout(),
            LayoutTemplates.create_dag_3d_layout(),
            LayoutTemplates.create_metrics_layout()
        ]
        
        for layout in default_layouts:
            self.layouts[layout.layout_id] = layout
            logger.info(f"✅ Layout loaded: {layout.name}")
    
    def select_layout(self, layout_id: str) -> bool:
        """Select a layout"""
        if layout_id not in self.layouts:
            logger.warning(f"⚠️ Layout not found: {layout_id}")
            return False
        
        self.current_layout = self.layouts[layout_id]
        self.layout_history.append(layout_id)
        logger.info(f"🎯 Layout selected: {self.current_layout.name}")
        return True
    
    def auto_select_layout(self, context: str, device: str, user_preference: Optional[str] = None) -> bool:
        """Automatically select layout based on context"""
        # Decision matrix
        if user_preference and user_preference in self.layouts:
            return self.select_layout(user_preference)
        
        if context == "chat":
            return self.select_layout("chat_focused")
        elif context == "metrics":
            return self.select_layout("metrics_dashboard")
        elif context == "3d_dag":
            return self.select_layout("dag_3d_view")
        elif context == "cli":
            return self.select_layout("cli_terminal")
        else:
            return self.select_layout("dashboard_default")
    
    def create_custom_layout(self, layout_def: LayoutDefinition) -> bool:
        """Create custom layout"""
        if layout_def.layout_id in self.layouts:
            logger.warning(f"⚠️ Layout already exists: {layout_def.layout_id}")
            return False
        
        self.layouts[layout_def.layout_id] = layout_def
        logger.info(f"✅ Custom layout created: {layout_def.name}")
        return True
    
    def get_layout(self, layout_id: str) -> Optional[LayoutDefinition]:
        """Get layout by ID"""
        return self.layouts.get(layout_id)
    
    def get_current_layout(self) -> Optional[LayoutDefinition]:
        """Get currently active layout"""
        return self.current_layout
    
    def list_layouts(self) -> Dict[str, str]:
        """List all available layouts"""
        return {
            layout_id: layout.name
            for layout_id, layout in self.layouts.items()
        }
    
    def update_component(self, layout_id: str, component_id: str, updates: Dict[str, Any]) -> bool:
        """Update specific component in layout"""
        if layout_id not in self.layouts:
            return False
        
        layout = self.layouts[layout_id]
        for component in layout.components:
            if component.component_id == component_id:
                for key, value in updates.items():
                    if hasattr(component, key):
                        setattr(component, key, value)
                logger.info(f"✅ Component updated: {component_id} in {layout_id}")
                return True
        
        return False
    
    def export_layout(self, layout_id: str) -> Optional[Dict[str, Any]]:
        """Export layout definition"""
        if layout_id not in self.layouts:
            return None
        
        return self.layouts[layout_id].to_dict()
    
    def import_layout(self, layout_dict: Dict[str, Any]) -> bool:
        """Import layout definition"""
        try:
            layout_type = LayoutType[layout_dict.get("layout_type", "DASHBOARD").upper()]
            components = [
                LayoutComponent(
                    component_id=c.get("component_id", ""),
                    component_type=c.get("component_type", ""),
                    title=c.get("title", ""),
                    position=ComponentPosition[c.get("position", "CENTER").upper()] if "position" in c else ComponentPosition.CENTER,
                    **{k: v for k, v in c.items() if k not in ["component_id", "component_type", "title", "position"]}
                )
                for c in layout_dict.get("components", [])
            ]
            
            layout = LayoutDefinition(
                layout_id=layout_dict.get("layout_id", "imported_layout"),
                name=layout_dict.get("name", "Imported"),
                layout_type=layout_type,
                components=components,
                **{k: v for k, v in layout_dict.items() if k not in ["layout_id", "name", "layout_type", "components"]}
            )
            
            return self.create_custom_layout(layout)
        except Exception as e:
            logger.error(f"❌ Layout import failed: {e}")
            return False


# Singleton instance
layout_manager = LayoutManager()
