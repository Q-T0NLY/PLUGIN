"""
✨ VISUAL STYLING ENGINE
Comprehensive styling with 3D effects, animations, gradients, emojis
Integrated with layouts and production-grade rendering
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
import json
from datetime import datetime

logger = logging.getLogger("hyper_registry.visual_styling")


# ============================================================================
# 🎨 VISUAL EFFECT ENUMS
# ============================================================================

class ShadowStyle(Enum):
    """Shadow effect styles"""
    NONE = "none"
    SOFT = "soft"                    # Subtle blur
    HARD = "hard"                    # Sharp edges
    DEEP = "deep"                    # 3D depth effect
    NEON = "neon"                    # Glowing shadow
    FLOATING = "floating"            # Elevation effect


class BorderStyle(Enum):
    """Border rendering styles"""
    NONE = "none"
    SINGLE = "single"                # Single line
    DOUBLE = "double"                # Double line
    ROUNDED = "rounded"              # Rounded corners
    BOLD = "bold"                    # Thick border
    NEON = "neon"                    # Glowing border
    GRADIENT = "gradient"            # Color gradient border


class GlowIntensity(Enum):
    """Glow effect intensity"""
    OFF = 0
    SUBTLE = 1
    MEDIUM = 2
    STRONG = 3
    INTENSE = 4


class AnimationType(Enum):
    """Animation types for UI elements"""
    NONE = "none"
    FADE = "fade"
    SLIDE = "slide"
    BOUNCE = "bounce"
    PULSE = "pulse"
    ROTATE = "rotate"
    FLIP = "flip"
    MORPH = "morph"
    SHIMMER = "shimmer"
    GLOW_PULSE = "glow_pulse"
    PARTICLE_FLOW = "particle_flow"


class VisualLayer(Enum):
    """Visual rendering layers"""
    BACKGROUND = 0
    SHADOW = 1
    BORDER = 2
    CONTENT = 3
    OVERLAY = 4
    GLOW = 5
    PARTICLES = 6
    FOCUS = 7


# ============================================================================
# 🎬 ANIMATION DEFINITIONS
# ============================================================================

@dataclass
class AnimationConfig:
    """Complete animation configuration"""
    type: AnimationType = AnimationType.NONE
    duration: float = 300            # milliseconds
    delay: float = 0
    repeat: int = 1                  # -1 = infinite
    easing: str = "ease-out"         # ease-in, ease-out, ease-in-out, linear
    direction: str = "forward"       # forward, reverse, alternate
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParticleEffect:
    """Particle effect configuration"""
    enabled: bool = False
    type: str = "sparkles"           # sparkles, dots, waves, orbital
    count: int = 10
    speed: float = 1.0
    direction: str = "up"            # up, down, left, right, orbital, random
    color: str = "#00d9ff"
    size: float = 1.0
    lifetime: float = 2.0            # seconds
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# 🎨 GRADIENT CONFIGURATION
# ============================================================================

@dataclass
class GradientStop:
    """Single gradient color stop"""
    color: str
    position: float               # 0.0 to 1.0
    intensity: float = 1.0


@dataclass
class GradientConfig:
    """Gradient effect configuration"""
    enabled: bool = False
    type: str = "linear"             # linear, radial, conic
    angle: float = 45.0              # degrees for linear
    stops: List[GradientStop] = field(default_factory=list)
    animation: Optional[AnimationConfig] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "type": self.type,
            "angle": self.angle,
            "stops": [asdict(s) for s in self.stops],
            "animation": self.animation.to_dict() if self.animation else None
        }


# ============================================================================
# 🌈 VISUAL STYLING CONFIGURATION
# ============================================================================

@dataclass
class VisualStyle:
    """Complete visual styling for a UI element"""
    element_id: str
    element_name: str
    
    # Colors
    foreground_color: str = "#ffffff"
    background_color: str = "#0a0e27"
    accent_color: str = "#00d9ff"
    border_color: str = "#00d9ff"
    shadow_color: str = "rgba(0, 0, 0, 0.3)"
    
    # Border
    border_style: BorderStyle = BorderStyle.ROUNDED
    border_width: float = 1.0
    border_radius: float = 8.0
    
    # Shadow & Depth
    shadow_style: ShadowStyle = ShadowStyle.SOFT
    shadow_blur: float = 10.0
    shadow_offset_x: float = 0
    shadow_offset_y: float = 2.0
    shadow_spread: float = 0
    
    # Glow
    glow_enabled: bool = True
    glow_color: str = "#00d9ff"
    glow_intensity: GlowIntensity = GlowIntensity.MEDIUM
    glow_blur: float = 15.0
    
    # Effects
    blur_amount: float = 0.0          # 0-100
    opacity: float = 1.0              # 0-1
    saturation: float = 1.0           # 0-2
    brightness: float = 1.0           # 0-2
    
    # Gradient
    gradient: GradientConfig = field(default_factory=GradientConfig)
    
    # Animations
    idle_animation: AnimationConfig = field(default_factory=AnimationConfig)
    hover_animation: AnimationConfig = field(default_factory=AnimationConfig)
    focus_animation: AnimationConfig = field(default_factory=AnimationConfig)
    active_animation: AnimationConfig = field(default_factory=AnimationConfig)
    
    # Particles
    particles: ParticleEffect = field(default_factory=ParticleEffect)
    
    # 3D Effects
    perspective: float = 1000.0
    rotate_x: float = 0.0
    rotate_y: float = 0.0
    rotate_z: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    scale_z: float = 1.0
    
    # Transitions
    transition_duration: float = 250  # ms
    transition_easing: str = "ease-out"
    
    # Metadata
    description: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "element_name": self.element_name,
            "colors": {
                "foreground": self.foreground_color,
                "background": self.background_color,
                "accent": self.accent_color,
                "border": self.border_color,
                "shadow": self.shadow_color
            },
            "border": {
                "style": self.border_style.value,
                "width": self.border_width,
                "radius": self.border_radius
            },
            "shadow": {
                "style": self.shadow_style.value,
                "blur": self.shadow_blur,
                "offset": [self.shadow_offset_x, self.shadow_offset_y],
                "spread": self.shadow_spread,
                "color": self.shadow_color
            },
            "glow": {
                "enabled": self.glow_enabled,
                "color": self.glow_color,
                "intensity": self.glow_intensity.value,
                "blur": self.glow_blur
            },
            "effects": {
                "blur": self.blur_amount,
                "opacity": self.opacity,
                "saturation": self.saturation,
                "brightness": self.brightness
            },
            "gradient": self.gradient.to_dict(),
            "animations": {
                "idle": self.idle_animation.to_dict(),
                "hover": self.hover_animation.to_dict(),
                "focus": self.focus_animation.to_dict(),
                "active": self.active_animation.to_dict()
            },
            "particles": self.particles.to_dict(),
            "3d": {
                "perspective": self.perspective,
                "rotateX": self.rotate_x,
                "rotateY": self.rotate_y,
                "rotateZ": self.rotate_z,
                "scaleX": self.scale_x,
                "scaleY": self.scale_y,
                "scaleZ": self.scale_z
            },
            "transitions": {
                "duration": self.transition_duration,
                "easing": self.transition_easing
            }
        }


# ============================================================================
# 🎨 VISUAL STYLE THEMES
# ============================================================================

class StyleThemes:
    """Pre-built visual style themes"""
    
    @staticmethod
    def create_quantum_theme() -> Dict[str, VisualStyle]:
        """Create quantum/cyberpunk theme"""
        
        return {
            "default": VisualStyle(
                element_id="default",
                element_name="Default Element",
                foreground_color="#ffffff",
                background_color="#0a0e27",
                accent_color="#00d9ff",
                border_color="#00d9ff",
                border_style=BorderStyle.NEON,
                glow_enabled=True,
                glow_color="#00d9ff",
                glow_intensity=GlowIntensity.MEDIUM,
                shadow_style=ShadowStyle.NEON
            ),
            "header": VisualStyle(
                element_id="header",
                element_name="Header Element",
                background_color="#1a1f3a",
                accent_color="#7c3aed",
                border_style=BorderStyle.DOUBLE,
                glow_enabled=True,
                glow_color="#7c3aed",
                particles=ParticleEffect(
                    enabled=True,
                    type="sparkles",
                    color="#00d9ff"
                ),
                gradient=GradientConfig(
                    enabled=True,
                    type="linear",
                    angle=45.0,
                    stops=[
                        GradientStop("#00d9ff", 0.0),
                        GradientStop("#7c3aed", 0.5),
                        GradientStop("#ff00ff", 1.0)
                    ]
                )
            ),
            "button": VisualStyle(
                element_id="button",
                element_name="Button Element",
                background_color="transparent",
                foreground_color="#00d9ff",
                border_color="#00d9ff",
                border_style=BorderStyle.ROUNDED,
                glow_enabled=True,
                hover_animation=AnimationConfig(
                    type=AnimationType.GLOW_PULSE,
                    duration=200
                ),
                active_animation=AnimationConfig(
                    type=AnimationType.BOUNCE,
                    duration=150
                )
            ),
            "panel": VisualStyle(
                element_id="panel",
                element_name="Panel Element",
                background_color="#1a1f3a",
                border_style=BorderStyle.ROUNDED,
                border_color="#00d9ff",
                shadow_style=ShadowStyle.DEEP,
                glow_enabled=True,
                glow_intensity=GlowIntensity.SUBTLE,
                idle_animation=AnimationConfig(
                    type=AnimationType.PULSE,
                    duration=3000,
                    repeat=-1
                )
            ),
            "success": VisualStyle(
                element_id="success",
                element_name="Success Indicator",
                foreground_color="#10b981",
                border_color="#10b981",
                glow_color="#10b981",
                glow_enabled=True,
                particles=ParticleEffect(
                    enabled=True,
                    type="sparkles",
                    color="#10b981",
                    count=5
                )
            ),
            "error": VisualStyle(
                element_id="error",
                element_name="Error Indicator",
                foreground_color="#ef4444",
                border_color="#ef4444",
                glow_color="#ef4444",
                glow_enabled=True,
                glow_intensity=GlowIntensity.STRONG,
                idle_animation=AnimationConfig(
                    type=AnimationType.PULSE,
                    duration=500,
                    repeat=-1
                )
            ),
            "warning": VisualStyle(
                element_id="warning",
                element_name="Warning Indicator",
                foreground_color="#f59e0b",
                border_color="#f59e0b",
                glow_color="#f59e0b",
                glow_enabled=True,
                glow_intensity=GlowIntensity.MEDIUM
            ),
            "info": VisualStyle(
                element_id="info",
                element_name="Info Indicator",
                foreground_color="#3b82f6",
                border_color="#3b82f6",
                glow_color="#3b82f6",
                glow_enabled=True
            )
        }
    
    @staticmethod
    def create_glassmorphism_theme() -> Dict[str, VisualStyle]:
        """Create glassmorphism theme with transparency and blur"""
        
        return {
            "default": VisualStyle(
                element_id="default",
                element_name="Default Element",
                background_color="rgba(26, 31, 58, 0.6)",
                border_color="#00d9ff",
                border_style=BorderStyle.ROUNDED,
                blur_amount=10.0,
                opacity=0.9,
                glow_enabled=True,
                glow_intensity=GlowIntensity.SUBTLE,
                shadow_style=ShadowStyle.SOFT
            ),
            "panel": VisualStyle(
                element_id="panel",
                element_name="Panel Element",
                background_color="rgba(26, 31, 58, 0.5)",
                border_style=BorderStyle.ROUNDED,
                blur_amount=20.0,
                opacity=0.8,
                glow_enabled=False,
                shadow_style=ShadowStyle.SOFT
            )
        }
    
    @staticmethod
    def create_minimal_theme() -> Dict[str, VisualStyle]:
        """Create minimal clean theme"""
        
        return {
            "default": VisualStyle(
                element_id="default",
                element_name="Default Element",
                foreground_color="#1f2937",
                background_color="#ffffff",
                accent_color="#2563eb",
                border_style=BorderStyle.SINGLE,
                border_color="#e5e7eb",
                glow_enabled=False,
                shadow_style=ShadowStyle.SOFT,
                shadow_blur=4.0
            )
        }


# ============================================================================
# 🎯 VISUAL STYLING ENGINE
# ============================================================================

class VisualStylingEngine:
    """
    Visual Styling Engine
    Manages all visual effects, animations, 3D transforms, particles, and gradients
    Production-grade with real-time rendering
    """
    
    def __init__(self):
        self.styles: Dict[str, VisualStyle] = {}
        self.active_theme: str = "quantum"
        self.themes: Dict[str, Dict[str, VisualStyle]] = {
            "quantum": StyleThemes.create_quantum_theme(),
            "glassmorphism": StyleThemes.create_glassmorphism_theme(),
            "minimal": StyleThemes.create_minimal_theme()
        }
        
        # Load default theme
        self._load_theme("quantum")
        
        logger.info("🎨 Visual Styling Engine initialized")
    
    def _load_theme(self, theme_name: str) -> bool:
        """Load a theme into active styles"""
        if theme_name not in self.themes:
            logger.warning(f"⚠️ Theme not found: {theme_name}")
            return False
        
        self.active_theme = theme_name
        self.styles.clear()
        self.styles.update(self.themes[theme_name])
        logger.info(f"🎨 Theme loaded: {theme_name}")
        return True
    
    def set_theme(self, theme_name: str) -> bool:
        """Switch to a different theme"""
        return self._load_theme(theme_name)
    
    def create_style(
        self,
        element_id: str,
        element_name: str,
        **kwargs
    ) -> VisualStyle:
        """Create a new custom visual style"""
        
        style = VisualStyle(
            element_id=element_id,
            element_name=element_name,
            **kwargs
        )
        
        self.styles[element_id] = style
        logger.info(f"✨ Visual style created: {element_id}")
        return style
    
    def get_style(self, element_id: str) -> Optional[VisualStyle]:
        """Get style by element ID"""
        return self.styles.get(element_id)
    
    def apply_animation(
        self,
        element_id: str,
        animation_type: AnimationType,
        trigger: str = "idle"  # idle, hover, focus, active
    ) -> bool:
        """Apply animation to a styled element"""
        
        style = self.get_style(element_id)
        if not style:
            logger.warning(f"⚠️ Style not found: {element_id}")
            return False
        
        anim = AnimationConfig(type=animation_type)
        
        if trigger == "idle":
            style.idle_animation = anim
        elif trigger == "hover":
            style.hover_animation = anim
        elif trigger == "focus":
            style.focus_animation = anim
        elif trigger == "active":
            style.active_animation = anim
        
        logger.info(f"✨ Animation applied: {element_id} ({trigger})")
        return True
    
    def enable_particles(
        self,
        element_id: str,
        particle_type: str = "sparkles",
        count: int = 10,
        color: str = "#00d9ff"
    ) -> bool:
        """Enable particle effects for an element"""
        
        style = self.get_style(element_id)
        if not style:
            return False
        
        style.particles = ParticleEffect(
            enabled=True,
            type=particle_type,
            count=count,
            color=color
        )
        
        logger.info(f"✨ Particles enabled: {element_id}")
        return True
    
    def apply_gradient(
        self,
        element_id: str,
        gradient_type: str = "linear",
        angle: float = 45.0,
        colors: Optional[List[Tuple[str, float]]] = None
    ) -> bool:
        """Apply gradient effect to an element"""
        
        style = self.get_style(element_id)
        if not style:
            return False
        
        stops = []
        if colors:
            stops = [GradientStop(color, position) for color, position in colors]
        
        style.gradient = GradientConfig(
            enabled=True,
            type=gradient_type,
            angle=angle,
            stops=stops
        )
        
        logger.info(f"✨ Gradient applied: {element_id}")
        return True
    
    def apply_3d_transform(
        self,
        element_id: str,
        rotate_x: float = 0,
        rotate_y: float = 0,
        rotate_z: float = 0,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
        scale_z: float = 1.0
    ) -> bool:
        """Apply 3D transforms to an element"""
        
        style = self.get_style(element_id)
        if not style:
            return False
        
        style.rotate_x = rotate_x
        style.rotate_y = rotate_y
        style.rotate_z = rotate_z
        style.scale_x = scale_x
        style.scale_y = scale_y
        style.scale_z = scale_z
        
        logger.info(f"✨ 3D transform applied: {element_id}")
        return True
    
    def export_style(self, element_id: str) -> Optional[str]:
        """Export style as JSON"""
        style = self.get_style(element_id)
        if not style:
            return None
        
        return json.dumps(style.to_dict(), indent=2)
    
    def export_all_styles(self) -> str:
        """Export all styles as JSON"""
        all_styles = {
            element_id: style.to_dict()
            for element_id, style in self.styles.items()
        }
        return json.dumps(all_styles, indent=2)
    
    def list_available_styles(self) -> List[str]:
        """List all available styles"""
        return list(self.styles.keys())
    
    def list_available_themes(self) -> List[str]:
        """List all available themes"""
        return list(self.themes.keys())


# Singleton instance
visual_engine = VisualStylingEngine()
