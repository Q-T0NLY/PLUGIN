"""
🎨 ULTRA-MODERN VISUALS ENGINE
3D Graphics, Animations, Emojis, Colors, and Advanced Rendering
Production-Grade Visual System for All Outputs
"""

import json
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger("hyper_registry.visuals_engine")

# ============================================================================
# 🎨 COLOR PALETTES & THEMES
# ============================================================================

class ColorPalette(Enum):
    """Ultra-modern color palettes for professional output"""
    # Primary Dark Theme (production)
    PRIMARY_DARK = {
        "bg": "#0a0e27",
        "surface": "#1a1f3a",
        "accent": "#00d9ff",
        "accent_alt": "#7c3aed",
        "text_primary": "#ffffff",
        "text_secondary": "#a0aec0",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    # Cyberpunk Neon
    CYBERPUNK = {
        "bg": "#0d0221",
        "surface": "#1a0033",
        "accent": "#ff006e",
        "accent_alt": "#00f5ff",
        "text_primary": "#ffffff",
        "text_secondary": "#b0b0b0",
        "success": "#00ff41",
        "warning": "#ffbe0b",
        "error": "#ff006e",
        "info": "#00d9ff"
    }
    
    # Glassmorphism
    GLASS = {
        "bg": "rgba(10, 14, 39, 0.8)",
        "surface": "rgba(26, 31, 58, 0.6)",
        "accent": "#00d9ff",
        "accent_alt": "#7c3aed",
        "text_primary": "#ffffff",
        "text_secondary": "#d0d0ff",
        "success": "#4ade80",
        "warning": "#facc15",
        "error": "#ff6b6b",
        "info": "#60a5fa"
    }
    
    # Gradient Flow
    GRADIENT = {
        "bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "surface": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "accent": "#00d9ff",
        "accent_alt": "#ffd89b",
        "text_primary": "#ffffff",
        "text_secondary": "#f0f0f0",
        "success": "#52c41a",
        "warning": "#fa8c16",
        "error": "#f5222d",
        "info": "#1890ff"
    }


class AnimationStyle(Enum):
    """Ultra-modern animation styles"""
    # Smooth & Fluid
    SMOOTH = "cubic-bezier(0.25, 0.46, 0.45, 0.94)"
    BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    ELASTIC = "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    
    # Fast & Snappy
    SNAPPY = "cubic-bezier(0.34, 1.56, 0.64, 1)"
    QUICK = "cubic-bezier(0.6, 0.04, 0.98, 0.34)"
    
    # Slow & Dramatic
    DRAMATIC = "cubic-bezier(0.25, 0.46, 0.45, 0.94)"
    EASE_IN = "cubic-bezier(0.42, 0, 1, 1)"
    EASE_OUT = "cubic-bezier(0, 0, 0.58, 1)"


class VisualComponentType(Enum):
    """Component types with visual representations"""
    # 3D Components
    CUBE_3D = "🎲 3D Cube"
    SPHERE_3D = "🔮 3D Sphere"
    PYRAMID_3D = "🔺 3D Pyramid"
    TORUS_3D = "🍩 3D Torus"
    
    # UI Components
    CARD = "📇 Card"
    PANEL = "📦 Panel"
    MODAL = "🪟 Modal"
    DROPDOWN = "▼ Dropdown"
    BUTTON = "🔘 Button"
    INPUT = "📝 Input"
    TOGGLE = "🔲 Toggle"
    SLIDER = "🎚️ Slider"
    
    # Data Visualization
    CHART_BAR = "📊 Bar Chart"
    CHART_LINE = "📈 Line Chart"
    CHART_PIE = "🥧 Pie Chart"
    CHART_SCATTER = "📍 Scatter"
    GAUGE = "🎯 Gauge"
    HEATMAP = "🔥 Heatmap"
    
    # Container
    GRID = "⊞ Grid"
    FLEX = "⟷ Flex"
    STACK = "⬆ Stack"
    SCROLL = "↕️ Scroll"


# ============================================================================
# 🎬 ANIMATION DEFINITIONS
# ============================================================================

@dataclass
class Animation:
    """Animation configuration"""
    name: str
    duration: float  # milliseconds
    delay: float = 0.0
    easing: AnimationStyle = AnimationStyle.SMOOTH
    repeat: int = 1  # -1 for infinite
    direction: str = "normal"  # normal, reverse, alternate, alternate-reverse
    fill_mode: str = "both"  # none, forwards, backwards, both
    
    def to_css(self) -> str:
        """Generate CSS animation string"""
        return f"{self.name} {self.duration}ms {self.easing.value} {self.delay}ms {self.direction} {self.fill_mode}"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AnimationLibrary:
    """Pre-built animation definitions"""
    
    FADE_IN = Animation("fadeIn", 600, 0, AnimationStyle.EASE_OUT)
    FADE_OUT = Animation("fadeOut", 600, 0, AnimationStyle.EASE_IN)
    
    SLIDE_UP = Animation("slideUp", 500, 0, AnimationStyle.SMOOTH)
    SLIDE_DOWN = Animation("slideDown", 500, 0, AnimationStyle.SMOOTH)
    SLIDE_LEFT = Animation("slideLeft", 500, 0, AnimationStyle.SMOOTH)
    SLIDE_RIGHT = Animation("slideRight", 500, 0, AnimationStyle.SMOOTH)
    
    SCALE_UP = Animation("scaleUp", 400, 0, AnimationStyle.BOUNCE)
    SCALE_DOWN = Animation("scaleDown", 400, 0, AnimationStyle.BOUNCE)
    
    ROTATE = Animation("rotate", 1000, 0, AnimationStyle.SMOOTH, repeat=-1)
    PULSE = Animation("pulse", 2000, 0, AnimationStyle.SMOOTH, repeat=-1)
    GLOW = Animation("glow", 2000, 0, AnimationStyle.SMOOTH, repeat=-1)
    
    FLIP_IN = Animation("flipIn", 600, 0, AnimationStyle.BOUNCE)
    FLIP_OUT = Animation("flipOut", 600, 0, AnimationStyle.BOUNCE)
    
    BOUNCE_IN = Animation("bounceIn", 700, 0, AnimationStyle.BOUNCE)
    BOUNCE_OUT = Animation("bounceOut", 700, 0, AnimationStyle.BOUNCE)
    
    MORPH = Animation("morph", 1500, 0, AnimationStyle.SMOOTH)
    LIQUID = Animation("liquid", 3000, 0, AnimationStyle.SMOOTH, repeat=-1)


# ============================================================================
# 🎨 GRADIENT EFFECTS
# ============================================================================

@dataclass
class GradientEffect:
    """Gradient effect definition"""
    type: str  # linear, radial, conic
    angle: float = 45.0  # degrees
    colors: List[Tuple[str, float]] = field(default_factory=list)  # (color, stop%)
    animation: Optional[Animation] = None
    
    def to_css(self) -> str:
        """Generate CSS gradient"""
        color_stops = ", ".join([f"{color} {stop}%" for color, stop in self.colors])
        
        if self.type == "linear":
            return f"linear-gradient({self.angle}deg, {color_stops})"
        elif self.type == "radial":
            return f"radial-gradient(circle, {color_stops})"
        elif self.type == "conic":
            return f"conic-gradient({color_stops})"
        
        return f"linear-gradient({self.angle}deg, {color_stops})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "angle": self.angle,
            "colors": self.colors,
            "animation": self.animation.to_dict() if self.animation else None
        }


# ============================================================================
# 🎭 3D EFFECTS & TRANSFORMS
# ============================================================================

@dataclass
class Transform3D:
    """3D transform configuration"""
    rotate_x: float = 0.0  # degrees
    rotate_y: float = 0.0
    rotate_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    translate_x: float = 0.0  # pixels
    translate_y: float = 0.0
    translate_z: float = 0.0
    skew_x: float = 0.0  # degrees
    skew_y: float = 0.0
    perspective: float = 1000.0  # pixels
    
    def to_css(self) -> str:
        """Generate CSS 3D transform"""
        transforms = [
            f"perspective({self.perspective}px)",
            f"rotateX({self.rotate_x}deg)",
            f"rotateY({self.rotate_y}deg)",
            f"rotateZ({self.rotate_z}deg)",
            f"scaleX({self.scale_x})",
            f"scaleY({self.scale_y})",
            f"scaleZ({self.scale_z})",
            f"translateX({self.translate_x}px)",
            f"translateY({self.translate_y}px)",
            f"translateZ({self.translate_z}px)",
            f"skewX({self.skew_x}deg)",
            f"skewY({self.skew_y}deg)"
        ]
        return " ".join(transforms)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# 🌐 VISUAL COMPONENT DEFINITION
# ============================================================================

@dataclass
class VisualComponent:
    """Complete visual component definition"""
    id: str
    type: VisualComponentType
    title: str
    description: str = ""
    
    # Styling
    color_palette: ColorPalette = ColorPalette.PRIMARY_DARK
    background_color: str = ""
    accent_color: str = ""
    border_color: str = ""
    border_width: float = 1.0
    border_radius: float = 8.0
    
    # Dimensions
    width: Optional[float] = None  # percentage or pixels
    height: Optional[float] = None
    padding: float = 16.0
    margin: float = 8.0
    
    # Effects
    shadow: bool = True
    shadow_blur: float = 10.0
    shadow_color: str = "rgba(0, 0, 0, 0.3)"
    
    blur_effect: float = 0.0  # 0-100
    opacity: float = 1.0
    
    # Animation
    animations: List[Animation] = field(default_factory=list)
    hover_animation: Optional[Animation] = None
    on_focus_animation: Optional[Animation] = None
    
    # 3D
    transform_3d: Optional[Transform3D] = None
    perspective_enabled: bool = False
    
    # Gradient
    gradient: Optional[GradientEffect] = None
    
    # Content
    icon: str = ""  # emoji or icon code
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "styling": {
                "color_palette": self.color_palette.name,
                "background_color": self.background_color,
                "accent_color": self.accent_color,
                "border_color": self.border_color,
                "border_width": self.border_width,
                "border_radius": self.border_radius
            },
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "padding": self.padding,
                "margin": self.margin
            },
            "effects": {
                "shadow": self.shadow,
                "shadow_blur": self.shadow_blur,
                "blur_effect": self.blur_effect,
                "opacity": self.opacity
            },
            "animations": [a.to_dict() for a in self.animations],
            "hover_animation": self.hover_animation.to_dict() if self.hover_animation else None,
            "transform_3d": self.transform_3d.to_dict() if self.transform_3d else None,
            "gradient": self.gradient.to_dict() if self.gradient else None,
            "icon": self.icon,
            "content": self.content,
            "metadata": self.metadata
        }


# ============================================================================
# 🎨 VISUALS ENGINE
# ============================================================================

class VisualsEngine:
    """
    Ultra-Modern Visuals Engine
    Manages all visual components, animations, colors, and 3D rendering
    """
    
    def __init__(self):
        self.components: Dict[str, VisualComponent] = {}
        self.color_palettes = ColorPalette
        self.animation_library = AnimationLibrary
        logger.info("🎨 Visuals Engine initialized")
    
    def create_component(
        self,
        component_id: str,
        component_type: VisualComponentType,
        title: str,
        description: str = "",
        color_palette: ColorPalette = ColorPalette.PRIMARY_DARK,
        animations: Optional[List[Animation]] = None,
        **kwargs
    ) -> VisualComponent:
        """Create a new visual component"""
        
        component = VisualComponent(
            id=component_id,
            type=component_type,
            title=title,
            description=description,
            color_palette=color_palette,
            animations=animations or [],
            **kwargs
        )
        
        self.components[component_id] = component
        logger.info(f"🎨 Visual component created: {component_id} ({component_type.value})")
        return component
    
    def apply_animation(
        self,
        component_id: str,
        animation: Animation,
        trigger: str = "default"  # default, hover, focus, scroll
    ) -> bool:
        """Apply animation to component"""
        
        if component_id not in self.components:
            logger.warning(f"⚠️ Component not found: {component_id}")
            return False
        
        component = self.components[component_id]
        
        if trigger == "default":
            component.animations.append(animation)
        elif trigger == "hover":
            component.hover_animation = animation
        elif trigger == "focus":
            component.on_focus_animation = animation
        
        logger.info(f"✅ Animation applied to {component_id}: {animation.name}")
        return True
    
    def apply_gradient(
        self,
        component_id: str,
        gradient: GradientEffect
    ) -> bool:
        """Apply gradient effect to component"""
        
        if component_id not in self.components:
            return False
        
        self.components[component_id].gradient = gradient
        logger.info(f"✅ Gradient applied to {component_id}")
        return True
    
    def apply_3d_transform(
        self,
        component_id: str,
        transform: Transform3D
    ) -> bool:
        """Apply 3D transform to component"""
        
        if component_id not in self.components:
            return False
        
        self.components[component_id].transform_3d = transform
        self.components[component_id].perspective_enabled = True
        logger.info(f"✅ 3D transform applied to {component_id}")
        return True
    
    def get_component(self, component_id: str) -> Optional[VisualComponent]:
        """Retrieve visual component"""
        return self.components.get(component_id)
    
    def get_all_components(self) -> Dict[str, VisualComponent]:
        """Get all registered components"""
        return self.components.copy()
    
    def export_css(self, component_id: str) -> str:
        """Export CSS for component"""
        
        component = self.get_component(component_id)
        if not component:
            return ""
        
        css_parts = [f"/* Component: {component.id} */"]
        css_parts.append(f".component-{component.id} {{")
        
        # Base styles
        palette = component.color_palette.value
        if isinstance(palette, dict):
            css_parts.append(f"  background-color: {palette.get('bg', 'transparent')};")
            css_parts.append(f"  color: {palette.get('text_primary', '#fff')};")
        
        if component.width:
            css_parts.append(f"  width: {component.width}px;")
        if component.height:
            css_parts.append(f"  height: {component.height}px;")
        
        css_parts.append(f"  padding: {component.padding}px;")
        css_parts.append(f"  margin: {component.margin}px;")
        css_parts.append(f"  border-radius: {component.border_radius}px;")
        css_parts.append(f"  opacity: {component.opacity};")
        
        # Shadow
        if component.shadow:
            css_parts.append(
                f"  box-shadow: 0 8px {component.shadow_blur}px {component.shadow_color};"
            )
        
        # 3D Transform
        if component.transform_3d:
            css_parts.append(f"  transform: {component.transform_3d.to_css()};")
            css_parts.append(f"  perspective: {component.transform_3d.perspective}px;")
        
        # Gradient
        if component.gradient:
            css_parts.append(f"  background: {component.gradient.to_css()};")
        
        # Animations
        if component.animations:
            anim_str = ", ".join([a.to_css() for a in component.animations])
            css_parts.append(f"  animation: {anim_str};")
        
        css_parts.append("}")
        
        return "\n".join(css_parts)
    
    def generate_design_system(self) -> Dict[str, Any]:
        """Generate complete design system JSON"""
        
        return {
            "version": "1.0.0",
            "color_palettes": {
                name.name: name.value for name in ColorPalette
            },
            "animation_library": {
                name: getattr(AnimationLibrary, name).to_dict()
                for name in dir(AnimationLibrary)
                if not name.startswith("_") and isinstance(getattr(AnimationLibrary, name), Animation)
            },
            "component_types": {
                name.name: name.value for name in VisualComponentType
            },
            "components": {
                cid: comp.to_dict() for cid, comp in self.components.items()
            }
        }


# Singleton instance
visuals_engine = VisualsEngine()
