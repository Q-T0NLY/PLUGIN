"""
🎨 LAYOUT CONFIGURATION ENGINE
Ultra-Modern Responsive Layout System for Terminal & Web Interfaces
Supports dynamic auto-scaling, centering, responsive design, and module morphing
Production-grade with real-time adaptation
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import json
from datetime import datetime

logger = logging.getLogger("hyper_registry.layout_engine")


# ============================================================================
# 📐 LAYOUT ENUMS & CONSTANTS
# ============================================================================

class LayoutType(Enum):
    """Available layout templates"""
    # Primary layouts
    DASHBOARD = "dashboard"           # 3D quantum header + modules
    CHAT = "chat"                     # Chatbox + visual panel
    BUILDER = "builder"               # Workflow canvas + code + visuals
    ANALYTICS = "analytics"           # Metrics + charts + sparklines
    MONITOR = "monitor"               # Real-time observability + alerts
    SETTINGS = "settings"             # Configuration panels
    
    # Specialized layouts
    MINIMAL = "minimal"               # Single-module compact mode
    FULLSCREEN = "fullscreen"         # Immersive single-focus mode
    SPLIT_VIEW = "split_view"         # Dual-pane synchronized layout
    FLOATING = "floating"             # Floating draggable modules
    TABBED = "tabbed"                 # Tab-based module switching
    KANBAN = "kanban"                 # Task board layout


class ResponsiveBreakpoint(Enum):
    """Terminal/viewport size breakpoints"""
    MOBILE = 60                       # < 60 cols
    MOBILE_L = 100                    # 60-100 cols
    TABLET = 120                      # 100-120 cols
    DESKTOP = 160                     # 120-160 cols
    ULTRA_WIDE = 200                  # > 160 cols


class ModulePosition(Enum):
    """Module positioning strategies"""
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
    OVERLAY = "overlay"


class SizeMode(Enum):
    """Module sizing modes"""
    FIXED = "fixed"                   # Fixed pixel size
    PERCENTAGE = "percentage"         # Percentage of container
    AUTO = "auto"                     # Auto-fit to content
    FLEX = "flex"                     # Flex growth/shrink
    FILL = "fill"                     # Fill remaining space


# ============================================================================
# 📦 MODULE & LAYOUT CONFIGURATION
# ============================================================================

@dataclass
class ModuleSize:
    """Module size configuration"""
    width: float                      # pixels or percentage
    height: float                     # pixels or percentage
    width_mode: SizeMode = SizeMode.PERCENTAGE
    height_mode: SizeMode = SizeMode.PERCENTAGE
    min_width: Optional[float] = None
    max_width: Optional[float] = None
    min_height: Optional[float] = None
    max_height: Optional[float] = None
    
    def get_computed_size(
        self,
        container_width: int,
        container_height: int
    ) -> Tuple[int, int]:
        """Compute actual size based on container and mode"""
        
        # Calculate width
        if self.width_mode == SizeMode.PERCENTAGE:
            w = int(container_width * (self.width / 100))
        elif self.width_mode == SizeMode.AUTO:
            w = container_width
        else:  # FIXED
            w = int(self.width)
        
        # Calculate height
        if self.height_mode == SizeMode.PERCENTAGE:
            h = int(container_height * (self.height / 100))
        elif self.height_mode == SizeMode.AUTO:
            h = container_height
        else:  # FIXED
            h = int(self.height)
        
        # Apply constraints
        if self.min_width:
            w = max(w, int(self.min_width))
        if self.max_width:
            w = min(w, int(self.max_width))
        if self.min_height:
            h = max(h, int(self.min_height))
        if self.max_height:
            h = min(h, int(self.max_height))
        
        return (w, h)


@dataclass
class ModuleLayout:
    """Layout configuration for a single module"""
    module_id: str
    module_name: str
    module_type: str                  # "chat", "visuals", "metrics", etc.
    
    # Positioning
    position: ModulePosition = ModulePosition.TOP_LEFT
    offset_x: float = 0
    offset_y: float = 0
    
    # Sizing
    size: ModuleSize = field(default_factory=lambda: ModuleSize(50, 50))
    
    # Visibility & State
    visible: bool = True
    z_index: int = 1
    collapsed: bool = False
    focused: bool = False
    
    # Animation & Effects
    animation_enabled: bool = True
    fade_in_duration: float = 300    # ms
    transition_duration: float = 250  # ms
    
    # Styling
    border_style: str = "double"      # single, double, rounded, none
    shadow_enabled: bool = True
    glow_enabled: bool = True
    glow_color: str = "#00d9ff"
    
    # Content & Metadata
    title: str = ""
    icon: str = ""
    responsive_rules: Dict[ResponsiveBreakpoint, 'ModuleLayout'] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def get_responsive_layout(
        self,
        breakpoint: ResponsiveBreakpoint
    ) -> 'ModuleLayout':
        """Get responsive variant or fall back to default"""
        return self.responsive_rules.get(breakpoint, self)


@dataclass
class ContainerLayout:
    """Layout configuration for module containers/grids"""
    container_id: str
    layout_type: LayoutType
    
    # Grid/Container properties
    rows: int = 3
    cols: int = 3
    gap: float = 1.0                 # spacing between modules
    padding: float = 1.0
    
    # Modules in this container
    modules: List[ModuleLayout] = field(default_factory=list)
    
    # Responsive configuration
    responsive_breakpoints: Dict[ResponsiveBreakpoint, 'ContainerLayout'] = field(default_factory=dict)
    
    # Header configuration
    show_header: bool = True
    header_height: float = 3.0
    header_style: str = "quantum"     # quantum, minimal, gradient, none
    
    # Footer configuration
    show_footer: bool = True
    footer_height: float = 1.0
    footer_style: str = "telemetry"   # telemetry, status, none
    
    # Background & Theme
    background_color: str = "#0a0e27"
    accent_color: str = "#00d9ff"
    theme: str = "dark"
    
    # Metadata
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_module(self, module: ModuleLayout) -> None:
        """Add module to container"""
        self.modules.append(module)
        logger.info(f"📦 Module added: {module.module_id}")
    
    def remove_module(self, module_id: str) -> bool:
        """Remove module from container"""
        initial_count = len(self.modules)
        self.modules = [m for m in self.modules if m.module_id != module_id]
        removed = len(self.modules) < initial_count
        if removed:
            logger.info(f"🗑️ Module removed: {module_id}")
        return removed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "container_id": self.container_id,
            "layout_type": self.layout_type.value,
            "rows": self.rows,
            "cols": self.cols,
            "gap": self.gap,
            "padding": self.padding,
            "modules": [m.to_dict() for m in self.modules],
            "show_header": self.show_header,
            "header_height": self.header_height,
            "header_style": self.header_style,
            "show_footer": self.show_footer,
            "footer_height": self.footer_height,
            "footer_style": self.footer_style,
            "background_color": self.background_color,
            "accent_color": self.accent_color,
            "theme": self.theme,
            "metadata": self.metadata
        }


# ============================================================================
# 🎨 LAYOUT TEMPLATES
# ============================================================================

class LayoutTemplates:
    """Pre-built layout templates for common scenarios"""
    
    @staticmethod
    def create_dashboard_layout() -> ContainerLayout:
        """Create the quantum dashboard layout (as shown in your design)"""
        
        container = ContainerLayout(
            container_id="dashboard_main",
            layout_type=LayoutType.DASHBOARD,
            rows=4,
            cols=2,
            gap=1.0,
            padding=0.5,
            header_height=5.0,
            header_style="quantum",
            show_footer=True,
            footer_height=2.0,
            footer_style="telemetry",
            theme="dark"
        )
        
        # Header (auto-spans full width)
        header = ModuleLayout(
            module_id="header_quantum",
            module_name="Quantum Header",
            module_type="header",
            position=ModulePosition.TOP_CENTER,
            size=ModuleSize(100, 5, SizeMode.PERCENTAGE, SizeMode.FIXED),
            title="🚀 NEXUS AI STUDIO MATRIX v2.0 🚀",
            icon="🌌",
            glow_color="#00d9ff"
        )
        
        # System Metadata Panel
        metadata_panel = ModuleLayout(
            module_id="metadata",
            module_name="System Metadata",
            module_type="info",
            position=ModulePosition.TOP_LEFT,
            size=ModuleSize(50, 3, SizeMode.PERCENTAGE, SizeMode.FIXED),
            title="🧱 SYSTEM METADATA",
            border_style="rounded",
            glow_enabled=True
        )
        
        # Live Telemetry Panel
        telemetry = ModuleLayout(
            module_id="telemetry",
            module_name="Live Telemetry",
            module_type="metrics",
            position=ModulePosition.TOP_RIGHT,
            size=ModuleSize(50, 3, SizeMode.PERCENTAGE, SizeMode.FIXED),
            title="📊 LIVE TELEMETRY",
            border_style="rounded",
            glow_enabled=True
        )
        
        # Model Response Panel (Content Area)
        content = ModuleLayout(
            module_id="model_response",
            module_name="Model Response",
            module_type="content",
            position=ModulePosition.CENTER,
            size=ModuleSize(100, 15, SizeMode.PERCENTAGE, SizeMode.AUTO),
            title="📋 MODEL RESPONSE",
            border_style="double",
            glow_enabled=True
        )
        
        # Input Panel
        input_panel = ModuleLayout(
            module_id="input_panel",
            module_name="Input Field",
            module_type="input",
            position=ModulePosition.BOTTOM_CENTER,
            size=ModuleSize(100, 3, SizeMode.PERCENTAGE, SizeMode.FIXED),
            title="⌨️ ENTER YOUR PROMPT HERE",
            border_style="rounded"
        )
        
        container.add_module(header)
        container.add_module(metadata_panel)
        container.add_module(telemetry)
        container.add_module(content)
        container.add_module(input_panel)
        
        return container
    
    @staticmethod
    def create_chat_layout() -> ContainerLayout:
        """Create hybrid chat + visual panel layout"""
        
        container = ContainerLayout(
            container_id="chat_main",
            layout_type=LayoutType.CHAT,
            rows=3,
            cols=2,
            gap=1.0,
            padding=0.5,
            header_height=3.0,
            header_style="gradient",
            show_footer=True,
            footer_height=1.0,
            footer_style="status"
        )
        
        # Chat panel (left 30%)
        chat = ModuleLayout(
            module_id="chat_panel",
            module_name="Chat Bubble Module",
            module_type="chat",
            position=ModulePosition.CENTER_LEFT,
            size=ModuleSize(30, 100, SizeMode.PERCENTAGE, SizeMode.PERCENTAGE),
            title="💬 Chat",
            icon="💬",
            border_style="rounded",
            glow_color="#7c3aed"
        )
        
        # Visual panel (right 70%)
        visuals = ModuleLayout(
            module_id="visual_panel",
            module_name="Visual Reasoning Module",
            module_type="visuals",
            position=ModulePosition.CENTER_RIGHT,
            size=ModuleSize(70, 100, SizeMode.PERCENTAGE, SizeMode.PERCENTAGE),
            title="🎨 Visual Reasoning",
            icon="🎨",
            border_style="rounded",
            glow_color="#00d9ff"
        )
        
        container.add_module(chat)
        container.add_module(visuals)
        
        return container
    
    @staticmethod
    def create_builder_layout() -> ContainerLayout:
        """Create code + workflow + visuals builder layout"""
        
        container = ContainerLayout(
            container_id="builder_main",
            layout_type=LayoutType.BUILDER,
            rows=2,
            cols=3,
            gap=1.0,
            padding=0.5,
            header_height=3.0,
            show_footer=True,
            footer_height=2.0
        )
        
        # Workflow canvas (left)
        workflow = ModuleLayout(
            module_id="workflow_canvas",
            module_name="Workflow Canvas",
            module_type="workflow",
            position=ModulePosition.CENTER_LEFT,
            size=ModuleSize(33, 100, SizeMode.PERCENTAGE, SizeMode.PERCENTAGE),
            title="🧩 Workflow",
            border_style="double"
        )
        
        # Code editor (center)
        code = ModuleLayout(
            module_id="code_editor",
            module_name="Code Hub",
            module_type="code",
            position=ModulePosition.CENTER,
            size=ModuleSize(33, 100, SizeMode.PERCENTAGE, SizeMode.PERCENTAGE),
            title="💻 Code",
            border_style="double"
        )
        
        # Visual preview (right)
        preview = ModuleLayout(
            module_id="visual_preview",
            module_name="Visual Preview",
            module_type="visuals",
            position=ModulePosition.CENTER_RIGHT,
            size=ModuleSize(33, 100, SizeMode.PERCENTAGE, SizeMode.PERCENTAGE),
            title="🎨 Preview",
            border_style="double"
        )
        
        container.add_module(workflow)
        container.add_module(code)
        container.add_module(preview)
        
        return container
    
    @staticmethod
    def create_analytics_layout() -> ContainerLayout:
        """Create metrics + analytics layout"""
        
        container = ContainerLayout(
            container_id="analytics_main",
            layout_type=LayoutType.ANALYTICS,
            rows=3,
            cols=3,
            gap=0.5,
            padding=0.5,
            header_height=2.0,
            show_footer=True,
            footer_height=1.0
        )
        
        # Sparklines (top row, full width)
        sparklines = ModuleLayout(
            module_id="sparklines",
            module_name="Performance Metrics",
            module_type="metrics",
            position=ModulePosition.TOP_CENTER,
            size=ModuleSize(100, 2.5, SizeMode.PERCENTAGE, SizeMode.FIXED),
            title="📊 Live Sparklines",
            border_style="rounded"
        )
        
        # CPU/GPU (left)
        cpu_gpu = ModuleLayout(
            module_id="cpu_gpu",
            module_name="CPU/GPU Usage",
            module_type="metrics",
            position=ModulePosition.CENTER_LEFT,
            size=ModuleSize(33, 4, SizeMode.PERCENTAGE, SizeMode.AUTO),
            title="⚡ Compute",
            border_style="rounded"
        )
        
        # Model Status (center)
        model_status = ModuleLayout(
            module_id="model_status",
            module_name="Model Status",
            module_type="metrics",
            position=ModulePosition.CENTER,
            size=ModuleSize(33, 4, SizeMode.PERCENTAGE, SizeMode.AUTO),
            title="🤖 Models",
            border_style="rounded"
        )
        
        # Task Queue (right)
        task_queue = ModuleLayout(
            module_id="task_queue",
            module_name="Task Queue",
            module_type="metrics",
            position=ModulePosition.CENTER_RIGHT,
            size=ModuleSize(33, 4, SizeMode.PERCENTAGE, SizeMode.AUTO),
            title="🔄 Tasks",
            border_style="rounded"
        )
        
        container.add_module(sparklines)
        container.add_module(cpu_gpu)
        container.add_module(model_status)
        container.add_module(task_queue)
        
        return container


# ============================================================================
# 🎯 LAYOUT CONFIGURATION ENGINE
# ============================================================================

class LayoutConfigurationEngine:
    """
    Advanced Layout Configuration Engine
    Manages multiple layout types, responsive design, auto-scaling, and module morphing
    Production-grade with real-time adaptation
    """
    
    def __init__(self):
        self.layouts: Dict[str, ContainerLayout] = {}
        self.current_layout_id: Optional[str] = None
        self.responsive_breakpoint = ResponsiveBreakpoint.DESKTOP
        self.terminal_width = 160
        self.terminal_height = 40
        
        # Register default templates
        self._register_default_templates()
        
        logger.info("🎯 Layout Configuration Engine initialized")
    
    def _register_default_templates(self) -> None:
        """Register all default layout templates"""
        
        templates = {
            "dashboard": LayoutTemplates.create_dashboard_layout(),
            "chat": LayoutTemplates.create_chat_layout(),
            "builder": LayoutTemplates.create_builder_layout(),
            "analytics": LayoutTemplates.create_analytics_layout(),
        }
        
        for name, layout in templates.items():
            self.layouts[name] = layout
            logger.info(f"✅ Layout registered: {name}")
    
    def set_terminal_size(self, width: int, height: int) -> None:
        """Update terminal size and adapt layouts"""
        self.terminal_width = width
        self.terminal_height = height
        self._update_responsive_breakpoint()
        logger.info(f"📐 Terminal resized: {width}x{height}")
    
    def _update_responsive_breakpoint(self) -> None:
        """Update responsive breakpoint based on terminal width"""
        
        if self.terminal_width < ResponsiveBreakpoint.MOBILE.value:
            self.responsive_breakpoint = ResponsiveBreakpoint.MOBILE
        elif self.terminal_width < ResponsiveBreakpoint.MOBILE_L.value:
            self.responsive_breakpoint = ResponsiveBreakpoint.MOBILE_L
        elif self.terminal_width < ResponsiveBreakpoint.TABLET.value:
            self.responsive_breakpoint = ResponsiveBreakpoint.TABLET
        elif self.terminal_width < ResponsiveBreakpoint.DESKTOP.value:
            self.responsive_breakpoint = ResponsiveBreakpoint.DESKTOP
        else:
            self.responsive_breakpoint = ResponsiveBreakpoint.ULTRA_WIDE
    
    def create_custom_layout(
        self,
        layout_id: str,
        layout_type: LayoutType,
        modules: List[Tuple[str, str, str, ModuleLayout]]  # (id, name, type, config)
    ) -> ContainerLayout:
        """Create a custom layout from scratch"""
        
        container = ContainerLayout(
            container_id=layout_id,
            layout_type=layout_type,
            rows=3,
            cols=2,
            header_height=3.0,
            show_header=True,
            show_footer=True,
            footer_height=1.0
        )
        
        for module_id, name, m_type, config in modules:
            module = ModuleLayout(
                module_id=module_id,
                module_name=name,
                module_type=m_type,
                **asdict(config)
            )
            container.add_module(module)
        
        self.layouts[layout_id] = container
        logger.info(f"🎨 Custom layout created: {layout_id}")
        return container
    
    def get_layout(self, layout_id: str) -> Optional[ContainerLayout]:
        """Get layout by ID"""
        return self.layouts.get(layout_id)
    
    def switch_layout(self, layout_id: str) -> bool:
        """Switch to a different layout"""
        if layout_id not in self.layouts:
            logger.warning(f"⚠️ Layout not found: {layout_id}")
            return False
        
        self.current_layout_id = layout_id
        logger.info(f"🔄 Layout switched to: {layout_id}")
        return True
    
    def compute_module_geometry(
        self,
        layout_id: str,
        module_id: str
    ) -> Optional[Dict[str, int]]:
        """Compute actual geometry for a module"""
        
        layout = self.get_layout(layout_id)
        if not layout:
            return None
        
        module = next(
            (m for m in layout.modules if m.module_id == module_id),
            None
        )
        
        if not module:
            return None
        
        width, height = module.size.get_computed_size(
            self.terminal_width,
            self.terminal_height
        )
        
        return {
            "module_id": module_id,
            "width": width,
            "height": height,
            "x": 0,  # Would be computed from position
            "y": 0,  # Would be computed from position
            "z_index": module.z_index
        }
    
    def get_layout_structure(self, layout_id: str) -> Dict[str, Any]:
        """Get complete layout structure for rendering"""
        
        layout = self.get_layout(layout_id)
        if not layout:
            return {}
        
        return {
            "container_id": layout.container_id,
            "layout_type": layout.layout_type.value,
            "terminal_width": self.terminal_width,
            "terminal_height": self.terminal_height,
            "breakpoint": self.responsive_breakpoint.name,
            "header": {
                "visible": layout.show_header,
                "height": layout.header_height,
                "style": layout.header_style
            },
            "footer": {
                "visible": layout.show_footer,
                "height": layout.footer_height,
                "style": layout.footer_style
            },
            "modules": [
                {
                    "id": m.module_id,
                    "name": m.module_name,
                    "type": m.module_type,
                    "title": m.title,
                    "position": m.position.value,
                    "visible": m.visible,
                    "collapsed": m.collapsed,
                    "focused": m.focused,
                    "geometry": self.compute_module_geometry(layout_id, m.module_id)
                }
                for m in layout.modules
            ]
        }
    
    def export_layout_config(self, layout_id: str) -> Optional[str]:
        """Export layout as JSON"""
        layout = self.get_layout(layout_id)
        if not layout:
            return None
        
        return json.dumps(layout.to_dict(), indent=2)
    
    def import_layout_config(self, layout_id: str, config_json: str) -> bool:
        """Import layout from JSON"""
        try:
            config = json.loads(config_json)
            # Parse and create layout from config
            # TODO: Full parser implementation
            return True
        except Exception as e:
            logger.error(f"❌ Failed to import layout: {e}")
            return False
    
    def list_available_layouts(self) -> Dict[str, str]:
        """List all available layouts"""
        return {
            layout_id: layout.layout_type.value
            for layout_id, layout in self.layouts.items()
        }


# Singleton instance
layout_engine = LayoutConfigurationEngine()
